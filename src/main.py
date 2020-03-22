#!/usr/bin/python3

import logging
import sys
import asyncio
import RPi.GPIO as GPIO
import pyudev
import evdev
from evdev import InputDevice, categorize, ecodes
import traceback
import time
import board
import busio
from transitions import Machine
from adafruit_ht16k33 import segments


# =---------------------------------------------------------------------------------- Constants =--=

# Logging
LOG_FORMAT = '{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'

# GPIO Pins
PINS = {
    'SOLENOID': 17,
    'PUSH_BUTTON': 27,
    'KEY_SWITCH': 22,
    'TOGGLE_SWITCH': 23,
    'TOGGLE_LED': 24
}

# Keyboard event scancode to character maps
SCAN_CODE = {
    # Scancode: ASCIICode
    0: u'', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8', 10: u'9',
    11: u'0', 16: u'q', 17: u'w', 18: u'e', 19: u'r', 20: u't', 21: u'y', 22: u'u', 23: u'i',
    24: u'o', 25: u'p', 30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j',
    37: u'k', 38: u'l', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n', 50: u'm',
    69: u'', 71: u'7', 72: u'8', 73: u'9', 75: u'4', 76: u'5', 77: u'6', 79: u'1', 80: u'2',
    81: u'3', 82: u'0'
}

CAPS_CODE = {
    0: u'', 16: u'Q', 17: u'W', 18: u'E', 19: u'R', 20: u'T', 21: u'Y', 22: u'U', 23: u'I',
    24: u'O', 25: u'P', 30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J',
    37: u'K', 38: u'L', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N', 50: u'M',
    69: u''
}


# =-----------------------------------------------------------------------------------= Globals =--=

# Control path
yubikey_path = None
loop = None
launch_control = None

# 14-segment Display
i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg14x4(i2c)
display.fill(0)  # clear the display
display.brightness = 1.0

# Logging
logger = logging.getLogger('launch_control')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(LOG_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)


# =----------------------------------------------------------------------= Finite State Machine =--=

class LaunchControl(object):
    states = ['off', 'on', 'waiting', 'standby', 'ready', 'launching']

    def __init__(self):
        self.machine = Machine(
            model=self, states=LaunchControl.states, initial='off', ignore_invalid_triggers=True)

        # Add transitions
        self.machine.add_transition('init', 'off', 'off')
        self.machine.add_transition('turn_on', 'off', 'on')
        self.machine.add_transition('key_insert', 'on', 'waiting')
        self.machine.add_transition('authenticate', 'waiting', 'standby')
        self.machine.add_transition('auth_timeout', 'standby', 'waiting')
        self.machine.add_transition('unlock', 'standby', 'ready')
        self.machine.add_transition('launch', 'ready', 'launching')
        self.machine.add_transition('complete', 'launching', 'ready')
        self.machine.add_transition('lock', ['ready', 'launching'], 'waiting')
        self.machine.add_transition(
            'turn_off', ['on', 'waiting', 'standby', 'ready', 'launching'], 'off')
        self.machine.add_transition(
            'key_remove', ['waiting', 'standby', 'ready', 'launching'], 'on')

    def on_enter_off(self):
        logger.info("Enter state Off")
        display.fill(0)
        if not GPIO.input(PINS['TOGGLE_SWITCH']):
            if launch_control:
                launch_control.turn_on()
            return None

        GPIO.output(PINS['TOGGLE_LED'], GPIO.LOW)

    def on_enter_on(self):
        logger.info("Enter state On")
        display.print('----')
        display.show()
        GPIO.output(PINS['TOGGLE_LED'], GPIO.HIGH)

        if yubikey_path and launch_control:
            launch_control.key_insert()

    def on_enter_waiting(self):
        logger.info("Enter state Waiting")
        display.print('AUTH')
        display.show()

    def on_enter_standby(self):
        logger.info("Enter state Standby")
        display.print('OPEN')
        display.show()
        asyncio.get_event_loop().create_task(pull_solenoid())

    def on_enter_ready(self):
        logger.info("Enter state Ready")
        display.print('-GO-')
        display.show()

    def on_enter_launching(self):
        logger.info("Enter state Launching")
        asyncio.get_event_loop().create_task(do_launch())


# =----------------------------------------------------------------------------= Async Handlers =--=

async def pull_solenoid():
    GPIO.output(PINS['SOLENOID'], GPIO.HIGH)
    await asyncio.sleep(3)
    GPIO.output(PINS['SOLENOID'], GPIO.LOW)

    if launch_control:
        launch_control.auth_timeout()


async def do_launch():
    logger.debug('launching!')
    task = asyncio.get_event_loop().create_task(animate_launch())
    await asyncio.sleep(5)
    task.cancel()
    logger.debug('launch complete')

    if launch_control:
        launch_control.complete()


async def authenticate_code(code):
    if launch_control:
        launch_control.authenticate()


async def animate_launch():
    while True:
        display.print('*   ')
        display.show()
        await asyncio.sleep(.5)
        display.print(' *  ')
        display.show()
        await asyncio.sleep(.5)
        display.print('  * ')
        display.show()
        await asyncio.sleep(.5)
        display.print('   *')
        display.show()
        await asyncio.sleep(.5)
        display.print('  * ')
        display.show()
        await asyncio.sleep(.5)
        display.print(' *  ')
        display.show()
        await asyncio.sleep(.5)


# =--------------------------------------------------------------------= GPIO Callback Handlers =--=

def toggle_switch(launch_control):
    if GPIO.input(PINS['TOGGLE_SWITCH']):
        # high = off
        logger.debug('toggle switch turned off')
        launch_control.turn_off()
    else:
        logger.debug('toggle switch turned on')
        launch_control.turn_on()


def key_switch(launch_control):
    if GPIO.input(PINS['KEY_SWITCH']):
        # high = off
        logger.debug('key switch locked')
        launch_control.lock()
    else:
        logger.debug('key switch unlocked')
        launch_control.unlock()


def push_button(launch_control):
    if not GPIO.input(PINS['PUSH_BUTTON']):
        logger.debug('push button pressed')
        launch_control.launch()


def gpio_callback(callback, launch_control):
    if loop is None:
        logger.exception("Error: Main loop went missing")
        return  # should not come to this
    loop.call_soon_threadsafe(callback, launch_control)


# =-------------------------------------------------------------------= Yubikey and Key Hanlers =--=

def setup_yubikey():
    logger.debug("Looking for Yubikey device")
    allDev = [InputDevice(dev) for dev in evdev.list_devices()]
    if len(allDev) == 0:
        logger.debug("No Yubikey found")
        return

    for device in allDev:
        if "usb" in device.phys and "Yubico" in device.name:
            logger.info("Yubikey device found at path %s", device.path)
            global yubikey_path
            yubikey_path = device.path
            device = InputDevice(device.path)
            asyncio.get_event_loop().create_task(read_yubikey(device))
            return

    logger.debug("No Yubikey found")


async def read_yubikey(device):
    code = ''
    shifted = False

    device.grab()
    try:
        async for event in device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if data.scancode == 42:  # LSHIFT, RSHIFT is 54
                    if data.keystate == 1:
                        shifted = True
                    if data.keystate == 0:
                        shifted = False

                if data.keystate == 1:  # Down events only
                    if data.scancode != 42 and data.scancode != 28:
                        if shifted:
                            key_lookup = u'{}'.format(
                                CAPS_CODE.get(data.scancode)) or ''
                        else:
                            key_lookup = u'{}'.format(
                                SCAN_CODE.get(data.scancode)) or ''

                        code += key_lookup

                    if data.scancode == 28:
                        logger.info('Yubikey code entered: %s', code)
                        asyncio.get_event_loop().create_task(authenticate_code(code))
                        code = ''
                        # return code
    except OSError:
        logger.debug("Yubikey likely removed")


def input_device_callback(action, udev, launch_control):
    if not udev.device_node:
        return

    if loop is None:
        logger.exception("Error: Main loop went missing")
        return  # should not come to this
    loop.call_soon_threadsafe(
        input_device_action, action, udev.device_node, launch_control)


def input_device_action(action, device_node, launch_control):
    global yubikey_path

    if action == "add":
        device = InputDevice(device_node)
        if "Yubico" in device.name:
            logger.info("Yubikey device inserted at %s", device_node)
            yubikey_path = device_node
            asyncio.get_event_loop().create_task(read_yubikey(device))

            # attempt FSM transition
            launch_control.key_insert()
    else:
        if device_node == yubikey_path:
            logger.info("Yubikey device removed")
            yubikey_path = None

            # attempts FSM transition
            launch_control.key_remove()


# =-----------------------------------------------------------------= Setup and Main Event Loop =--=

if __name__ == '__main__':
    try:
        # setup the GPIO
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PINS['SOLENOID'], GPIO.OUT)
        GPIO.setup(PINS['TOGGLE_LED'], GPIO.OUT)
        GPIO.setup(PINS['TOGGLE_SWITCH'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS['KEY_SWITCH'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS['PUSH_BUTTON'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(PINS['TOGGLE_SWITCH'], GPIO.BOTH, lambda pin: gpio_callback(
            toggle_switch, launch_control), bouncetime=500)
        GPIO.add_event_detect(PINS['KEY_SWITCH'], GPIO.BOTH, lambda pin: gpio_callback(
            key_switch, launch_control), bouncetime=500)
        GPIO.add_event_detect(PINS['PUSH_BUTTON'], GPIO.BOTH, lambda pin: gpio_callback(
            push_button, launch_control), bouncetime=500)

        # Watch for keyboard add/remove
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='input')

        observer = pyudev.MonitorObserver(monitor, lambda action, device: input_device_callback(
            action, device, launch_control))
        observer.start()

        # check for yubikey already inserted
        setup_yubikey()

        # setup FSM
        launch_control = LaunchControl()
        launch_control.init()

        # run the event loop
        loop = asyncio.get_event_loop()
        loop.run_forever()
        loop.close()
    except KeyboardInterrupt:
        logger.debug("Breaking out of main loop")
    except:
        exc_info = sys.exc_info()
        logger.exception("Error: %s", exc_info)
        traceback.print_exception(*exc_info)

    # cleanup
    logger.info("Cleanup and exit")
    display.fill(0)
    GPIO.cleanup()

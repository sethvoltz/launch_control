# Launch Control

A fun 70's industrial "launch" control panel with a Yubikey key switch

## Install

Clone this repo onto the launch control Raspberry Pi and run the following:

```bash
pip3 install pyudev evdev transitions adafruit-blinka adafruit-circuitpython-ht16k33
cd launch_control
./bin/install
```

When it is complete, reboot to validate operation. You can view and follow logs with

```bash
journalctl -u launch_control.service -f
```

## Enroll Yubikey

TBD

## To Do

- [ ] Script to authenticate against Yubico server and validate token
- [ ] Script to enroll a Yubikey locally and pair it with a given action
- [ ] Scroll a custom name string for a recognized Yubikey on the display

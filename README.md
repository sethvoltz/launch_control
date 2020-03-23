# Launch Control

![Header image made of photos of the control](https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/header.jpg)

A fun 70's industrial inspired "launch" control panel with a Yubikey key switch. If the Yubikey is authenticated as valid by Yubico servers and is recognized as enrolled on the device, it pulls a solenoid and allows the user to turn the Yubikey like a real key, engaging the system.

**Watch a demo of the prototype in action!**

[![Screenshot of demo video](https://img.youtube.com/vi/w-GI3CmeeaE/0.jpg)](https://youtu.be/w-GI3CmeeaE "Click here to watch a demo on YouTube")

## Install

1. Get a new [API Key from Yubico][apikey].

2. Clone this repo onto the launch control Raspberry Pi and run the following:

    ```bash
    pip3 install pyudev evdev transitions adafruit-blinka adafruit-circuitpython-ht16k33 yubico-client
    cd launch_control
    cp config.json.example config.json
    ./bin/install
    ```

3. Edit `config.json` with your API key and secret

4. Reboot to validate operation. You can view and follow logs with

    ```bash
    journalctl -u launch_control.service -f
    ```

[apikey]: https://upgrade.yubico.com/getapikey/

## Enroll Yubikey

TBD

## Media and Build

I have included a [bunch of build and notebook photos][photos] taken across the project. These are numbered in order to tell a story, not necessarily chronological order, as can be seen by the dates in the notebook photos. Additionally, here is a [short CAD demo][lock-demo] of how the Yubi-lock works, taken from within Fusion 360.

[photos]: https://github.com/sethvoltz/launch_control/tree/master/media/build-photos
[lock-demo]: https://youtu.be/Ur00jpR6VwQ

## To Do

- [ ] Script to enroll a Yubikey locally and pair it with a given action
- [ ] Scroll a custom name string for a recognized Yubikey on the display
- [ ] Include CAD for Yubi-lock

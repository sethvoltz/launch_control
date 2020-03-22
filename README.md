# Launch Control

A fun 70's industrial inspired "launch" control panel with a Yubikey key switch

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

## To Do

- [ ] Script to enroll a Yubikey locally and pair it with a given action
- [ ] Scroll a custom name string for a recognized Yubikey on the display

# Launch Control

![Header image made of photos of the control](https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/header.jpg)

A fun 70's industrial inspired "launch" control panel with a Yubikey key switch. If the Yubikey is authenticated as valid by Yubico servers and is recognized as enrolled on the device, it pulls a solenoid and allows the user to turn the Yubikey like a real key, engaging the system.

**Watch a demo of the prototype in action!**

[![Screenshot of demo video](https://img.youtube.com/vi/w-GI3CmeeaE/0.jpg)](https://youtu.be/w-GI3CmeeaE "Click here to watch a demo on YouTube")

## History

This project was insprired by an idea a friend and I used to joke about back in 2011/2012 timeframe when he was working at a small startup and they wanted something more fun to push their code to production. They were already using Yubikeys to authenticate against the deploy server as a second factor and we thought why not make it a standalone device. The idea at the time was something more akin to those covered buttons that took a key to flip open the lid, and when you pressed it, it would turn on a police-style spinning light 🚨 while the deply was going on.

Flash forward to the winter of 2019 when this idea was brought up over a beers with friends and I decided I had the skills and components laying around to actually make this happen. It started [as a sketch][idea-sketch] one evening to realize the central mechanism was all about a USB port that only fit a Yubikey, disguised as a lock cylinder. After a few spins in Fusion 360 to work out the lock mechanism, and [some][usb-port] [detailed][microswitch] [sketches][solenoid] of the various bits and bobs I thought were needed, I was able to [3D print][lock-prototype] a succesful machanism.

From that foundation, I worked through the rest of the placement, and had a friend with a wood shop cut some scrap wood to make the prototype case. The sizing is wrong (I forgot to take into account the [breakout board][breakout-board] needed, and the Raspberry Pi case) and the metal work is rough (I don't have the right tools for sheet metal work, so I made do) but it was enough to get it together with some solder, hot glue and a bunch of heat shrink tubing. And some extra screws to lift it up enough to fit everything.

Keep an eye on this repo for updates to the software and more details about the internal mechanism, parts used, and some hacks I did to pull it together into a working prototype.

[idea-sketch]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/01%20-%20First%20concept%20sketch.jpg
[usb-port]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/05%20-%20Component%20detail%20sketch%20-%20USB%20female%20socket.jpg
[microswitch]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/03%20-%20Component%20detail%20sketch%20-%20microswitch.jpg
[solenoid]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/04%20-%20Component%20detail%20sketch%20-%20solenoid.jpg
[lock-prototype]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/08%20-%20Yubi-lock%20final%20prototype%20with%20components.jpg
[breakout-board]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/13%20-%20Assembled%20Raspberry%20Pi%20and%20breakout%20board.jpg

## Install

1. Get a new [API Key from Yubico][apikey].

2. Clone this repo onto the launch control Raspberry Pi and run the following:

    ```bash
    cd launch_control
    pip3 install -r requirements.txt
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
  - A script in bin to read a Yubikey, extract the identifier and ask for a script to run for that device's launch action
- [ ] Create a general display asyncio Task for running the display
  - Some function to set display to static string, scroll, or the launch animation and the display Task itself to run an infinite loop looking for changes to the display mode and to tick the display forward.
- [ ] Scroll a custom name string for a recognized Yubikey on the display
  - Additionally take a display name for an enrolled Yubikey and extend the display loop to show it
- [ ] Include CAD for Yubi-lock
- [ ] Automatic (or scripted) updates via Git pull and service restart

# Launch Control

![Header image made of photos of the control](https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/header.jpg)

A fun 70's industrial inspired "launch" control panel with a Yubikey key switch. If the Yubikey is authenticated as valid by Yubico servers and is recognized as enrolled on the device, it pulls a solenoid and allows the user to turn the Yubikey like a real key, engaging the system.

**Watch a demo of the prototype in action!**

[![Screenshot of demo video](https://img.youtube.com/vi/w-GI3CmeeaE/0.jpg)](https://youtu.be/w-GI3CmeeaE "Click here to watch a demo on YouTube")

## History

This project was insprired by an idea a friend and I used to joke about back in 2011/2012 timeframe, when he was working at a small startup and they wanted something more fun to push their code to production. They were already using Yubikeys to authenticate against the deploy server as a second factor and we thought why not make it a standalone device. The idea at the time was something more akin to those covered buttons that took a key to flip open the lid, and when you pressed it, it would turn on a police-style spinning light 🚨 while the deply was going on.

Flash forward to the winter of 2019 when this idea was brought up over a beers with friends and I decided I had the skills and components laying around to actually make this happen. It started [as a sketch][idea-sketch] one evening to realize the central mechanism was all about a USB port that only fit a Yubikey, disguised as a lock cylinder. After a few spins in Fusion 360 to work out the lock mechanism, and [some][usb-port-drawing] [detailed][microswitch-drawing] [sketches][solenoid-drawing] of the various bits and bobs I thought were needed, I was able to [3D print][lock-prototype] a succesful machanism.

From that foundation, I worked through the rest of the placement, and had a friend with a wood shop cut some scrap wood to make the prototype case. The sizing is wrong (I forgot to take into account the [breakout board][breakout-board] needed, and the Raspberry Pi case) and the metal work is rough (I don't have the right tools for sheet metal work, so I made do) but it was enough to get it together with some solder, hot glue and a bunch of heat shrink tubing. And some extra screws to lift it up enough to fit everything.

Keep an eye on this repo for updates to the software and more details about the internal mechanism, parts used, and some hacks I did to pull it together into a working prototype.

[idea-sketch]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/01%20-%20First%20concept%20sketch.jpg
[usb-port-drawing]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/05%20-%20Component%20detail%20sketch%20-%20USB%20female%20socket.jpg
[microswitch-drawing]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/03%20-%20Component%20detail%20sketch%20-%20microswitch.jpg
[solenoid-drawing]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/04%20-%20Component%20detail%20sketch%20-%20solenoid.jpg
[lock-prototype]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/08%20-%20Yubi-lock%20final%20prototype%20with%20components.jpg
[breakout-board]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/13%20-%20Assembled%20Raspberry%20Pi%20and%20breakout%20board.jpg

## Hardware

The launch control is composed of a handful of parts, mounted on a sheet metal cover and in a wooden box. Below are the parts I used, however they can be swapped out for your needs and the software tweaked for the specifics of your setup. Additionally, the central component is the Yubikey Lock, which is 3D printed, lightly sanded to make rotation smooth, and parts hot glued, screwed or rubber banded into place. More on that later.

### Parts List

**Launch Panel:**

- [Illuminated toggle switch][toggle] ‡ modified
- [Adafruit 14-segment display and backpack][display]
- [Mushroom push button][button]
- [Lit power button][power-button]
- [5V 8A power supply with socket][power-supply]
- Raspberry Pi 3 and case (dealer's choice)

**Yubikey Lock:**

- [Microswitch][microswitch]
- [Female and male USB A][usb-female]
- [Heat set inserts][heat-set]
- [Solenoid][solenoid]

**Misc Other Parts:**

- [Adafruit Perma-Proto][perma-proto]
- [Adafruit Trinket M0][trinket]

[toggle]: https://www.adafruit.com/product/3218
[display]: https://www.adafruit.com/product/2157
[button]: https://www.amazon.com/gp/product/B07QL1PYP1
[microswitch]: https://www.amazon.com/gp/product/B073TYWX86
[usb-female]: https://www.amazon.com/gp/product/B07569PK5B
[heat-set]: https://www.amazon.com/gp/product/B077CJV3Z9
[solenoid]: https://www.amazon.com/gp/product/B013DR655A
[perma-proto]: https://www.adafruit.com/product/1609
[trinket]: https://www.adafruit.com/product/3500
[power-button]: https://www.adafruit.com/product/3105
[power-supply]: https://www.amazon.com/gp/product/B07RJPV36C

‡ The illuminated toggle in the parts list didn't quite work for my needs, due to the LED and the switch being electrically connected internally. In order to isolate them, so that the LED can be controlled independently by the Raspberry Pi at a different voltage level than the GPIO sensing the switch. To do this, you need to pry open the metal sides of the switch, careful to take note of where everything is inside. Clip the resistor lead connected to the bottom pin, notch out part of the plastic case and feed the wire through. Solder on and extension wire, and wrap in heat-shrink to protect it. Bend the metal case closed, put everything back in and snap it shut. It didn't perfectly close for me, so I had to wrap a bit of Kapton tape around it.

### 3D Printing

Print out all the parts from the [STLs folder][stl-folder]. There are individual STLs for each part, as well as a combined one that fits in my teeny Monoprice printer. Before assembly, you will likely need to sand down the core to smooth out some of the 3D printing lines. Be sure it slips into the shell and rotates without too much friction. Don't sand it too far, otherwise there can be problems with binding later.

**[To assemble...][lock-prototype]**

- First, solder wires onto the USB female port, then onto the microswitch.
- Carefully bend the end of the microswitch arm into a slight curve, as shown in the photos and [sketch][microswitch-drawing].
- Hot glue the USB port into the core, then hot glue in the microswitch, and add a bit more hot glue to secure the wires of the USB and microswitch into the center, along the axis of rotation.
- At the other end of the wires from the USB socket, solder on the male USB-A and wrap the wires in heat shrink or electrical tape.
- Rubber band the solenoid onto the base plate.
- Use a heat-set tool or a soldering iron to put the heat-set inserts into the shell, insert the core into the shell and use the retainer to lock it in.
- Finally, place the base plate with the solenoid onto the shell and screw it in with M3 screws.
  - Due to tolerances in 3D printers and imperfect alignment of the inserts, you'll have to play around with how tight you tighten the screws down to make sure the solenoid and core can still move freely and doesn't bind.

With [everything assembled][lock-demo], now is the time to test that the movement is smooth, the USB pass-through works, the solenoid retracts properly, and to tweak the rouded bend on the microswitch to engage right at the end of the key turn. It should contact somewhere after turning 45°, preferrably right before a full 90°.

[stl-folder]: https://github.com/sethvoltz/launch_control/tree/master/hardware/stl

### Breakout Board

Using the [provided diagram][breakout-wiring], solder everything onto the [Adafruit Perma Protoboard][perma-proto], using sockets for the trinket placement. Write the [SoftPower][soft-power] firmware to the [trinket][], and socket it into the board. On the right side of the board, use sockets or screw terminals for the Raspberry Pi connector (I used screw terminals, if I were to do it again I would use sockets to make maintenance easier). Solder wires from all the Raspberry Pi terminals/sockets to the appropriate place on the board, according to the [provided diagram][pi-wiring]. Sorry, I don't have better build progress photos for it. Ideally, this would be a dedicated PCB to make it more compact and make wiring a no-brainer.

[breakout-wiring]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/10%20-%20Board%20layout%20for%20breakout%20perma-proto%20board.jpg
[pi-wiring]: https://raw.githubusercontent.com/sethvoltz/launch_control/master/media/build-photos/10%20-%20Board%20layout%20for%20breakout%20perma-proto%20board.jpg

### Assemble

To finish everything up, just... cut some pieces of wood and sheet metal, a bunch of lengths of wire, cut holes in the metal, screw and bolt the bits in place, solder the wires onto all the bits and shove it all inside. Install the software and power it up.

More on the above later.

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
- [ ] Automatic (or scripted) updates via Git pull and service restart
- [ ] Make a cool icon or logo for this project. PRs welcome 😇

## Press

- [Adafruit Daily][adafruit-daily]
- [Hack-A-Day][hackaday]

[adafruit-daily]: https://hackaday.com/2020/03/26/launch-console-delivers-enjoyment-to-software-deployment/
[hackaday]: https://hackaday.com/2020/03/26/launch-console-delivers-enjoyment-to-software-deployment/

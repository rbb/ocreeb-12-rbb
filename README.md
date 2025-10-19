# Ocreeb12-rbb

This is a fork of [Ocreeb12](https://github.com/sb-ocr/ocreeb-12). Many thanks
to Salim Benbouziyane, for putting together the mechanicals and PCBs!.

The goal of this fork is to update the versions of KMK and Circuit Python used
in the project.

# Ocreeb12 Stuff
Watch the build video ↓

[<img src="/Images/001.png">](https://youtu.be/P_oSLBZABGA)

This is a 12 key macro keypad with 2 rotary encoders, custom keycaps and under-glow RGB. 
Ocreeb is running KMK firmware on the Adafruit KB2040.

Order the PCB: [pcbway.com](https://www.pcbway.com/project/shareproject/DIY_Mechanical_Macro_Keypad_Ocreeb_24300065.html)

Build instructions: [instructables.com](https://www.instructables.com/DIY-Mechanical-Macro-Keypad-Ocreeb/)

# New in this Fork

## Copies of Libraries

I've copied the necessary files for making library changes (most likely to add
files that are not already in the Firmware/ directory) to:
- `CircuitPython/`
- `kmk_full/`

## Quick Start Software Guide.

1. Install the Circuit Python UF2 on the KB2040, by copying the appropriate UF2
and libraries to the RPI-RP2 mass storage device.
Once you have your KB2040 board, get a copy of [CircuitPython for the KB2040](https://circuitpython.org/board/adafruit_kb2040/).

Optionally, if you will want to be adding libraries, download the
[Library](https://circuitpython.org/libraries)
[V10.x](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20251014/adafruit-circuitpython-bundle-10.x-mpy-20251014.zip).

Note: This fork also has copies of these under `CircuitPython/`.

Circuit Python has [instructions for install](https://learn.adafruit.com/adafruit-kb2040/circuitpython).
Basically, you just copy the UF2 file to the RPI-RP2 drive that shows up when
you plug in the KB2040. After it reboots itself, it should show up as a drive
called CIRCUITPY.

2. Copy everything in the Firmware/ directory onto the new CIRCUITPY drive.
Salim has some instructions about disabling the CIRCUITPY from showing up after
your done, but I've just left it alone, so that making changes is easier.

3. After copying, it should automatically reboot, and be functional.

## Debugging.

When connecting over USB, a serial port is created. Debug messages (and any
print statements you add to the Python code) show up here.

On a Mac, it is usually `/dev/tty.usbmodem14101`. Use your favorote terminal
emulator, or the [mu editor](https://codewith.mu/) to connect to it. I usually use `screen`.

   ```
   screen /dev/tty.usbmodem14101 115200
   ```

Note: when you copy a new file to the CIRCUITPY drive, the KB2040 will reboot,
and most terminal emulators will behave funny. I typically get out of the
terminal emulator (with screen it is ctrl-a, then k, then y) before doing a
copy.

## Changing the Macros

Change the code in `CIRCUITPY/code.py` to meet your needs.

I will typically edit on my PC/Mac and copy the changes.

   ```
   cp code.py /Volumes/CIRCUITPY/
   ```

## Current Status

I had to make some `code.py` changes to support syntax/command changes in the
latest kmk library (October 2025). For the moment, I've ripped out the layers
and changed to just a simple set of macro keys. I've added a repeat (RapidFire)
to some of the keys. I've re-implemented layers, and color coded the backlights
to the current layer.

I have not been able to get combos or sequences (inputs) to work.

I've added and examples/ folder for putting in code.py examples. The older,
single layer code.py is in there now.

Some notes on the current code.py:
- Upper left key switches between layers (sets of keymaps).
- Encoder 1 is volume. Encoder 2 changes, depending on the layer.
- The lock key (upper right) has only been tested with MacOs.

Other Notes:
- I'd like to figure out a way to get the macros/keys to change, depending on
the host OS. But since this is an HID device, it only sends data, and does not
receive data. So, it would be complicated. Maybe use the debug serial port?
Otherwise, we'd probably have to figure out a way to add an extra USB endpoint,
which probably means abandoning KMK?

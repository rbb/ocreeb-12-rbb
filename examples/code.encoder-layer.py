import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, Key
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
#from kmk.modules.combos import Combos, Chord, Sequence
from kmk.modules.rapidfire import RapidFire
from kmk.modules.macros import Macros, Tap, Delay, Press, Release
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB

print("Starting")

# KEYBOARD SETUP
keyboard = KMKKeyboard()
encoders = EncoderHandler()

# MODULES
rapid_fire_module = RapidFire()
macros_module = Macros()
#combos = Combos()
#combos.timeout = 1000  # milliseconds
#leader = Leader()
#layers = Layers()

# Modules - RGB Stuff
# More colors at https://docs.qmk.fm/features/rgblight
RED = 0
ORANGE = 45
GREEN = 85
CYAN = 125
BLUE = 170
PURPLE = 205
class LayerRGB(RGB):
    def on_layer_change(self, layer):
        if layer == 0:
            self.set_hsv_fill(BLUE, self.sat, self.val)
        elif layer == 1:
            self.set_hsv_fill(GREEN, self.sat, self.val)
        elif layer == 2:
            self.set_hsv_fill(RED, self.sat, self.val)
        else:
            self.set_hsv_fill(0, 0, 0)       # off
        # update the LEDs manually if no animation is active:
        self.show()


rgb = LayerRGB(pixel_pin=board.D10,  # GPIO pin of the status LED, or background RGB light
        num_pixels=4,                # one if status LED, more if background RGB light
        rgb_order=(1, 0, 2),         # GRB order for the ocreeb-12 hardware
        hue_default=BLUE,            # in range 0-255: 0/255-red, 85-green, 170-blue
        sat_default=255,
        val_default=16,
        )


class RGBLayers(Layers):
    def activate_layer(self, keyboard, layer, idx=None):
        super().activate_layer(keyboard, layer, idx)
        rgb.on_layer_change(layer)

    def deactivate_layer(self, keyboard, layer):
        super().deactivate_layer(keyboard, layer)
        rgb.on_layer_change(keyboard.active_layers[-1])
layers = RGBLayers()

# Add all modules/extensions
keyboard.modules = [encoders, rapid_fire_module, macros_module, layers] #, combos]
keyboard.extensions = [rgb, MediaKeys()]

# --- LAYER CYCLING MACRO DEFINITIONS ---
# This approach uses a Macro to calculate the next/previous layer and uses
# KC.TO(N) to switch, ensuring the RGB extension receives the layer change event.

def cycle_layer_plus(keyboard):
    # Get the highest active layer index
    current_layer = keyboard.active_layers[-1]
    num_layers = len(keyboard.keymap)
    # Calculate next layer with wrap-around (0 -> 1 -> 2 -> 0)
    next_layer = (current_layer + 1) % num_layers

    # Use KC.TO(N) via tap_key for guaranteed layer and RGB update
    keyboard.tap_key(KC.TO(next_layer))
    return keyboard

def cycle_layer_minus(keyboard):
    # Get the highest active layer index
    current_layer = keyboard.active_layers[-1]
    num_layers = len(keyboard.keymap)
    # Calculate previous layer with wrap-around (0 -> 2 -> 1 -> 0)
    # Adding num_layers before subtracting prevents negative modulo results.
    prev_layer = (current_layer - 1 + num_layers) % num_layers

    # Use KC.TO(N) via tap_key for guaranteed layer and RGB update
    keyboard.tap_key(KC.TO(prev_layer))
    return keyboard

# Instantiate the custom macro keys
LCY_P = KC.MACRO(cycle_layer_plus)
LCY_M = KC.MACRO(cycle_layer_minus)
# --------------------------------------------------------

# SWITCH MATRIX
keyboard.col_pins = (board.D3, board.D4, board.D5, board.D6)
keyboard.row_pins = (board.D7, board.D8, board.D9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ENCODERS
encoders.pins = ((board.A2, board.A1, board.A0, False),
                 (board.SCK, board.MISO, board.MOSI, False),
                 )

# Note: probably needs a custom keyboard shortcut defined in Mac OS.
TERMINAL = KC.MACRO(
    Tap(KC.LCMD(KC.LALT(KC.LSFT(KC.T)))), # Open Terminal (assuming LCMD = GUI)
    Tap(KC.LCTRL(KC.U))                  # Custom terminal command (e.g., clear line)
)
# Note: Another Mac OS thing
FORCE_QUIT = KC.MACRO(
    Tap(KC.LCMD(KC.LALT(KC.ESCAPE)))     # Force Quit dialog
)
# Note: This works on Mac OS, not tested on other operating systems yet.
LOCK = KC.MACRO(
    Tap(KC.LCTRL(KC.LCMD(KC.Q))),        # Lock Screen
    Delay(400),                          # Wait for system to register lock
    Tap(KC.ESCAPE)                       # Escape (safeguard/clear other apps)
)
# YouTube Speed Jumps, by 2
SPEED_UP = KC.MACRO(Tap(KC.RABK), Tap(KC.RABK))  # Youtube change speed faster
SPEED_DN = KC.MACRO(Tap(KC.LABK), Tap(KC.LABK))  # Youtube change speed slower

SAT_UP = KC.RF(KC.RGB_SAI)
SAT_DN = KC.RF(KC.RGB_SAD)
RGB_UP = KC.RF(KC.RGB_VAI)
RGB_DN = KC.RF(KC.RGB_VAD)
HUE_UP = KC.RF(KC.RGB_HUI)
HUE_DN = KC.RF(KC.RGB_HUD)

# KEYMAPS
# Notice that the first position (Index=0 in KMK terms, upper left key on the
# ocreeb-12, is always LCY_P, so that regardless of the current layer, that key
# will ALWAYS cycle to the next layer.
keyboard.keymap = [
    # Layer 0 (Blue), Youtube
    [
        LCY_P, TERMINAL, KC.MEDIA_PLAY_PAUSE, LOCK,
        KC.F2, SPEED_DN, KC.AUDIO_MUTE,       SPEED_UP,
        KC.A,  KC.LEFT,  KC.SPACE,            KC.RIGHT,
    ],
    # Layer 1 (Green), numpad?
    [

        LCY_P, KC.N2, KC.N3, KC.N4,
        KC.N5, KC.N6, KC.N7, KC.N8,
        KC.B, KC.N0, KC.MINS, KC.EQL,
    ],
    # Layer 2 (Red), media
    [
        #KC.MPLY, KC.MPRV, KC.MNXT, KC.MSTP,
        LCY_P,  KC.MPRV, KC.MNXT, KC.MSTP,
        KC.VOLD, KC.VOLU, KC.MUTE, KC.NO,
        KC.C, KC.NO, KC.NO, KC.NO,
    ],
]

# COMBOS for Layer Cycling
# NOTE: Could not get Chords or Sequences to work
#combos.combos = [
#    # Combo Upper left key, plus another key in the top row to change layers.
#    Chord((0, 1), KC.TO(0), timeout=200),
#    Chord((0, 2), KC.TO(1), timeout=200),
#    Chord((0, 3), KC.TO(2), timeout=200),
#]

ENC_MAP_VOL = (KC.AUDIO_VOL_DOWN,   # CW = vol down
            KC.AUDIO_VOL_UP,     # CCW = vol up
            KC.AUDIO_MUTE,       # push = mute toggle
            )
ENC_MAP_RGB_BRIGHT = (KC.RGB_VAD,  # CW=RGB ocreeb-12 backlighting brightness down
                       KC.RGB_VAI,  # CCW=RGB ocreeb-12 backlighting brightness up
                       KC.RGB_TOG   # Push= RGB on/off
            )
ENC_MAP_LAYER = (LCY_M,       # CW=backward through layers
                 LCY_P,       # CCW= Forward through layers
                 KC.NO        # Push= Nothing
            )
ENC_MAP_UP_DOWN = (KC.DOWN,  # CW=down
                    KC.UP,  # CCW=UP
                    KC.NO     # Push= Nothing
            )
ENC_MAP_SHIFT_UP_DOWN = (KC.LSFT(KC.DOWN),  # CW=down
                         KC.LSFT(KC.UP),  # CCW= Forward through layers
                         KC.NO               # Push= Nothing
            )
# Keep encoder 1 always adjusts volume.
# Keep encoder 2 always adjusts layer.
encoders.map = [(ENC_MAP_VOL, ENC_MAP_LAYER),
                (ENC_MAP_VOL, ENC_MAP_LAYER),
                (ENC_MAP_VOL, ENC_MAP_LAYER),
                ]

if __name__ == '__main__':
    keyboard.go()

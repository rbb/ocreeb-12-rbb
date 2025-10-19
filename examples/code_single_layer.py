import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.rapidfire import RapidFire
from kmk.modules.macros import Macros, Tap, Delay, Press, Release
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB

print("Starting")

# KEYBOARD SETUP
keyboard = KMKKeyboard()
encoders = EncoderHandler()

# MODULES
rapid_fire_module = RapidFire()
macros_module = Macros()

# ADDED modules to modules list
keyboard.modules = [encoders, rapid_fire_module, macros_module]

# SWITCH MATRIX
keyboard.col_pins = (board.D3, board.D4, board.D5, board.D6)
keyboard.row_pins = (board.D7, board.D8, board.D9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# ENCODERS
encoders.pins = ((board.A2, board.A1, board.A0, False),
                 (board.SCK, board.MISO, board.MOSI, False),
                 )

# RGB Stuff
RED = 0
ORANGE = 45
GREEN = 85
CYAN = 125
BLUE = 170
PURPLE = 205
rgb_ext = RGB(pixel_pin=board.D10,
              num_pixels=4,
              hue_default=BLUE,
              sat_default=255, # 0=white/desat, 255=full saturation
              val_default=16,  # Brightness
              )
keyboard.extensions.append(rgb_ext)
keyboard.extensions.append(MediaKeys())
keyboard.debug_enabled = False


# MACROS ROW 3 (UPDATED TO KC.MACRO() AND Delay)
# Original: (KC.LCMD(KC.LALT(KC.LSFT(KC.T))), KC.LCTRL(KC.U))
TERMINAL = KC.MACRO(
    Tap(KC.LCMD(KC.LALT(KC.LSFT(KC.T)))), # Open Terminal (assuming LCMD = GUI)
    Tap(KC.LCTRL(KC.U))                  # Custom terminal command (e.g., clear line)
)

# Original: (KC.LCMD(KC.LALT(KC.ESCAPE)),)
FORCE_QUIT = KC.MACRO(
    Tap(KC.LCMD(KC.LALT(KC.ESCAPE)))     # Force Quit dialog
)

# Original: (KC.LCTRL(KC.LCMD(KC.Q)), KC.MACRO_SLEEP_MS(400), KC.ESCAPE)
LOCK = KC.MACRO(
    Tap(KC.LCTRL(KC.LCMD(KC.Q))),        # Lock Screen
    Delay(400),                          # Wait for system to register lock
    Tap(KC.ESCAPE)                       # Escape (safeguard/clear other apps)
)
#SPEED_UP = KC.RF(KC.RABK, interval=100, timeout=100)  # Youtube change speed faster
#SPEED_DN = KC.RF(KC.LABK, interval=100, timeout=100)  # Youtube change speed slower
SPEED_UP = KC.MACRO(Tap(KC.RABK), Tap(KC.RABK))  # Youtube change speed faster
SPEED_DN = KC.MACRO(Tap(KC.LABK), Tap(KC.LABK))  # Youtube change speed slower

SAT_UP = KC.RF(KC.RGB_SAI)
SAT_DN = KC.RF(KC.RGB_SAD)
RGB_UP = KC.RF(KC.RGB_VAI)
RGB_DN = KC.RF(KC.RGB_VAD)
HUE_UP = KC.RF(KC.RGB_HUI)
HUE_DN = KC.RF(KC.RGB_HUD)

# KEYMAPS
keyboard.keymap = [
    # Layer 0
    [
        TERMINAL, FORCE_QUIT, KC.MEDIA_PLAY_PAUSE, LOCK,
        HUE_UP,   SPEED_DN,   KC.AUDIO_MUTE, SPEED_UP,
        HUE_DN,   KC.LEFT,    KC.SPACE,      KC.RIGHT,
    ]
]

ENC_MAP_VOL = (KC.AUDIO_VOL_DOWN,   # CW = vol down
           KC.AUDIO_VOL_UP,     # CCW = vol up
           KC.AUDIO_MUTE,       # push = mute toggle
           )
ENC_MAP_BRIGHT = (KC.RGB_VAD,  # CW=RGB Bright down
                  KC.RGB_VAI,  # CCW= RGB Bright up
                  KC.RGB_TOG   # Push= RGB on/off
                  )
# Encoder 1 always adjusts volume
# Encoder 2 alwys adjusts background RGB brightness
encoders.map = [(ENC1_MAP_VOL, ENC_MAP_BRIGHT)]


if __name__ == '__main__':
    keyboard.go()

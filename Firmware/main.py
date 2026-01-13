print("Starting")

import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.macros import Macros

from kmk.extensions.display import Display
from kmk.extensions.display.ssd1306 import SSD1306

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP26, board.GP27, board.GP28)
keyboard.row_pins = (board.GP29, board.GP4, board.GP2, board.GP0)
keyboard.diode_orientation = DiodeOrientation.COL2ROW


layers = Layers()
macros = Macros()

keyboard.modules.append(layers)
keyboard.modules.append(macros)


i2c = busio.I2C(board.GP7, board.GP6)

oled = SSD1306(
    i2c=i2c,
    width=128,
    height=32,
    rotation=0,
)

display = Display(
    display=oled,
    width=128,
    height=32,
    brightness=1,
)

keyboard.extensions.append(display)


LAYER_NAMES = {
    0: "BASE",
    1: "APPS",
    2: "ZOOM",
    3: "VSCODE",
}

def draw_layer(oled, layer):
    oled.fill(0)
    oled.text("Reprint", 0, 0, 1)
    oled.text(LAYER_NAMES.get(layer, "???"), 0, 16, 1)
    oled.show()

def on_layer_change(layer):
    draw_layer(oled, layer)

layers.after_layer_change = on_layer_change
draw_layer(oled, 0)


macros.macros = {
    # App Launch 
    "GMAIL": [KC.LGUI, KC.R, "https://mail.google.com", KC.ENTER],
    "CAL":   [KC.LGUI, KC.R, "https://calendar.google.com", KC.ENTER],
    "GIT":   [KC.LGUI, KC.R, "https://github.com", KC.ENTER],
    "JIRA":  [KC.LGUI, KC.R, "https://jira.atlassian.com", KC.ENTER],
    "ZOOM":  [KC.LGUI, KC.R, "zoom", KC.ENTER],
    "SLACK": [KC.LGUI, KC.R, "slack", KC.ENTER],
    "CODE":  [KC.LGUI, KC.R, "code", KC.ENTER],
    "EXP":   [KC.LGUI, KC.E],
    "LOCK":  [KC.LGUI, KC.L],

    # Zoom Controls
    "ZM_MUTE":  [KC.LALT, KC.A],
    "ZM_VIDEO": [KC.LALT, KC.V],
    "ZM_SHARE": [KC.LALT, KC.S],
    "ZM_FOCUS": [KC.LCTRL, KC.LALT, KC.LSHIFT],

    # VS Code
    "VS_CMD":   [KC.LCTRL, KC.LSHIFT, KC.P],
    "VS_OPEN":  [KC.LCTRL, KC.P],
    "VS_TERM":  [KC.LCTRL, KC.GRAVE],
    "VS_SAVE":  [KC.LCTRL, KC.S],
    "VS_FIND":  [KC.LCTRL, KC.F],
    "VS_REPL":  [KC.LCTRL, KC.H],
    "VS_FMT":   [KC.LSHIFT, KC.LALT, KC.F],
}


MO_APPS   = KC.MO(1)
MO_ZOOM   = KC.MO(2)
MO_VSCODE = KC.MO(3)

keyboard.keymap = [
    # Layer 0 — BASE
    [
        KC.A,       KC.B,       KC.C,
        KC.D,       KC.E,       KC.F,
        KC.G,       KC.H,       KC.I,
        MO_APPS,    MO_ZOOM,    MO_VSCODE,
    ],

    # Layer 1 — APPS
    [
        KC.MACRO("GMAIL"), KC.MACRO("CAL"),   KC.MACRO("GIT"),
        KC.MACRO("JIRA"),  KC.MACRO("ZOOM"),  KC.MACRO("SLACK"),
        KC.MACRO("CODE"),  KC.MACRO("EXP"),   KC.NO,
        KC.MACRO("LOCK"),  KC.NO,             KC.NO,
    ],

    # Layer 2 — ZOOM
    [
        KC.MACRO("ZM_MUTE"),  KC.MACRO("ZM_VIDEO"), KC.MACRO("ZM_SHARE"),
        KC.MACRO("ZM_FOCUS"), KC.NO,                KC.NO,
        KC.NO,                KC.NO,                KC.NO,
        KC.MO(0),             KC.NO,                KC.NO,
    ],

    # Layer 3 — VSCODE
    [
        KC.MACRO("VS_CMD"),  KC.MACRO("VS_OPEN"), KC.MACRO("VS_TERM"),
        KC.F12,              KC.MACRO("VS_FIND"), KC.MACRO("VS_REPL"),
        KC.MACRO("VS_SAVE"), KC.MACRO("VS_FMT"),  KC.NO,
        KC.MO(0),            KC.NO,               KC.NO,
    ],
]

if __name__ == "__main__":
    keyboard.go()
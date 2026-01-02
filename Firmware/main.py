import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import MatrixScanner
from kmk.keys import KC
from kmk.extensions.rgb import RGB


# Maak keyboard aan
keyboard = KMKKeyboard()

# Definieer rows en columns
ROW_PINS = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)
COL_PINS = (board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20, board.GP21, board.GP22)

# Matrix scanner instellen
keyboard.matrix = MatrixScanner(
    row_pins=ROW_PINS,
    col_pins=COL_PINS,
    columns_to_anodes=False,  # True als je diodes andersom zitten
)

# Keymap (row-major order!)
keyboard.keymap = [
    [
        # Row 0
        KC.GRAVE, KC.1, KC.2, KC.3, KC.4, KC.5, KC.6, KC.7, KC.8, KC.9, KC.0, KC.MINUS, KC.EQUAL, KC.BSPACE, KC.DELETE

        # Row 1
        KC.KP_7, KC.KP_8, KC.KP_9, KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRACKET, KC.RBRACKET, KC.BSLASH, KC.PGUP

        # Row 2
        KC.KP_4, KC.KP_5, KC.KP_6, KC.LOCKING_CAPS, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCOLON, KC.QUOTE, KC.ENTER, KC.NO, KC.PGDOWN

        # Row 3
        KC.KP_1, KC.KP_2, KC.KP_3, KC.LSHIFT, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLASH, KC.RSHIFT, KC.NO, KC.UP, KC.EncodingWarning

        # Row 4
        KC.KP_0, KC.NO, KC.KP_DOT, KC.LCTRL, KC.LGUI, KC.LALT, KC.NO, KC.NO, KC.SPACE, KC.NO, KC.NO, KC.NO, KC.RALT, KC.RGUI, KC.RCTRL, KC.LEFT, KC.DOWN, KC.RIGHT
    ]
]

rgb = RGB(
    pixel_pin=board.GP28,  # DIN van eerste SK6812
    num_pixels=4,          # 4 LEDs
    hue_default=170,       # blauw/paars
    sat_default=255,
    val_default=80,        # veilige helderheid
)

keyboard.extensions.append(rgb)

# Startkleur groen
current_color = [0, 255, 0]

def set_rgb_color(color):
    global current_color
    for i in range(rgb.num_pixels):
        rgb.pixels[i] = color
    rgb.show()
    current_color = list(color)

def fade_to_color(target_color, steps=20, delay=0.01):
    global current_color
    # Bereken stapgroottes voor R, G, B
    step = [(target_color[i] - current_color[i]) / steps for i in range(3)]
    for s in range(steps):
        new_color = [int(current_color[i] + step[i]*(s+1)) for i in range(3)]
        set_rgb_color(new_color)
        time.sleep(delay)

@keyboard.on_press
def on_key_press(key):
    # Fade naar rood
    fade_to_color([255, 0, 0])

@keyboard.on_release
def on_key_release(key):
    # Fade terug naar groen
    fade_to_color([0, 255, 0])


# Start KMK
if __name__ == '__main__':
    keyboard.go()
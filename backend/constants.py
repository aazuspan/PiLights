# Development mode disables Raspberry Pi-specific libraries and functionality
DEV_MODE = False

if not DEV_MODE:
    import board
    GPIO_PIN = board.D21

else:
    GPIO_PIN = None

PIXEL_COUNT = 151
BRG = (1, 2, 0)
MIN_BRIGHTNESS = 1
MAX_BRIGHTNESS = 255
VIS_DIR = 'visualizations'

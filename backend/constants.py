# Development mode disables Raspberry Pi-specific libraries and functionality
DEV_MODE = False
# Use this setting to skip Wemo discovery. Only use this during development.
IGNORE_WEMOS = True

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

# GENERAL
HEIGHT = 900
WIDTH = 875
APP_NAME = "CeX Price Checker"
DEFAULT_PADDING = 20

# STYLES
FONT = 'Calibri'
H1_STYLES = "24 bold"
H2_STYLES = '16 bold'
TAG_STYLES = '10 bold'

CONDITION_BASED_CATEGORIES = {
    'Games': {
        'Nintendo 64': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Mint', 'Mint')),
        'SNES': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Mint', 'Mint')),
        'PlayStation 1': (('Boxed', 'Boxed'), ('Mint', 'Mint')),
    },
    'Consoles': {
        'Nintendo 3DS': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Nintendo 64': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Nintendo DS': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Nintendo GameCube': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Nintendo Switch': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Nintendo Wii': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Nintendo Wii U':(('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'PlayStation 1': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'PlayStation 2': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'PlayStation 3': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'PlayStation 4': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'PlayStation 5': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'PS Vita': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'PSP': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'SNES': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Xbox': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Xbox 360': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Xbox One': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
        'Xbox Series X': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted')),
    }
}

# RESULTS BOX
TAG_WRAPLENGTH = 90
CONTENT_WRAPLENGTH = 230
RESULTS_TAG_MIN_WIDTH = 110
RESULTS_CONTENT_MIN_WIDTH = 210
RESULTS_IMAGE_MAX_HEIGHT = 175
RESULTS_IMAGE_MAX_WIDTH = 340
DEFAULT_CEX_CONTENT = {
    "Game Title:" : "-",
    "Platform:" : "-",
    "Sell Price (Cash):" : "-",
    "Sell Price (Voucher):" : "-",
    "Buy Price:" : "-",
    "In Stock:": "-",
    "URL:" : "-",
}

# SCROLL LIST
SCROLL_LIST_WIDTH = 380
ITEM_IMAGE_MAX_HEIGHT = 125
ITEM_IMAGE_MAX_WIDTH = 100
ITEM_WRAPLENGTH = 140
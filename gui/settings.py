# GENERAL
HEIGHT = 900
WIDTH = 925
APP_NAME = "CeX Price Checker"
DEFAULT_PADDING = 20

# STYLES
FONT = 'Calibri'
H1_STYLES = "24 bold"
H2_STYLES = '16 bold'
TAG_STYLES = '10 bold'

CONDITION_BASED_CATEGORIES = {
    'Games': {
        'Gameboy Advance': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Mint', 'Mint'), ('None', 'None')),
        'Nintendo 64': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Mint', 'Mint'), ('None', 'None')),
        'SNES': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Mint', 'Mint'), ('None', 'None')),
        'PlayStation 1': (('Boxed', 'Boxed'), ('Mint', 'Mint'), ('None', 'None')),
    },
    'Consoles': {
        'Nintendo 3DS': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Nintendo 64': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Nintendo DS': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Nintendo GameCube': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Nintendo Switch': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Nintendo Wii': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Nintendo Wii U':(('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'PlayStation 1': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'PlayStation 2': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'PlayStation 3': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'PlayStation 4': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'PlayStation 5': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'PS Vita': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'PSP': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'SNES': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Xbox': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Xbox 360': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Xbox One': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
        'Xbox Series X': (('Boxed', 'Boxed'), ('Unboxed', 'Unboxed'), ('Discounted', 'Discounted'), ('None', 'None')),
    },
    'Phones': {
        'Android': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'iPhone': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Windows': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Vodafone': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Meteor': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        '3': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'eMobile': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Tesco': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Other': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
    },
    'Computing': {
        'Desktops': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Graphics, Sound & Capture Cards': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Handheld Gaming PCs': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Laptops': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Networking': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Peripherals': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Tablets': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
    },
    'Electronics': {
        'Wearables': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Smart Technology': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Health & Beauty': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Robots and Automation': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'eBook Readers': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Media Devices': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'TVs, Monitors & Projectors': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Cameras & Photography': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Accessories': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Headphones & Earphones': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'DAB & Internet Radios': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
        'Sat Nav & GPS Units': (('A', 'A'), ('B', 'B'), ('C', 'C'), ('None', 'None')),
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
    "Category:" : "-",
    "Sell Price (Cash):" : "-",
    "Sell Price (Voucher):" : "-",
    "Buy Price:" : "-",
    "In Stock:": "-",
    "URL:" : "-",
}

# SCROLL LIST
SCROLL_LIST_WIDTH = 360
SCROLLBAR_WIDTH = 17
ITEM_IMAGE_MAX_HEIGHT = 125
ITEM_IMAGE_MAX_WIDTH = 100
ITEM_WRAPLENGTH = 144
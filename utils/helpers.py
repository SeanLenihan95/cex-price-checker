import PIL
import requests
from io import BytesIO
from functools import lru_cache

### IMAGE HELPERS ###
    
def convert_PIL_to_tk(image):
    if isinstance(image, PIL.Image.Image):
        return PIL.ImageTk.PhotoImage(image)

@lru_cache(maxsize=None)
def get_image_from_url(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return
    
    image = PIL.Image.open(BytesIO(response.content))
    return image

### FORMATTING HELPERS ###
    
@lru_cache(maxsize=None)
def prettify_platform(input_platform:str) -> str:
    platform = input_platform.lower()

    if 'dvd' in platform:
        return 'DVD'
    if 'blu-ray' in platform:
        return 'Blu-Ray'
    
    forbidden_words = ['games', 'software', 'pal', 'jp', 'nintendo', 'sega', 'consoles', 'accessories']
    platform = ' '.join([word for word in platform.split(' ') if word not in forbidden_words])
        
    match (platform):
        case 'playstation 5' | 'ps5' | 'playstation5':
            platform = 'PlayStation 5'
        case 'playstation 4' | 'ps4' | 'playstation4':
            platform = 'PlayStation 4'
        case 'playstation 3' | 'ps3' | 'playstation3':
            platform = 'PlayStation 3'
        case 'playstation 2' | 'ps2' | 'playstation2':
            platform = 'PlayStation 2'
        case 'playstation' | 'playstation 1' | 'ps1' | 'playstation1':
            platform = 'PlayStation 1'
        case 'playstation portable' | 'psp':
            platform = 'PSP'
        case 'playstation vita' | 'vita' | 'ps vita':
            platform = 'PS Vita'
        case 'original xbox' | 'xbox':
            platform = 'Xbox' 
        case '360' | 'xbox 360':
            platform = 'Xbox 360' 
        case 'xb1' | 'xbox one':
            platform = 'Xbox One'
        case 'xbsx' | 'xbox series x' | 'xbox series':
            platform = 'Xbox Series X'
        case 'gamecube':
            platform = 'Nintendo GameCube'
        case 'wii':
            platform = 'Nintendo Wii'
        case 'wii u':
            platform = 'Nintendo Wii U'
        case 'ds':
            platform = 'Nintendo DS'
        case '3ds':
            platform = 'Nintendo 3DS'
        case 'switch':
            platform = 'Nintendo Switch'
        case '64' | 'n64':
            platform = 'Nintendo 64'
        case 'pc' | 'pc games':
            platform = 'PC'
        case 'snes' | 'super' | 'super nes' | 'super nintendo entertainment system':
            platform = 'SNES'
        case 'skylanders':
            platform = 'Skylanders'
        case 'disney infinity':
            platform = 'Disney Infinity'
        case 'amiibo' | 'amibo':
            platform = 'Amiibo'
        case 'lego dimensions':
            platform = 'LEGO Dimensions'
        case 'dvd' | 'feature films':
            platform = 'DVD'
        case 'blu-ray' | 'blu ray' | '4k' | '4k ultra' | '4k hd' | '4k hd ultra':
            platform = 'Blu-Ray / 4K'
        case _:
            platform = input_platform

    return platform

def format_currency(amount):
    amount = max(round(float(amount), 2), 0)
    amount = '{:.2f}'.format(amount)
    return '€' + amount
import requests
import json
from functools import lru_cache

from utils.helpers import *
from .get_similarity_score import *

class CeXChecker():
    def __init__(self):
        self.categories = {
            'Games': {
                'Gameboy Advance': ('Gameboy Advance Software',),
                'Nintendo 3DS': ('3DS Games',), 
                'Nintendo 64': ('Nintendo 64 Software',),
                'Nintendo DS': ('Nintendo DS Games',),
                'Nintendo GameCube': ('GameCube Games',),
                'Nintendo Switch': ('Switch Software',), 
                'Nintendo Wii': ('Wii Games',), 
                'Nintendo Wii U': ('Wii U Games',),
                'PC': ('PC Games',),
                'PlayStation 1': ('Playstation1 Software',), 
                'PlayStation 2': ('Playstation2 Games',), 
                'PlayStation 3': ('Playstation3 Games',), 
                'PlayStation 4': ('Playstation4 Games',), 
                'PlayStation 5': ('Playstation5 Games',), 
                'PS Vita': ('PS Vita Games',),
                'PSP': ('PSP Games', 'PSP UMD Movies',),
                'SNES': ('Super NES Software',),
                'Xbox': ('Xbox Games',),
                'Xbox 360': ('Xbox 360 Games',),
                'Xbox One': ('Xbox One Games', 'Xbox Smart Delivery Games'),
                'Xbox Series X': ('Xbox Series Games', 'Xbox Smart Delivery Games',),
            },
            'Consoles': {
                'Gameboy Advance': ('Gameboy Advance Console',),
                'Nintendo 3DS': ('3DS Consoles',),
                'Nintendo 64': ('Nintendo 64 Consoles',),
                'Nintendo DS': ('Nintendo DS Consoles',),
                'Nintendo GameCube': ('GameCube Consoles',),
                'Nintendo Switch': ('Switch Consoles',),
                'Nintendo Wii': ('Wii Consoles',),
                'Nintendo Wii U': ('Wii U Consoles',),
                'PlayStation 1': ('Playstation1 Consoles',),
                'PlayStation 2': ('Playstation2 Consoles',),
                'PlayStation 3': ('Playstation3 Consoles',),
                'PlayStation 4': ('Playstation4 Consoles',),
                'PlayStation 5': ('Playstation5 Consoles',),
                'PS Vita': ('PS Vita Consoles',),
                'PSP': ('PSP Consoles',),
                'SNES': ('Super NES Consoles',),
                'Xbox': ('Xbox Consoles',),
                'Xbox 360': ('Xbox 360 Consoles',),
                'Xbox One': ('Xbox One Consoles',),
                'Xbox Series X': ('Xbox Series Consoles',)
            },
            'Accessories': {
                'Gameboy Advance': ('Gameboy Advance Accessories',),
                'Nintendo 3DS': ('3DS Accessories',),
                'Nintendo 64': ('Nintendo 64 Accessories',),
                'Nintendo DS': ('Nintendo DS Accessories',),
                'Nintendo GameCube': ('GameCube Accessories',),
                'Nintendo Switch': ('Switch Accessories',),
                'Nintendo Wii': ('Wii Accessories',),
                'Nintendo Wii U': ('Wii U Accessories',),
                'PlayStation 1': ('Playstation1 Accessories',),
                'PlayStation 2': ('Playstation2 Accessories',),
                'PlayStation 3': ('Playstation3 Accessories',),
                'PlayStation 4': ('Playstation4 Accessories',),
                'PlayStation 5': ('Playstation5 Accessories',),
                'PS Vita': ('PS Vita Accessories',),
                'PSP': ('PSP Accessories',),
                'SNES': ('Super NES Accessories',),
                'Xbox': ('Xbox Accessories',),
                'Xbox 360': ('Xbox 360 Accessories',),
                'Xbox One': ('Xbox One Accessories',),
                'Xbox Series X': ('Xbox Series Accessories',)
            },
            'DVD & Blu-Ray': {
                'DVDs': ('DVD Movies €1', 'Feature Films', 'DVD Anime', 'DVD Music €1', 'DVD Sport €1', 'DVD TV & Documentary', 'DVD World Cinema', 'DVD World Cinema €1', 'DVD Adult', 'DVD Music', 'DVD Sport', 'DVD TV €1'),
                'Blu-Rays': ('Blu-Ray Movies', 'Blu-Ray TV & Documentary', 'Blu-Ray World Cinema', 'Blu-Ray Music', 'Blu-Ray Sports'),
                '4K': ('Blu-Ray Movies', 'Blu-Ray TV & Documentary', 'Blu-Ray World Cinema', 'Blu-Ray Music', 'Blu-Ray Sports'),
                'DVD Players': ('DVD-RW Drives', 'Portable DVD Players'),
                'Blu-Ray Players': ('Blu-Ray Players', 'Blu-Ray Drives'),
            },
            'Figures': {
                'Amiibo': ('NFC Figures',),
                'Disney Infinity': ('NFC Figures',),
                'LEGO Dimensions': ('NFC Figures',),
                'Skylanders': ('NFC Figures',),
            },
            'Phones': {
                'Android': ('Phones Android',),
                'iPhones': ('Phones - iPhones',),
                'Windows': ('Phones Windows Phone',),
                'Vodafone': ('Phones - Vodafone',),
                'Meteor': ('Phones - Meteor',),
                '3': ('Phones - 3',),
                'eMobile': ('Phones - eMobile',),
                'Tesco': ('Phones - Tesco',),
                'Non-Working': ('Phones iPhone Non Working', 'Non-working Phones'),
                'Mobile Broadband': ('Mobile Broadband',),
                'Accessories': ('Apple iPhone Accessories', 'CeX basics - Phone Accessories', 'Phone Accessories',),
                'Other': ('Phones - Unlocked',),
            },
            'Computing': {
                'Data Storage': ('Solid State Hard Drives (SSD)', 'USB Flash Drives', 'USB External Hard Drives', 'SATA Hard Drives', 'IDE Hard Drives', '2.5 Inch Laptop Hard Drives', 'Network Attached Hard Drives'),
                'Desktops': ('Desktops - Apple Mac', 'Desktops - Windows', 'Desktops - Other OS'),
                'Graphics, Sound & Capture Cards': ('Capture Cards', 'TV Tuner Cards & Adaptors', 'PCI-Express Graphics Cards'),
                'Handheld Gaming PCs': ('Handheld Gaming PCs',),
                'Internal Memory': ('DDR2 - Desktop 240 Pin', 'DDR3 - Desktop 240 Pin', 'DDR2 - Laptop 200 Pin', 'DDR3 - Laptop 204 Pin', 'Memory - Desktop DDR4', 'Memory - Laptop DDR4', 'DDR5 - Laptop 262 Pin', 'DDR5 - Desktop 288pin'),
                'Laptops': ('Laptops - Apple Mac', 'Laptops - Windows', 'Laptops - Other OS'),
                'Networking': ('Wireless Cards & Adaptors', 'Wireless Routers'),
                'Peripherals': ('PC Accessories', 'PC Speakers', 'PC Mice', 'PC Keyboards', 'PC Headsets', 'PC Gaming Controllers'),
                'Processors': ('AMD Processors', 'Intel Processors'),
                'Software': ('Apple Software', 'Microsoft Software'),
                'Tablets': ('Apple iPad', 'Tablets - Blackberry', 'Tablet Accessories', 'Tablets - Android', 'Tablets - Windows')
            },
            'Electronics': {
                'Wearables': ('Wearables - Activity Trackers', 'Wearables - Smartwatches', 'Wearables - Hybrid Smartwatches'),
                'Smart Technology': ('Smart Lighting', 'Smart Security', 'Smart Home Monitoring', 'Smart Assistant', 'Smart Accessories'),
                'Miscellaneous': ('E-Book Readers', 'Home Automation', 'Robots', 'Robot Vacuum', 'Baby Monitor', 'Health Monitors')
            }
        }
    
    @lru_cache(maxsize=None)
    def search(self, title:str, category:str, subcategory:str, condition:str):
        if category not in self.categories or subcategory not in self.categories[category]:
            return
        
        self.title = title
        self.condition = condition

        results = self.make_request(title, category, subcategory)
        if not results:
            return
        
        self.print_results(results)

        sorted_results = self.sort_results(results)
        
        return [self.extract_details(result) for result in sorted_results]
    
    def make_request(self, title, category, subcategory):        
        search_space = self.categories[category][subcategory]
        search_term = f'{title} {subcategory}' if subcategory in {'4K', 'Skylanders', 'Amiibo', 'Disney Infinity', 'LEGO Dimensions'} else title
        
        url = 'https://lnnfeewzva-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.41.1)%3B%20Vue%20(2.6.14)%3B%20Vue%20InstantSearch%20(4.3.3)%3B%20JS%20Helper%20(3.8.2)&x-algolia-api-key=07aa231df2da5ac18bd9b1385546e963&x-algolia-application-id=LNNFEEWZVA'
        
        payload = {
            'requests': [
                {
                    'indexName': 'prod_cex_ie',
                    'query': search_term,
                    'facetFilters': [[f'categoryFriendlyName:{category}' for category in search_space]]
                }
            ]
        }
        response = requests.post(url=url, data=json.dumps(payload))

        try:
            if response.status_code == 200:
                response_json = json.loads(response.text)
                result = response_json['results'][0]['hits']

                return result
            else:
                # Raise an exception for non-200 status codes
                response.raise_for_status()
        
        except Exception as e:
            print(f'Error occured at make_request():\n{e}')
        
    def sort_results(self, results):
        def custom_sort(result):
            title = result['boxName']
            similarity_score = result['similarity_score']

            if self.condition:
                condition_keywords = ('Mint', 'Boxed', 'Unboxed', 'Discounted', 'A', 'B', 'C')
            
                condition = next((keyword for keyword in (title.split(' ')[-1], title.split('/')[-1]) if keyword in condition_keywords), None)
                
                if condition and condition == self.condition:
                    return (1, similarity_score)
            
            return (0, similarity_score)

        # remove all discontinued results
        results = [result for result in results if not result['discontinued']]
        
        # add similarity score to result
        for result in results:
            similarity_score = get_similarity_score(result['boxName'], self.title)
            result['similarity_score'] = similarity_score

        return sorted(results, key=custom_sort, reverse=True)

    def extract_details(self, result):
        return {
            'title': result['boxName'],
            'sim_score': result['similarity_score'],
            'platform': prettify_platform(result['categoryFriendlyName']),
            'sell_price_cash': result['cashPriceCalculated'],
            'sell_price_voucher': result['exchangePriceCalculated'],
            'buy_price': result['sellPrice'],
            'ean': result['boxId'],
            'image': result['imageUrls']['large'].replace(' ', '%20'),
            'is_in_stock': bool(result['availability']),
            'url': 'https://ie.webuy.com/product-detail?id=' + result['boxId'],
        }
    
    def get_supported_categories(self):
        return {key: list(self.categories[key].keys()) for key in self.categories.keys()}
    
    def print_results(self, results):
        print(f'Hits: {len(results)}')
        for result in results:
            print(f'Name: {result["boxName"]}')
            print(f'Platform: {prettify_platform(result["categoryFriendlyName"])}')
            print(f'Discontinued: {bool(result["discontinued"])}')
            print(f'Available: {bool(result["availability"])}')
            print()
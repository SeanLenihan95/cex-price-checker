import requests
import json
from functools import lru_cache

from utils.helpers import *
from .get_similarity_score import *

class CeXChecker():
    def __init__(self):
        self.categories = {
            'Games': {
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
                'PS Vita': ('PS Vita Games', 'PS Vita Consoles',),
                'PSP': ('PSP Games', 'PSP UMD Movies', 'PSP Consoles',),
                'SNES': ('Super NES Software', 'Super NES Consoles',),
                'Xbox': ('Xbox Consoles',),
                'Xbox 360': ('Xbox 360 Consoles',),
                'Xbox One': ('Xbox One Consoles',),
                'Xbox Series X': ('Xbox Series Consoles',)
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
            }
        }
        self.supported_categories = {key: list(self.categories[key].keys()) for key in self.categories.keys()}
    
    @lru_cache(maxsize=None)
    def search(self, title:str, category:str, subcategory:str, condition:str):
        if category not in self.categories or subcategory not in self.categories[category]:
            return
        
        self.title = title
        self.condition = condition

        results = self.make_request(title, category, subcategory)
        if not results:
            return
        
        # self.print_results(results)

        results_sorted = self.sort_results(results)
        
        return [self.extract_game_details(result_and_score) for result_and_score in results_sorted]
    
    def make_request(self, title, category, subcategory):        
        search_space = self.categories[category][subcategory]
        include_subcategory_in_search = {'4K', 'Skylanders', 'Amiibo', 'Disney Infinity', 'LEGO Dimensions'}
        search_term = f'{title} {subcategory}' if subcategory in include_subcategory_in_search else title
        
        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '896',
            'DNT': '1',
            'Host': 'lnnfeewzva-dsn.algolia.net',
            'Origin': 'https://ie.webuy.com',
            'Pragma': 'no-cache',
            'Referer': 'https://ie.webuy.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': 'Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"
        }

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
        response = requests.post(url=url, headers=header, data=json.dumps(payload))

        try:
            if response.status_code == 200:
                response_json = json.loads(response.text)
                result = response_json['results'][0]['hits']

                return result
            else:
                # Raise an exception for non-200 status codes
                response.raise_for_status()
        
        except Exception as e:
            print(f'Error occured at search():\n{e}')
        
    def sort_results(self, results):
        def custom_sort(result_and_score):
            result, similarity_score = result_and_score
            title = result['boxName']

            if self.condition:
                condition_keywords = ('Mint', 'Boxed', 'Unboxed', 'Discounted', 'A', 'B', 'C')
            
                if title.split(' ')[-1] in condition_keywords and self.condition != title.split(' ')[-1]:
                    return (0, similarity_score)
            
            return (1, similarity_score)

        results_and_scores = [(result, get_similarity_score(result['boxName'], self.title)) for result in results if not result['discontinued']]
    
        return sorted(results_and_scores, key=custom_sort, reverse=True)

    def extract_game_details(self, result_and_score):
        result, similarity_score = result_and_score

        title = result['boxName']
        sell_price_cash = result['cashPriceCalculated']
        sell_price_voucher = result['exchangePriceCalculated']
        buy_price = result['sellPrice']
        ean = result['boxId']
        image = result['imageUrls']['large'].replace(' ', '%20')
        is_in_stock = bool(result['availability'])
        
        platform = prettify_platform(result['categoryFriendlyName'])

        return {
            'title': title,
            'sim_score': similarity_score,
            'platform': platform,
            'sell_price_cash': sell_price_cash,
            'sell_price_voucher': sell_price_voucher,
            'buy_price': buy_price,
            'ean': ean,
            'image': image,
            'is_in_stock': is_in_stock,
            'url': 'https://ie.webuy.com/product-detail?id=' + ean,
        }
    
    def get_supported_categories(self):
        return self.supported_categories
    
    def print_results(self, results):
        print(f'Hits: {len(results)}')
        for result in results:
            print(f'Name: {result["boxName"]}')
            print(f'Platform: {prettify_platform(result["categoryFriendlyName"])}')
            print(f'Discontinued: {bool(result["discontinued"])}')
            print(f'Available: {bool(result["availability"])}')
            print()
    
# cpc = CeXChecker()
# results = cpc.search(title='God of War', 
#                      platform=prettify_platform('PS4'), 
#                      condition='Boxed')

# if not results:
#     print('NO RESULT FOUND')
# else:
#     for result in results:
#         print(f'RESULT {results.index(result) + 1} OF {len(results)}')
#         print(f'Title: {result["title"]}')
#         print(f'Platform: {result["platform"]}')
#         print(f'Sell Price (Cash): {result["sell_price_cash"]}')
#         print(f'Sell Price (Voucher): {result["sell_price_voucher"]}')
#         print(f'Buy Price: {result["buy_price"]}')
#         print(f'Similarity Score: {round(100 * result["sim_score"], 2)}%')
#         print(f'Image URL: {result["image"]}\n')
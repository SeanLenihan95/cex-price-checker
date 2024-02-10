from difflib import SequenceMatcher
import re
from word2number import w2n
import roman

YEAR_THRESHOLD = 1900
NUMBER_MISMATCH_PENALTY = 0.25
EDITION_MISMATCH_PENALTY = 0.5
FORBIDDEN_TERMS = {'Mint', 'Boxed', 'Unboxed', 'w/Manual', 'No DLC', 'The Official Videogame', 'The Videogame', 'The Game'}

def get_similarity_score(a: str, b: str):
    def word_to_num(word:str):
        try:
            return str(w2n.word_to_num(word))
        except:
            return word
        
    def roman_to_num(word:str):
        try:
            return str(roman.fromRoman(word))
        except:
            return word
        
    def remove_words_in_brackets(a_str:str):
        pattern = re.compile(r'\([^)]*\)')
        
        # remove any words in brackets
        result = re.sub(pattern, '', a_str)
        
        # remove any double spaces
        result = re.sub(r'\s+', ' ', result)
        
        return result
        
    def preprocess_string(string:str):
        # remove forbidden words
        for term in FORBIDDEN_TERMS:
            string = string.replace(term, '').strip()

        # remove any words in brackets
        string = remove_words_in_brackets(string)

        # capitalise and strip leading whitespace
        string = string.upper().strip()

        # replace '2K' with '20', hyphens with spaces, and 'Ed.' with 'Edition'
        string = string.replace('2K', '20')
        string = string.replace('-', ' ')
        string = string.replace('ED.', 'EDITION')

        # remove all non-alphanumeric characters
        string = re.sub(r'[^a-zA-Z0-9 ]', '', string)

        # convert Roman numerals / written numbers into digital equivalents
        string = ' '.join([word_to_num(roman_to_num(word)) for word in string.split(' ')])

        return string

    def numbers_mismatch(a, b):
        # return True if there are any non-year numbers in the differences between a and b
        differences = (set(a.split(' ')).symmetric_difference(set(b.split(' '))))
        return any(word.isnumeric() and int(word) < YEAR_THRESHOLD for word in differences)

    def editions_mismatch(a, b):
        if ('EDITION' not in a and 'EDITION' not in b):
            return False
        
        if ('EDITION' in a and 'EDITION' not in b) or ('EDITION' in b and 'EDITION' not in a):
            return True

        word_before_a = a.split(' ')[a.split(' ').index('EDITION') - 1]
        word_before_b = b.split(' ')[b.split(' ').index('EDITION') - 1]

        return word_before_a != word_before_b

    a, b = preprocess_string(a), preprocess_string(b)
            
    if numbers_mismatch(a, b):
        return SequenceMatcher(None, a, b).ratio() * NUMBER_MISMATCH_PENALTY
        
    if editions_mismatch(a, b):
        return SequenceMatcher(None, a, b).ratio() * EDITION_MISMATCH_PENALTY
    
    return SequenceMatcher(None, a, b).ratio()

# print(get_similarity_score('Spyro: Year of the Dragon, Platinum Ed., Boxed', 
#                            'Crash'))
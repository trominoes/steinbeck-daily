import requests
from bs4 import BeautifulSoup
import json
import time
import random
import re


BASE_URL = 'https://www.goodreads.com/author/quotes/585.John_Steinbeck?page={}'
EXCEPTIONS = ['a', 'an', 'the', 'in', 'on', 'of', 'for', 'with', 'and', 'but', 'or']

# Mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

ENGLISH_PATTERN = re.compile(r'^[a-zA-Z0-9\s,.\'?!;:—“”‘’]*$')
CHAR_MIN = 20
CHAR_MAX = 500

def compile_quotes_on_page(n):
    '''Returns a list of all quotes and book sources on page n of the BASE_URL'''
    url = BASE_URL.format(n)
    quotes_and_sources = []
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all divs with class 'quoteText' (where quotes are stored)
        quote_elements = soup.find_all('div', class_='quoteText')

        # Loop through each quote and append to list
        for quote in quote_elements:
            cleaned_quote = quote.get_text(strip=True)
            if '―John' in cleaned_quote:
                quote_text, aux_text = cleaned_quote.split('―John', 1)
                # Checks that source is listed, quote is of suitable length, contains only alphabet
                if 'Steinbeck,' in aux_text:
                    if len(quote_text) <= CHAR_MAX and len(quote_text) >= CHAR_MIN:
                        if ENGLISH_PATTERN.match(quote_text):
                            # Correct capitalizations for quote and source
                            book_name = aux_text.split(',')[1].strip()
                            book_name = title_case(book_name, EXCEPTIONS)
                            quotes_and_sources.append((capitalize_quote(quote_text).strip(), book_name))

        return quotes_and_sources
    else:
        print(f"Failed to retrieve page {n}. Status code: {response.status_code}")

def sources_on_list(quote_list):
    '''Returns a list of all unique sources present in the given quote_list'''
    sources = []
    for quote in quote_list:
        if quote[1] not in sources:
            sources.append(quote[1])

    return sources

def accept_quotes_with_source(quote_list, source):
    '''Returns a list of quotes within quote_list which match source'''
    quotes = []
    for quote in quote_list:
        if quote[1] == source:
            quotes.append(quote)

    return quotes


def accept_quotes_with_sources(quote_list, source_list):
    '''Returns a list of quotes within quote_list which match a source in source_list'''
    quotes = []
    for quote in quote_list:
        if quote[1] in source_list:
            quotes.append(quote)

    return quotes

def compile_all_pages():
    '''Compiles quote list for all pages'''
    PAGES = 100
    full_list = []
    for i in range(1, PAGES+1):
        full_list.extend(compile_quotes_on_page(i))
        delay = random.uniform(3, 5)
        print(f"Finished scraping page {i}. Waiting for {delay:.2f} seconds...")
        time.sleep(delay)

    return full_list

def save_to_json(quotes_and_sources, filename):
    '''Saves a given list of quotes and sources to json with filename'''
    with open(f"static/{filename}.json", "w", encoding="utf-8") as f:
        json.dump(
            [{"quote": q, "book": b} for q, b in quotes_and_sources],
            f,
            ensure_ascii=False,
            indent=2
        )

def capitalize_quote(s):
    '''Capitalizes a quote (second char, to skip the quotation mark)'''
    new_string = s[0] + s[1].upper() + s[2:]
    return new_string

def title_case(s, exceptions):
    '''Converts a string to title case, except for specified exceptions.'''
    # Handle titles with colon
    s = s.split(':')[0]
    word_list = s.split(' ')
    
    # Always capitalize first word
    final = [word_list[0].capitalize()]
    
    for word in word_list[1:]:
        # Keep other words lowercase if it is in the exceptions list
        if word.lower() in [e.lower() for e in exceptions]:
            final.append(word.lower())
        elif word.lower() == "iv":
            final.append("IV")
        else:
            final.append(word.capitalize())
            
    title_cased = " ".join(final)
    # Handle grapes of wrath special case
    if title_cased == 'Grapes of Wrath':
        return 'The Grapes of Wrath'
    else: 
        return title_cased


#quotes_and_sources = compile_quotes_on_page(1)
#print(len(quotes_and_sources))

quotes_and_sources = compile_all_pages()
#print(sources_on_list(quotes_and_sources))

accepted_books = ['The Winter of Our Discontent', 'East of Eden', 'Of Mice and Men', 
                  'The Grapes of Wrath', 'Travels with Charley', 'Cannery Row', 'Sweet Thursday', 
                  'The Log From the Sea of Cortez', 'The Pearl', 'The Pastures of Heaven', 
                  'The Acts of King Arthur and His Noble Knights', 'Tortilla Flat', 'The Moon Is Down', 
                  'To a God Unknown', 'Once There Was a War', 'In Dubious Battle', 'Cup of Gold', 
                  'The Red Pony', 'The Wayward Bus', 'A Russian Journal', 'Burning Bright', 
                  'Flight', 'A Life in Letters', 'The Long Valley', 'The Short Reign of Pippin IV', 
                  'America and Americans']

save_to_json(accept_quotes_with_sources(quotes_and_sources, accepted_books), "all_quotes")

with open(f"static/book_titles.json", "w", encoding="utf-8") as f:
    json.dump(accepted_books, f)


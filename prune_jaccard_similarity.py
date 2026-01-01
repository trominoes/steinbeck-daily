import json


def jaccard_similarity(quote1, quote2):
    '''Uses Jaccard similarity to compare quote1 and quote2 text'''
    # Split quotes into words and convert to sets
    words1 = set(quote1.lower().split())
    words2 = set(quote2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union


with open(f"static/all_quotes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)

    # Define a threshold for similarity (0 to 1)
    similarity_threshold = 0.8 

    filtered_quotes = []
    duplicate_quotes = []

    # Track removed quotes' indices
    removed_indices = set()

    # Loop through each quote and compare to others
    for i, quote1 in enumerate(quotes_data):
        if i in removed_indices:
            continue 
        
        quote1_text = quote1['quote']
        
        for j in range(i + 1, len(quotes_data)):
            if j in removed_indices:
                continue 
            
            quote2 = quotes_data[j]
            quote2_text = quote2['quote']
            
            similarity = jaccard_similarity(quote1_text, quote2_text)
            if similarity >= similarity_threshold:
                duplicate_quotes.append((quote1_text,quote2_text))
                # If the quotes are similar, keep shorter one 
                if len(quote1_text) > len(quote2_text):
                    removed_indices.add(i) 
                else:
                    removed_indices.add(j) 
                    
        # Store all filtered quotes
        if i not in removed_indices:
            filtered_quotes.append((quote1['quote'], quote1['book']))
    
    # Print the removed pairs
    for pair in duplicate_quotes:
        print(pair)

    print(f"Number of quotes before deduplication: {len(quotes_data)}")
    print(f"Number of quotes after deduplication: {len(filtered_quotes)}")

with open(f"static/all_quotes_filtered.json", "w", encoding="utf-8") as f:
        json.dump(
            [{"quote": q, "book": b} for q, b in filtered_quotes],
            f,
            ensure_ascii=False,
            indent=2
        )

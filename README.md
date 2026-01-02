# steinbeck-daily
Steinbeck Daily is a project that displays a unique quote from the works of John Steinbeck every day. The quotes are curated from Goodreads, with some filtering applied to ensure quality.
## Features:
- A new quote is displayed every day at https://trominoes.github.io/steinbeck-daily!
- Quotes are scraped from Goodreads in `scrape_quotes.py` and lightly filtered (character limits, accepted book sources, alphabetic characters only)
- Jaccard similarity is used in `prune_jaccard_similarity.py` to remove highly similar quotes to promote uniqueness
- Quotes are shuffled and selected based on a reference date (01-01-2026) to ensure randomness
## Statistics:
- 4778 quotes originally listed on Goodreads
- 1440 quotes after filtering (e.g. character limits, valid book sources)
- 1362 quotes after Jaccard similarity pruning
- 1357 quotes after manual removal of quotes with offensive language
This curated set offers about 3 years and 9 months of unique Steinbeck quotes. The `all_quotes_filtered.json` file contains the randomly shuffled final set of quotes.
## Website
Find today's Steinbeck quote at https://trominoes.github.io/steinbeck-daily. 
I opted for a simple interface for a simple project - some nifty animations and font selection on load, but I wanted to keep things lightweight and non-distracting. I initially used Tailwind CSS to accelerate the styling process, but I found that for certain features, vanilla CSS provided more control over the design. I used a hybrid approach to get the best of both worlds.
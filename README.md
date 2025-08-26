<div id="top"></div>
<div align="center">
  <h1 align="center">News Aggregator</h1>
</div>

A simple Python-based news aggregator that fetches the latest articles from multiple newspapers using their RSS feeds and appends them to a CSV file for easy storage and analysis.
  <br>

## Features :
- Fetch articles from one or multiple RSS feed URLs.
- Extract key details like title, link, publication date, authors, tags, article content and image.
- Store results in a CSV file.
- Automatically appends new articles while avoiding duplicates.
- Lightweight and easy to extend.


<!-- GETTING STARTED -->
## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/sarrarmohcin/googleMapsScraper.git
   ```
2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

1. Add your RSS feed URLs to newspapers.json
```
[
  {
    "name": "New York Times",
    "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
  },
  {
    "name": "France 24",
    "url": "https://www.france24.com/en/rss"
  },
  {
    "name": "NBC News",
    "url": "https://www.nbcnews.com/feed"
  }
]

```


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Demo

[![IMAGE ALT TEXT](http://img.youtube.com/vi/KXWTdC9wPD8/0.jpg)](http://www.youtube.com/watch?v=KXWTdC9wPD8 "Watch Demo")


# Chatzy Logger
A simple (and slow) scraper to pull logs from Chatzy for offline access.
It records the full HTML for each page of logs (only the logs;
it does not record the sidebars).wNo CSS or JavaScript is included,
so a bit of further work is required to make the page display nicely.

As is the nature of page scraping, this scraper may break at any time if Chatzy
makes changes to their UI.

## Usage
`git clone` this repository

Add a directory to the root of this repo called `logs`.

Set up Python and pip. Plenty of tutorials on the internet on how to do that,
so I won't include one here.

```pip install -r requirements.txt```

Make a `config.ini` file using `config.ini.sample` as a guideline.

Download a Selenium WebDriver of your choice and put it in your PATH.
Out of the box, this scraper supports Chrome, Firefox, and Opera through the
`config.ini` file. If you use a different WebDriver,
just make the appropriate change in the code.

Let 'er rip.
```python scraper.py```

# Parser
This parser uses BeautifulSoup to parse the raw scraped logs into JSONL,
with one line in Chatzy translating to one JSON format object.

## Usage
Make sure all your logs are in the `logs` folder. Make an empty folder `parsed_logs` in the repo root.

```python parser.py```

## JSON fields
* `t`: "type", the class assigned to the line in Chatzy. "a" seems to be
the standard message, "b" are non-dialogue messages, and "c" are long-form or
block-type messages. `<div class="c">` content is marked as type `div`, and
the will not include some of the other fields.
* `c`: "color", the color used by the message author, or the message bar color
for type `div`.
* `n`: "name", the name of the message author
* `m`: "message", the message contents
* `d`: "date/time", the timestamp seen on log (if enabled in the chatroom)

# TODOs
In no particular order
* Add links to the README
* Adapt the parser to better handle `b` and `c` class messages
* Move parser into a class
* Ask for confirmation before proceeding
* Add configurability to the folder locations
* Add configurability for inclusion/exclusion of fields.

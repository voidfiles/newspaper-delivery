# Newspaper Delivery

[newspaper](https://github.com/codelucas/newspaper/) is a python based article extraction framework. It can produce pocket-like results. While it is very easy to use as a python library, I thought it would be interesting to turn this into a hosted app. Its all setup to be heroku app.

## Installation

```sh
git clone https://github.com/voidfiles/newspaper-delivery.git
cd newspaper-delivery
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

You should now have a local version of the app running at http://127.0.0.1:5000/

## User

You can now try it out there are two main endpoints. First is the /article endpoint. This works with newspapers [article extraction](http://newspaper.readthedocs.org/en/latest/user_guide/quickstart.html#downloading-an-article).

```
curl http://localhost:5000/article?url=http://www.macdrifter.com/2014/01/list-of-natural-language-apis-link.html
```

Will produce something like this

```js
{
    "additional_data": {},
    "authors": [],
    "canonical_link": "http://www.macdrifter.com/2014/01/list-of-natural-language-apis-link.html",
    "images": [
        "http://www.macdrifter.com/theme/images/logo.svg",
        ...
    ],
    "keywords": [
        "rundown",
		...
    ],
    "meta_description": "",
    "meta_favicon": "/theme/images/touch-icon-iphone.png",
    "meta_keywords": [
        ""
    ],
    "meta_lang": "en",
    "movies": [],
    "summary": [],
    "tags": [
        "Programming",
        "Link"
    ],
    "text": "This is a nice rundown of some natural language APIs.\n\nThe source is Mashape which looks like an API middleman. It's an interesting idea and their index looks very good and it's searchable.\n\nDon't miss the link at the bottom for PublicAPI.com, which I've seen before but always forget about.",
    "title": "List of Natural Language APIs [Link]",
    "top_image": "/theme/images/favicon.png",
    "url": "http://www.macdrifter.com/2014/01/list-of-natural-language-apis-link.html"
}
```

Lastly is the /source endpoint. Which is synonmous with the main [interface of newspaper](http://newspaper.readthedocs.org/en/latest/user_guide/quickstart.html).


```
curl http://localhost:5000/source?url=http://cnn.com
```

Will produce something like this

```js

{
    "articles": [
        "http://www.cnn.com/2012/04/04/opinion/colb-strip-search/index.html",
        "http://ac360.blogs.cnn.com/2013/12/03/pick-your-favorite-ridiculist-of-2013/",
        "http://piersmorgan.blogs.cnn.com/2013/11/08/william-shatner-on-obamacare-ponder-the-mystery/",
        ...
    ],
    "brand": "cnn",
    "categories": [
        "http://cnn.com",
        "http://cnn.com/HLN",
        "https://portfolio.money.cnn.com",
        "http://ireport.cnn.com",
        ...
    ],
    "description": "CNN.com delivers the latest breaking news and information on the latest top stories, weather, business, entertainment, politics, and more. For in-depth coverage, CNN.com provides special reports, video, audio, photo galleries, and interactive guides.",
    "domain": "cnn.com",
    "favicon": "",
    "feeds": [
        "http://rss.cnn.com/rss/cnn_tech.rss",
        ...
    ],
    "logo_url": ""
}
```

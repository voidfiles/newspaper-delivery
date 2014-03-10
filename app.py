# First have to monkey patch ntlk to find it data in a local directory
import os
from nltk import data

current_path = os.path.dirname(os.path.realpath(__file__))
nltk_data = os.path.join(current_path, 'nltk_data', '')
data.path = [nltk_data]

from urllib import quote

from flask import Flask, make_response, redirect
from flask.ext.restful import Resource, Api, reqparse
from flask.ext.restful.representations.json import output_json

from newspaper.parsers import Parser
from lxml.html.clean import Cleaner
from html2text import HTML2Text


def clean_article_html(cls, node):
    article_cleaner = Cleaner()
    article_cleaner.javascript = True
    article_cleaner.style = True
    article_cleaner.allow_tags = ['a', 'span', 'p', 'br', 'strong', 'b', 'ul', 'ol', 'li',
                                  'em', 'i', 'code', 'pre', 'blockquote', 'h1',
                                  'h2', 'h3', 'h4', 'h5', 'h6']
    article_cleaner.remove_unknown_tags = False
    return article_cleaner.clean_html(node)

Parser.clean_article_html = classmethod(clean_article_html)

import newspaper

app = Flask(__name__)
app.config['DEBUG'] = True


def output_text(data, code, headers):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


class MyApi(Api):
    def __init__(self, *args, **kwargs):
        super(MyApi, self).__init__(*args, **kwargs)
        self.representations = {
            'text': output_text,
            'application/json': output_json,
        }

api = MyApi(app)

config = newspaper.Config()
config.is_memoize_articles = False
config.keep_article_html = True

article_parser = reqparse.RequestParser()
article_parser.add_argument('url', type=unicode, help='The url of the site to scrape')
article_parser.add_argument('format', type=unicode, help='Format of article in json/text', default='json')
article_parser.add_argument('markdownify', type=bool, help='Should the text of the article be markdown', default=True)
article_parser.add_argument('include_summary', type=bool, help='Should a nlp summary be included', default=False)
article_parser.add_argument('redirect', type=unicode, help='Should redirect to another program', default='')


class ArticleSimple(Resource):
    def get(self):
        args = article_parser.parse_args()
        url = args['url']
        output_format = args['format']
        article = newspaper.build_article(url, config)
        article.download()
        article.parse()
        article.nlp()

        markdownify = bool(args['markdownify'])
        text = article.text
        if markdownify:
            h = HTML2Text(baseurl=args['url'])
            h.body_width = 0
            text = h.handle(article.article_html)

        data = {
            'url': article.url,
            'title': article.title,
            'top_image': article.top_img,
            'images': [x for x in article.imgs],
            'text': text,
            'html': article.article_html,
            'keywords': article.keywords,
            'authors': article.authors,
            'summary': article.summary,
            'meta_description': article.meta_description,
            'meta_lang': article.meta_lang,
            'meta_favicon': article.meta_favicon,
            'meta_keywords': article.meta_keywords,
            'canonical_link': article.canonical_link,
            'tags': [unicode(x) for x in article.tags],
            'movies': article.movies,
            'additional_data': article.additional_data,
        }

        if output_format == 'json':
            return output_json(data, 200, {})

        if output_format == 'text':
            output = u'---\n'
            output += u'link: %s\n' % (article.url)
            output += u'title: %s\n' % (article.title)
            output += u'authors: %s\n' % (u', '.join(article.authors))
            output += u'keywords: %s\n' % (u', '.join(article.keywords))
            output += u'---\n\n'
            if args['include_summary']:
                output += u'# Summary\n\n%s\n' % (article.summary)

            output += text

            r = args.get('redirect')
            if r and r in ['nvalt', 'notsey']:
                title = u'%s - %s' % (article.title, u', '.join(article.authors))
                title = title.encode('utf-8')
                output = output.encode('utf-8')

                if r == 'nvalt':
                    opts = {
                        'txt': output,
                        'title': title,
                    }
                    opts = '&'.join(['%s=%s' % (key, quote(val)) for key, val in opts.items()])
                    url = 'nvalt://make/?' + opts

                if r == 'notsey':
                    opts = {
                        'text': output,
                        'name': title,
                    }
                    opts = '&'.join(['%s=%s' % (key, quote(val)) for key, val in opts.items()])
                    url = 'notesy://x-callback-url/append?' + opts

                return make_response(redirect(url))

            return output_text(output, 200, {'Content-Type': 'text'})

site_parser = reqparse.RequestParser()
site_parser.add_argument('url', type=unicode, help='The url of the site to scrape')


class SourceSimple(Resource):

    def get(self):
        args = site_parser.parse_args()
        source = newspaper.build(args['url'], config)
        return {
            'domain': source.domain,
            'logo_url': source.logo_url,
            'favicon': source.favicon,
            'brand': source.brand,
            'description': source.description,
            'categories': [unicode(x.url) for x in source.categories],
            'feeds': [unicode(x.url) for x in source.feeds],
            'articles': [unicode(x.url) for x in source.articles],
        }


api.add_resource(ArticleSimple, '/article')
api.add_resource(SourceSimple, '/source')

if __name__ == '__main__':
    app.run(debug=True)

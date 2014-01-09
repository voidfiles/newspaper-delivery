from flask import Flask
from flask.ext.restful import Resource, Api, reqparse

import newspaper

app = Flask(__name__)
api = Api(app)

config = newspaper.Config()
config.is_memoize_articles = False

article_parser = reqparse.RequestParser()
article_parser.add_argument('url', type=unicode, help='The url of the site to scrape')


class ArticleSimple(Resource):
    def get(self):
        args = article_parser.parse_args()
        url = args['url']
        article = newspaper.build_article(url)
        article.download()
        article.parse()
        article.nlp()

        return {
            'url': article.url,
            'title': article.title,
            'top_image': article.top_img,
            'images': [x for x in article.imgs],
            'text': article.text,
            'keywords': article.keywords,
            'authors': article.authors,
            'summary': article.authors,
            'authors': article.authors,
            'meta_description': article.meta_description,
            'meta_lang': article.meta_lang,
            'meta_favicon': article.meta_favicon,
            'meta_keywords': article.meta_keywords,
            'canonical_link': article.canonical_link,
            'tags': [unicode(x) for x in article.tags],
            'movies': article.movies,
            'additional_data': article.additional_data,
        }


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

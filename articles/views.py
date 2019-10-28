import json
import random
from articles.api import get_articles, get_quotes
from articles.models import Comment
from dateutil.parser import parse
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        articles = get_articles()['results']
        # get first article from api with tag slug=10-promise to display as main article
        main_article = next(iter([a for a in articles if '10-promise' in [t['slug'] for t in a['tags']]]), None)
        if main_article:
            url_headline = strip_headline_for_url(main_article['headline'])
            image_url = self.get_featured_image_url(main_article)

            context['main_article'] = { 'headline': main_article['headline'],
                                        'url_headline': url_headline,
                                        'image_url': image_url,
                                        'author': main_article['byline'],
                                        'publish_date': parse(main_article['publish_at']).strftime('%B %-d, %Y'),
                                        'promo': main_article['promo']
                                        }
            articles.remove(main_article)
        else:
            context['main_article'] = {}

        # from the remaining articles take 3 at random to display below the main article
        other_articles = random.sample(articles, 3)
        context['other_articles'] = []
        for article in other_articles:
          url_headline = strip_headline_for_url(article['headline'])
          image_url = self.get_featured_image_url(article)
          context['other_articles'].append({
                                    'headline': article['headline'],
                                    'url_headline': url_headline,
                                    'image_url': image_url,
                                    'author': article['byline'],
                                    'publish_date': parse(article['publish_at']).strftime('%B %-d, %Y'),
                                    'promo': article['promo']
          })

        return context

    def get_featured_image_url(self, article):
        return next(iter([i['url'] for i in article['images'] if i['featured'] == True]), None)


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = get_articles()['results']

        # get the article matching the headline from the url with related comments
        article = next(iter([a for a in articles if strip_headline_for_url(a['headline']) == kwargs['headline']]))
        if article:
            comments = [c.comment_text for c in Comment.objects.filter(article_uuid=article['uuid'])]
            context['article'] = {'headline': article['headline'],
                                    'author': article['byline'],
                                    'publish_datetime': parse(article['publish_at']).strftime('%B %-d, %Y at %-I:%M%P'),
                                    'body': article['body'].replace('{%sfr%}',''),
                                    'disclosure': article['disclosure'],
                                    'uuid': article['uuid'],
                                    'comments': comments
                                    }

            articles.remove(article)
        else:
            context['article'] = {}

        latest_headlines = []
        # from the remaining articles take the 5 most recently published to display as latest headlines
        for a in list(reversed(sorted(articles, key=lambda x: x['publish_at'])))[:5]:
            latest_headlines.append({'headline': a['headline'], 'url_headline': strip_headline_for_url(a['headline'])})
        context['latest_headlines'] = latest_headlines

        # get quotes related to the article from the api data
        instrument_ids = [i['instrument_id'] for i in article['instruments']]
        quotes = []
        for q in get_quotes():
            # there are duplicates in the quote data, for example INTC, so an extra de-duplication check is needed
            if q['InstrumentId'] in instrument_ids and q not in quotes:
                quotes.append(q)

        for q in quotes:
            q['change_percent'] = round(q['PercentChange']['Value'] * 100, 2)

        context['quotes'] = quotes
        return context


@method_decorator(csrf_exempt, name='dispatch')
class CommentView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        Comment.objects.create(comment_text=payload['comment'], article_uuid=payload['article_uuid'])
        response = HttpResponse(status=201)
        return response
    

def strip_headline_for_url(headline):
    # return headline in lowercase, with non-alphanumeric characters removed, and spaces replaced with dashes
    return ''.join([i for i in headline if i.isalnum() or i == ' ']).replace(' ','-').lower()

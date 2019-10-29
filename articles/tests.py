from articles.models import Comment
from articles.views import HomeView, strip_headline_for_url
from django.test import TestCase


class HomeViewTests(TestCase):

    def test_get_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'home.html')

    def test_correct_articles_are_shown(self):
        response = self.client.get('/')
        main_article = response.context_data['main_article']
        self.assertEqual(main_article, {'headline': "Here's Why Barrrick Gold Plunged 10% in October",
                                        'url_headline': 'heres-why-barrrick-gold-plunged-10-in-october',
                                        'image_url': 'https://g.foolcdn.com/editorial/images/463206/gold_bar_2.jpg',
                                        'author': 'Scott Levine', 'publish_date': 'November 10, 2017',
                                        'promo': 'As autumn marches on, the trees are losing their leaves, and Barrick is losing its glitter.'})
        other_articles = response.context_data['other_articles']
        self.assertEqual(len(other_articles), 3)
        other_headlines = [a['url_headline'] for a in other_articles]
        self.assertNotIn(main_article['url_headline'], other_headlines)

    def test_get_featured_image_url(self):
        view = HomeView()
        article = {
            'images': [
                {'url': 'first', 'featured': False},
                {'url': 'second', 'featured': True},
                {'url': 'third', 'featured': False},
            ]
        }
        url = view.get_featured_image_url(article)
        self.assertEqual(url, 'second')

        article = {
            'images': [
                {'url': 'first', 'featured': False},
                {'url': 'second', 'featured': False},
                {'url': 'third', 'featured': False},
            ]
        }
        url = view.get_featured_image_url(article)
        self.assertEqual(url, None)

        article = {
            'images': []
        }
        url = view.get_featured_image_url(article)
        self.assertEqual(url, None)

    def test_strip_headline_for_url(self):
        stripped_headline = strip_headline_for_url("Here's Why Barrrick Gold Plunged 10% in October")
        self.assertEqual(stripped_headline, 'heres-why-barrrick-gold-plunged-10-in-october')


class ArticleViewTests(TestCase):

    def test_get_article_detail(self):
        response = self.client.get('/articles/heres-why-barrrick-gold-plunged-10-in-october')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'article.html')

    def test_correct_content_is_shown(self):
        response = self.client.get('/articles/heres-why-barrrick-gold-plunged-10-in-october')
        article = response.context_data['article']
        self.assertEqual(article, {'headline': "Here's Why Barrrick Gold Plunged 10% in October",
                                   'author': 'Scott Levine',
                                   'publish_datetime': 'November 10, 2017 at 3:04PM',
                                   'body': article['body'],
                                   'disclosure': article['disclosure'],
                                   'uuid': 'a7acd8c8-c5ce-11e7-9fa6-0050569d4be0',
                                   'comments': []})
        latest_headlines = response.context_data['latest_headlines']
        self.assertEqual(latest_headlines, [{'headline': "Is Goldman Sachs' Stock Worth a Look?", 'url_headline': 'is-goldman-sachs-stock-worth-a-look'},
                                            {'headline': "National Grid's Earnings Underwhelm, but There Are Some Silver Linings", 'url_headline': 'national-grids-earnings-underwhelm-but-there-are-some-silver-linings'},
                                            {'headline': '51job Accelerates to Get the Job Done', 'url_headline': '51job-accelerates-to-get-the-job-done'},
                                            {'headline': 'If You Love Artificial Intelligence, You Should Check Out NVIDIA Corporation', 'url_headline': 'if-you-love-artificial-intelligence-you-should-check-out-nvidia-corporation'},
                                            {'headline': "3 Takeaways From Intel Corp.'s 10-Q Filing", 'url_headline': '3-takeaways-from-intel-corps-10q-filing'}])
        quotes = response.context_data['quotes']
        symbols = [q['Symbol'] for q in quotes]
        self.assertEqual(len(quotes), 2)
        self.assertEqual(symbols, ['ABX', 'GLD'])


class CommentViewTests(TestCase):

    def test_post_article_comment(self):
        self.assertEqual(Comment.objects.count(), 0)
        data = {'comment': 'test comment', 'article_uuid': 'a7acd8c8-c5ce-11e7-9fa6-0050569d4be0'}
        response = self.client.post('/comments', data=data, content_type='application/json')
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.comment_text, 'test comment')
        self.assertEqual(str(comment.article_uuid), 'a7acd8c8-c5ce-11e7-9fa6-0050569d4be0')

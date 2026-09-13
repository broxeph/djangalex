"""
Whole-site render checks.

Merging to master deploys straight to production with no CI in between, so
``./manage.py test`` is the last gate. These tests render every page, anonymous
and logged in, to catch broken templates, template tags and URL names. They are
not about business logic; the app-level tests cover that.
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from django.views.defaults import server_error

from home.models import Box, Subtitle
from wineapp.models import Post, Review, Wine


class SiteRenderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'correct horse battery staple'
        cls.user = User.objects.create_user('taster', 'taster@example.com', cls.password)
        cls.wine = Wine.objects.create(name='Chateau Test', variety='Merlot', abv=13.5, description='Fine.')
        Wine.objects.create(name='Unreviewed Wine')  # Gives the recommendation page something to show
        cls.review = Review.objects.create(
            wine=cls.wine, pub_date=timezone.now(), user_name=cls.user.username, comment='Nice.', rating=4)
        Post.objects.create(title='Some news', text='Text.', pub_date=timezone.now(), user_name=cls.user.username)
        Box.objects.create(name='GitHub', logo_url='github.png', link_url='https://github.com/', sort_order=1)
        Subtitle.objects.create(text='A memorable quote.', author='Someone')

    @classmethod
    def public_urls(cls):
        return [
            reverse('home:index'),
            reverse('wineapp:index'),
            reverse('wineapp:wine_list'),
            reverse('wineapp:wine_detail', args=[cls.wine.id]),
            reverse('wineapp:review_list'),
            reverse('wineapp:review_detail', args=[cls.review.id]),
            reverse('wineapp:user_review_list', args=[cls.user.username]),
            reverse('login'),
        ]

    @classmethod
    def login_required_urls(cls):
        return [
            reverse('wineapp:user_recommendation_list'),
            reverse('wineapp:add_review', args=[cls.wine.id]),
            reverse('password_change'),
            reverse('password_change_done'),
        ]

    def assert_renders(self, urls):
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertGreater(len(response.content), 500)

    def test_public_pages_render_for_anonymous_visitors(self):
        self.assert_renders(self.public_urls() + [reverse('registration_register')])

    def test_pages_render_for_logged_in_users(self):
        self.client.force_login(self.user)
        self.assert_renders(self.public_urls() + [
            reverse('wineapp:user_recommendation_list'),
            reverse('wineapp:user_review_list'),
            reverse('password_change'),
            reverse('password_change_done'),
        ])

    def test_login_required_pages_redirect_anonymous_visitors_to_login(self):
        for url in self.login_required_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_home_page_shows_boxes_and_a_quote(self):
        response = self.client.get(reverse('home:index'))
        self.assertContains(response, 'home/github.png')
        self.assertContains(response, 'A memorable quote.')

    def test_recommendations_exclude_wines_the_user_reviewed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('wineapp:user_recommendation_list'))
        self.assertContains(response, 'Unreviewed Wine')
        self.assertNotContains(response, 'Chateau Test')

    def test_registration_creates_and_logs_in_the_user(self):
        response = self.client.post(reverse('registration_register'), {
            'username': 'newbie', 'email': 'newbie@example.com',
            'password1': self.password, 'password2': self.password,
        })
        self.assertRedirects(response, reverse('wineapp:index'))
        self.assertTrue(User.objects.filter(username='newbie').exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username='newbie').pk)

    def test_registration_redirects_users_who_are_already_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('registration_register'))
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False)

    def test_logout_is_post_only_and_renders_the_logged_out_page(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logout.html')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_adding_a_review_redirects_to_the_wine(self):
        self.client.force_login(self.user)
        url = reverse('wineapp:add_review', args=[self.wine.id])
        response = self.client.post(url, {'rating': 5, 'comment': 'Superb.'})
        self.assertRedirects(response, reverse('wineapp:wine_detail', args=[self.wine.id]))
        self.assertEqual(self.wine.review_set.filter(comment='Superb.', user_name=self.user.username).count(), 1)

    def test_invalid_review_re_renders_the_form(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('wineapp:add_review', args=[self.wine.id]), {'rating': '', 'comment': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add your review')

    def test_unknown_urls_render_the_custom_404_page(self):
        for url in ('/no-such-page/', '/wineapp/admin/'):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.assertTemplateUsed(response, '404.html')
                self.assertContains(response, 'Page not found', status_code=404)

    def test_500_page_renders_with_no_request_context(self):
        # Django renders 500.html with an empty context, so the template must not need one
        response = server_error(RequestFactory().get('/'))
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Something broke', response.content)

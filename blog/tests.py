from django.test import TestCase, Client

from bs4 import BeautifulSoup
from .models import Post



class TestView(TestCase):
    def setUp(self):
        self.client = Client()


    # navbar 이동설정 해주기.
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):

        # 포스트 목록 페이지를 가져옴
        response = self.client.get('/blog/')

        #정상적으로 페이지가 로드된다
        self.assertEqual(response.status_code, 200)

        #페이지 타이틀은  blog 이다
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        # 위에 def navbar 설정한 내용이 읽어진다. 아래 주석처리 부분과 동일한 효과를 가지고있다.
        self.navbar_test(soup)


        # # 네비게이션 바가 있다.
        # navbar = soup.nav
        #
        # # blog, About me 라는 문구가 네비게이션 바에 있다.
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)


        # 포스트 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)

        # 아직 게시물이 없다는 문구를 출력한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)


        # 포스트가 2개 있다면
        post_001 = Post.objects.create(
            title='첫번째 포스트 입니다.',
            content='Hello word. We are the World',
        )
        post_002 = Post.objects.create(
            title='두번째 포스트 입니다.',
            content='1등이 전부는 아니잖어요',
        )

        self.assertEqual(Post.objects.count(), 2)


        # 포스트 목록 페이지를 새로고침 했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        # main_area에 포스트 2개의 제목이 존재한다
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 아직 게시물이 없다는 문구는 더이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):

        # 포스트 1개를 만든다
        post_001 = Post.objects.create(
            title='첫번째 포스트',
            content='hello word'
        )

        # 그 포스트의 url 은 blog/1 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 첫번째 포스트의 상세페이지로
        # 첫번째 포스트url로 접근하면 정삭적으로 작동한다
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 위에 def navbar 의 내용을 읽어온다. 아래 주석처리와 동일한 효과를 지니고 있다.
        self.navbar_test(soup)


        # # 포스트 목록 페이지와 똑같은 네비게이션 바가 있다.
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)

        # 첫번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어있다
        self.assertIn(post_001.title, soup.title.text)


        #첫번째 포스트의 제목이 포스트 영역에 들어있다
        # 아직 작성 불가
        main_area = soup.find('div', id="main-area")
        post_area = main_area.find('div', id="post-area")
        self.assertIn(post_001.title, post_area.text)

        # 첫번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)

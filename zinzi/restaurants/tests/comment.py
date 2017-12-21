from random import randint

from django.db.models import Avg
from django.urls import reverse, resolve
from rest_framework import status

from restaurants.models import Comment, STAR_RATING
from restaurants.tests import RestaurantTestBase
from restaurants.views import CommentListCreateView, CommentUpdateDestroyView

__all__ = (
    'CommentListCreateViewTest',
    'CommentUpdateDestroyViewTest',
)


class CommentListCreateViewTest(RestaurantTestBase):
    URL_COMMENT_LIST_CREATE_NAME = 'restaurants:detail:comment-list-create'
    URL_COMMENT_LIST_CREATE = '/restaurants/1/comments/'
    VIEW_CLASS = CommentListCreateView

    def create_comment(self, restaurant):
        user = self.create_user()
        num = randint(5, 20)
        for i in range(num):
            Comment.objects.create(
                author=user,
                restaurant=restaurant,
                star_rate=STAR_RATING[randint(0, len(STAR_RATING) - 1)][0],
                comment='test',
            )
        return Comment.objects.all()

    def test_comment_list_create_url_name_reverse(self):
        url = reverse(self.URL_COMMENT_LIST_CREATE_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_COMMENT_LIST_CREATE)

    def test_comment_list_create_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_COMMENT_LIST_CREATE)
        self.assertEqual(resolver_match.view_name, self.URL_COMMENT_LIST_CREATE_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW_CLASS)

    def test_http_method(self):
        restaurant = self.create_restaurant()
        user = self.create_user()
        self.create_comment(restaurant=restaurant)
        url = reverse(self.URL_COMMENT_LIST_CREATE_NAME, kwargs={'pk': restaurant.pk})
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        # 로그인 전
        post_response_before_login = self.client.post(url)
        self.assertEqual(post_response_before_login.status_code, status.HTTP_401_UNAUTHORIZED)
        # 로그인 후
        self.client.force_authenticate(user=user)
        self.client.force_login(user=user)
        post_response_after_login = self.client.post(url, data={
            'star_rate': STAR_RATING[randint(0, len(STAR_RATING) - 1)][0],
            'comment': "test"
        })
        self.assertEqual(post_response_after_login.status_code, status.HTTP_201_CREATED)
        put_response = self.client.put(url)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        patch_response = self.client.patch(url)
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_comment_list_before_restaurant_is_not_created(self):
        url = reverse(self.URL_COMMENT_LIST_CREATE_NAME, kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_list(self):
        restaurant = self.create_restaurant()
        url = reverse(self.URL_COMMENT_LIST_CREATE_NAME, kwargs={'pk': restaurant.pk})
        self.create_comment(restaurant=restaurant)
        response = self.client.get(url)
        comment = Comment.objects.all()
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], comment.count())
        # pagination 체크
        self.assertTrue(len(response.data['results']) <= 5)

    def test_comment_create(self):
        restaurant = self.create_restaurant()
        url = reverse(self.URL_COMMENT_LIST_CREATE_NAME, kwargs={'pk': restaurant.pk})
        user = self.create_user()
        self.client.force_authenticate(user=user)
        self.client.force_login(user=user)
        response = self.client.post(url, data={
            'star_rate': STAR_RATING[randint(0, len(STAR_RATING) - 1)][0],
            'comment': "test"
        })
        self.assertIn('pk', response.data)
        self.assertIn('author', response.data)
        self.assertIn('restaurant', response.data)
        self.assertIn('star_rate', response.data)
        self.assertIn('comment', response.data)
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        # restaurant.calculate_goten_star_rate가 정상동작을 하는지, star_rate가 잘 들어가는지 테스트
        restaurant.calculate_goten_star_rate()
        comment = Comment.objects.filter(restaurant=restaurant)
        avg = comment.aggregate(Avg('star_rate'))
        self.assertEqual(restaurant.star_rate, avg['star_rate__avg'])
        # 잘못된 데이터를 넣었을 경우 400오류가 잘 발생하는지 테스트
        wrong_data_list = (
            {"star_rate": -1, "comment": "test"},
            {"star_rate": 0.1, "comment": "test"},
            {"star_rate": 6, "comment": "test"},
            {"star_rate": 1,
             "comment": "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest"
                        "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest"
                        "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest"
                        "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest"
                        "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest"
                        "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest"},
            {"star_rate": 1},
            {"comment": "comment"},
        )
        for wrong_data in wrong_data_list:
            wrong_response = self.client.post(url, data=wrong_data)
            self.assertEqual(wrong_response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentUpdateDestroyViewTest(RestaurantTestBase):
    URL_COMMENT_UPDATE_DELETE_NAME = 'restaurants:comment-update-destroy'
    URL_COMMENT_UPDATE_DELETE = '/restaurants/comments/1/'
    VIEW_CLASS = CommentUpdateDestroyView

    def create_comment(self):
        user = self.create_user()
        if Comment.objects.count() != 0:
            return Comment.objects.first()
        return Comment.objects.create(
            author=user,
            restaurant=self.create_restaurant(),
            star_rate=STAR_RATING[randint(0, len(STAR_RATING) - 1)][0],
            comment='test',
        )

    def test_comment_update_destroy_url_name_reverse(self):
        url = reverse(self.URL_COMMENT_UPDATE_DELETE_NAME, kwargs={'pk': 1})
        self.assertEqual(url, self.URL_COMMENT_UPDATE_DELETE)

    def test_comment_update_destroy_url_resovle_view_class(self):
        resolver_match = resolve(self.URL_COMMENT_UPDATE_DELETE)
        self.assertEqual(resolver_match.view_name, self.URL_COMMENT_UPDATE_DELETE_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW_CLASS)

    def test_http_method_with_have_permission_user(self):
        user = self.create_user()
        comment = self.create_comment()
        url = reverse(self.URL_COMMENT_UPDATE_DELETE_NAME, kwargs={'pk': comment.pk})
        self.client.force_authenticate(user=user)
        self.client.force_login(user=user)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        put_response = self.client.put(url)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        patch_response = self.client.patch(url)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_http_method_with_do_not_have_permission_user(self):
        comment = self.create_comment()
        user2 = self.create_user2()
        url = reverse(self.URL_COMMENT_UPDATE_DELETE_NAME, kwargs={'pk': comment.pk})
        self.client.force_authenticate(user=user2)
        self.client.force_login(user=user2)
        self.client.force_authenticate(user=user2)
        self.client.force_login(user=user2)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        post_response = self.client.post(url)
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        put_response = self.client.put(url)
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        patch_response = self.client.patch(url)
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)
        delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    
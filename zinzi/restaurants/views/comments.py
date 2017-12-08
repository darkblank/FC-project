from rest_framework import generics, permissions, mixins
from rest_framework.generics import get_object_or_404

from utils.permissions import IsAuthorOrReadOnly
from ..models import Comment, Restaurant
from ..pagination import CommentListPagination
from ..serializers import CommentSerializer

__all__ = (
    'CommentListCreateView',
    'CommentUpdateDestroyView',
)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentListPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        res_pk = self.kwargs['pk']
        return Comment.objects.filter(restaurant_id=res_pk)

    def perform_create(self, serializer):
        # url에서 받은 레스토랑 pk를 이용해 레스토랑 객체를 가져옴
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        serializer.save(restaurant=restaurant, author=self.request.user)
        # 코멘트 작성시 자동으로 별점을 계산하도록 설정
        restaurant.calculate_goten_star_rate()


class CommentUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        # 로그인하지 않았을 경우 읽기만 가능
        permissions.IsAuthenticatedOrReadOnly,
        # 작성자가 아니면 읽기만 가능
        IsAuthorOrReadOnly,
        # Admin일 경우 사용 가능
        permissions.IsAdminUser,
    )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

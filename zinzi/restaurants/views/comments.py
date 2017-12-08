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
        queryset = Comment.objects.filter(restaurant_id=res_pk)
        return queryset

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        serializer.save(restaurant=restaurant, author=self.request.user)
        restaurant.calculate_goten_star_rate()


class CommentUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # fixme permission 적용이 안됨
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

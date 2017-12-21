from rest_framework import generics

from accounts.models import Profile
from accounts.serializers import ProfileSerializer, OwnerProfileSerializer
from utils.permissions import IsUserOrNotAllow


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'user'
    permission_classes = (
        IsUserOrNotAllow,
    )


class OwnerProfileView(generics.RetrieveAPIView):
    serializer_class = OwnerProfileSerializer
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'user'
    permission_classes = (
        IsUserOrNotAllow,
    )

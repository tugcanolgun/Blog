from rest_framework import permissions, mixins
from rest_framework.generics import GenericAPIView

from panel.models import Content
from panel.api.serializers import ContentSerializer


class ContentList(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

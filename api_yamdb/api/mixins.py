from rest_framework import mixins, viewsets


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """
    Набор представлений, обеспечивающий действия 'create','list','.
    """
    pass


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Набор представлений, обеспечивающий действия 'retrieve','update'.
    """
    pass
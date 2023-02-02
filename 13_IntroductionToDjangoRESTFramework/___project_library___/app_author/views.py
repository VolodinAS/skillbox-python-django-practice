from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from rest_framework.request import Request

from app_author.models import Author
from app_author.serializers import AuthorSerializer


class AuthorList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление для получения списка книг и добавления новой книги
    """
    serializer_class = AuthorSerializer
    
    def get_queryset(self):
        queryset = Author.objects.all()
        return queryset
    
    def get(self, request: Request):
        return self.list(request)
    
    def post(self, request: Request):
        return self.create(request)


class AuthorDetail(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Информация об отдельном авторе, изменение, удаление
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

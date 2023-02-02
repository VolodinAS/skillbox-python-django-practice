from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from app_books.models import Book
from app_author.models import Author
from app_books.serializers import BookSerializer


class BooksList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление для получения списка книг и добавления новой книги
    """
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        # print(queryset)
        book_title = self.request.query_params.get('title')
        author: str = self.request.query_params.get('author')
        pages: str = self.request.query_params.get('pages')
        pages_more: str = self.request.query_params.get('pages_more')
        pages_less: str = self.request.query_params.get('pages_less')
        
        try:
            pages = int(pages)
        except TypeError:
            pages = None
        
        try:
            pages_more = int(pages_more)
        except TypeError:
            pages_more = None
        
        try:
            pages_less = int(pages_less)
        except TypeError:
            pages_less = None
        
        last_name = None
        first_name = None
        if author and len(author) > 0:
            author_data: list = author.split()
            print(f'{author_data=}')
            if len(author_data) == 2:
                last_name = author_data[0]
                first_name = author_data[1]
            else:
                last_name = author
        if book_title:
            queryset = queryset.filter(title__contains=book_title)
        
        if last_name:
            queryset = queryset.filter(author__last_name__contains=last_name)
        
        if first_name:
            queryset = queryset.filter(author__first_name__contains=first_name)
            
        if pages:
            queryset = queryset.filter(pages=pages)
        else:
            if pages_more:
                queryset = queryset.filter(pages__gte=pages_more)
            if pages_less:
                queryset = queryset.filter(pages__lte=pages_less)
        
        return queryset
    
    def get(self, request: Request):
        return self.list(request)
    
    def post(self, request: Request):
        print(request.data)
        last_name = request.data['author.last_name']
        first_name = request.data['author.first_name']
        birthday = request.data['author.birthday']
        title = request.data['title']
        isbn = request.data['isbn']
        year = request.data['year']
        pages = request.data['pages']

        author_exists, created_author = Author.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            birthday=birthday
        )
        book, created_book = Book.objects.get_or_create(
            isbn=isbn,
            defaults={
                'author': author_exists,
                'title': title,
                'isbn': isbn,
                'year': year,
                'pages': pages
            }
        )
        data = BookSerializer(book).data
        return Response(data, status=status.HTTP_200_OK)
        
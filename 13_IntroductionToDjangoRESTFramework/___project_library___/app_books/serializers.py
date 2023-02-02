from rest_framework import serializers

from app_author.serializers import AuthorSerializer
from app_books.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    # author = serializers.HyperlinkedIdentityField(
    #     view_name='api:author-detail'
    # )
    
    author = AuthorSerializer()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'author',
            'title',
            'isbn',
            'year',
            'pages'
        ]

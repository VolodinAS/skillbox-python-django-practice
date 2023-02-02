from rest_framework import serializers

from app_author.models import Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    
    # author = serializers.HyperlinkedIdentityField(
    #     view_name='api:author-detail'
    # )
    
    class Meta:
        model = Author
        fields = [
            'id',
            'last_name',
            'first_name',
            'birthday'
        ]

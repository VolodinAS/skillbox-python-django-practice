# from rest_framework import routers
#
# from app_books.api import BookViewSet
#
# router = routers.DefaultRouter()
# router.register('books', BookViewSet)
#
# urlpatterns = router.urls

from django.urls import path

from app_books.views import BooksList

urlpatterns = [
    path(
        'books/',
        BooksList.as_view(),
        name='books_list'
    )
]

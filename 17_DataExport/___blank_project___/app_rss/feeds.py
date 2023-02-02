from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.urls import reverse

from app_news.models import News


class LatestNewsFeed(Feed):
    title = 'Новости'
    link = '/latest/'
    description = 'Самые свежие новости'
    
    def items(self) -> QuerySet:
        return News.objects.filter(is_published=True).order_by('-is_published', '-published_at')
    
    def item_title(self, item: News) -> str:
        return item.title
    
    def item_description(self, item: News) -> str:
        return item.content
    
    def item_link(self, item: News) -> str:
        return reverse('news:page_houses_news_item', args=[item.pk])

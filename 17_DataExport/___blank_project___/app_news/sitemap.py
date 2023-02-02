from django.contrib.sitemaps import Sitemap

from app_news.models import News


class NewsSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return News.objects.filter(is_published=True).all()
    
    def lastmod(self, obj: News):
        return obj.published_at
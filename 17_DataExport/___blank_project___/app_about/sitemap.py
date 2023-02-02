from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class AboutSiteMap(Sitemap):
    changefreq = "yearly"
    priority = 0.5
    
    def items(self):
        # Return list of url names for views to include in sitemap
        return ['about:page_houses_about']
    
    def location(self, item):
        return reverse(item)

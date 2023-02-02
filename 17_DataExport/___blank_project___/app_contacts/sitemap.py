from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ContactsSiteMap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    
    def items(self):
        # Return list of url names for views to include in sitemap
        return ['contacts:page_houses_contacts']
    
    def location(self, item):
        return reverse(item)

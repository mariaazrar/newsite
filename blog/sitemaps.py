from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly' 
    priority = 0.9

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated
    
    # location is optional
    # def location(self, obj): 
    #     return reverse('blog:post_list')
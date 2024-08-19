from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy 
from django.utils.safestring import SafeText
import markdown
from .models import Post

class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('blog:post_list')
    description = 'Updated content of my blog'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item):
        return item.publish
    
    

    
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    commented_posts = Post.published.annotate(most_commented=Count('comments')).order_by('-most_commented')[:count]
    return commented_posts

@register.filter(name='markdown')
def markdown_format(body):
    return mark_safe(markdown.markdown(body))
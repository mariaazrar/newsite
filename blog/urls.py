from django.urls import path
from .views import post_list, post_detail, share_post, comment_post, post_search
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # post views
    # path('', PostListView.as_view(), name='post_list'),
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', share_post, name='post_share'),
    path('<int:post_id>/comment/', comment_post, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', post_search, name='post_search'),
]
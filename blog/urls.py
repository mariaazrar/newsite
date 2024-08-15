from django.urls import path
from .views import PostListView, post_detail, share_post, comment_post

app_name = 'blog'

urlpatterns = [
    # post views
    path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', share_post, name='post_share'),
    path('<int:post_id>/comment/', comment_post, name='post_comment')
]
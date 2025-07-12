from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('create/', views.make_post, name='post_create'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('post/<int:post_id>/', views.post_page, name='post_detail'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]

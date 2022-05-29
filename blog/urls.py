from django.urls import path, include
from blog import views

urlpatterns = [
    path('latest-blogs/', views.LatestPostsList.as_view()),
    path('blogs/', views.PostsList.as_view()),
    path('blogs/search/', views.search),
    path('blog/<slug:post_slug>/', views.PostDetail.as_view()),
]

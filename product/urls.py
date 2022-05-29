from django.urls import path, include
from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/comment/', views.comment),

    path('products/review/', views.ListReview.as_view()),

    path('products/<slug:product_slug>/reviews/', views.DetailReview.as_view()),

    path('products/<slug:category_slug>/<slug:product_slug>/',
         views.ProductDetail.as_view()),

    path('products/<slug:category_slug>/',
         views.CategoryDetail.as_view()),
]

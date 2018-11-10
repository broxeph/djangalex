from django.contrib import admin
from django.urls import path

from . import views

app_name = 'wineapp'
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /admin/
    path('admin/', admin.site.urls),
    # ex: /review_list.html
    path('review_list/', views.review_list, name='review_list'),
    # ex: /review/5/
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),
    # ex: /wine/
    path('wine/', views.wine_list, name='wine_list',),
    # ex: /wine/5/
    path('wine/<int:wine_id>/', views.wine_detail, name='wine_detail'),
    path('wine/<int:wine_id>/add_review/', views.add_review, name='add_review'),
    # ex: /review/user/TestUser/ - get reviews for a user
    path('review/user/<username>/', views.user_review_list, name='user_review_list'),
    path('review/user/', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get wine recommendations for the logged-in user
    path('recommendation/', views.user_recommendation_list,  name='user_recommendation_list'),
]

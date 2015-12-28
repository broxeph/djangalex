from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    # ex: /admin/
    url(r'^admin/', include(admin.site.urls)),
    # ex: /review_list.html
    url(r'^review_list', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail,
        name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.wine_list, name='wine_list',),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail')
]

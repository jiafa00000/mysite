"""fucetheworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mysite import views as mysite_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',mysite_views.home,name="home"),#home page
    url(r'^about/$',mysite_views.about,name='about'),#introduce
    url(r'^message/$',mysite_views.message,name='message'),#leaving message for me
    url(r'^archive/$',mysite_views.archive,name='archive'),#archive
    url(r'^search/$',mysite_views.blog_search,name='search'),#search title
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<id>\d+)/$',mysite_views.detail,name='detail'),#article detail
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{1,2})/$',mysite_views.archive_monthDetail,name='archive_month'),#archive on month
    url(r'^articleClassfi/(?P<classfi>\w+)/$',mysite_views.classificationDetail,name='classfiDetail'),#archive on classification
    url(r'^articleTag/(?P<tag>\w+)/$',mysite_views.tagDetail,name='tagDetail')
]

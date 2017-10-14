"""prhlt2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from portal import views as vportal

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

	url(r'^login/', vportal.login),
	url(r'^logout/', vportal.logout),

    url(r'^problems/show_problem_status/$', vportal.show_problem_status, name='show_problem_status'),

    url(r'^problems/upload_training/upload/', vportal.upload_training, name='upload_training'),
    url(r'^problems/upload_training/delete/', vportal.delete_training, name='check_upload_training'),
    url(r'^problems/upload_training/check/', vportal.check_upload_training, name='check_upload_training'),

    url(r'^problems/train/start/', vportal.start_training, name='start_training'),
    url(r'^problems/train/check/', vportal.check_training, name='check_training'),
    url(r'^problems/train/', vportal.check_training, name='check_training'),

    url(r'^problems/upload_test/upload/', vportal.upload_test, name='upload_test'),
    url(r'^problems/upload_test/delete/', vportal.delete_test, name='check_upload_test'),
    url(r'^problems/upload_test/check/', vportal.check_upload_test, name='check_upload_test'),

    url(r'^problems/evaluate/start/', vportal.start_evaluation, name='start_evaluation'),
    url(r'^problems/evaluate/check/', vportal.check_evaluation, name='check_evaluation'),
    url(r'^problems/evaluate/', vportal.check_evaluation, name='check_evaluation'),


	url(r'^problems/$', vportal.load_problem, name='problems'),

    url(r'^', vportal.login, name='index'),
    
]

#coding:utf-8
from django.conf import settings
from django.conf.urls import patterns, url
import views

# Uncomment the next two lines to enable the admin:
# admin.autodiscover()

urlpatterns = patterns('', 
    url
    # media URL
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + "js/"}), 
    
    #apidemo
    (r'^$', views.index), 
    (r'^index/$', views.index), 
    (r'^userinfo$', views.show_userinfo), 
    (r'^videolist$', views.show_videolist), 
    (r'^play/([\d, A-Z]{1,6})/([\d, A-Z]{1,32})$', views.show_play), 
    (r'^playcode/([\d, A-Z]{1,32})$', views.show_playcode), 
    (r'^edit/([\d, A-Z]{1,32})$', views.show_edit), 
    (r'^upload$', views.show_upload), 
    (r'^notify_info$', views.show_notify_info), 
    (r'^search$', views.show_search), 
    (r'^notify$', views.notify), 
    (r'^getuploadurl$', views.get_upload_url), 
    (r'^searchvideo$', views.search_video), 
    (r'^delete/([\d, A-Z]{1,32})$', views.delete), 
    (r'^editvideo$', views.edit_video), 
    (r'^videosync$', views.videosync), 
)
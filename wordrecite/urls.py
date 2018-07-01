# coding:utf-8


from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.indexview, name='indexview'),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.loginview, name='loginview'),
    url(r'^logout/$', views.logoutview, name='logoutview'),
    url(r'^register/$', views.registerview, name='registerview'),
    url(r'^vocabulary/$', views.vocabularyview, name='vocabularyview'),
    url(r'^status/$', views.statusview, name='statusview'),
    url(r'^settings/$', views.settingsview, name='settingsview'),
    url(r'^task/$', views.taskview, name='taskview'),
    url(r'^mynotes/$', views.mynotesview, name='mynotesview'),
    url(r'^detail/(?P<word_id>\d+)$', views.detailview, name='detailview'),
    url(r'^notes/(?P<word_id>\d+)$', views.notesview, name='notesview'),
    url(r'^editnote/(?P<word_id>\d+)$', views.editnoteview, name='editnoteview'),
    url(r'^deletenote/(?P<word_id>\d+)$',
        views.deletenoteview, name='deletenoteview'),
    url(r'^moretask/$', views.moretaskview, name='moretaskview'),
    url(r'^admin/', admin.site.urls),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^change-password/', views.change_password, name='change_password'),
    url(r'^changefile/', views.changefile, name='changefile'),
]
#url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^change-password/', views.change_password, name='change_password'),
    url(r'^changefile/', views.changefile, name='changefile'),
    url(r'^mycentral/', views.mycentral, name='mycentral'),
    url(r'^keep/(?P<book_id>[0-9]+)/', views.keep, name='keep'),
    url(r'^keeplist/', views.keeplist, name='keeplist'),
    url(r'^cancel/(?P<book_id>[0-9]+)/', views.cancel, name='cancel'),
    url(r'^recommend/', views.recommend, name='recommend'),
    url(r'^recommendlist/', views.recommendlist, name='recommendlist'),
    url(r'^cancelbook/(?P<book_id>[0-9]+)/', views.cancelbook, name='cancelbook'),
    url(r'^feedback/', views.feedback, name='feedback'),
    url(r'^book/(?P<book_id>[0-9]+)/', views.book, name='book'),
    url(r'^discuss/', views.discuss, name='discuss'),
    url(r'^get-client-ip/', views.get_client_ip, name='get_client_ip'),
    url(r'^rate/(?P<book_id>[0-9]+)/', views.rate, name='rate'),
    url(r'^cancelcomment/(?P<book_id>[0-9]+)/(?P<comment_id>[0-9]+)', views.cancelcomment, name='cancelcomment'),
    url(r'^commentavaliable/(?P<book_id>[0-9]+)/(?P<comment_id>[0-9]+)', views.commentavaliable, name='commentavaliable'),
    url(r'^unavaliable/(?P<book_id>[0-9]+)/(?P<comment_id>[0-9]+)', views.unavaliable, name='unavaliable'),
    url(r'^classify/(?P<type_id>[0-9]+)/', views.classify, name='classify'),
]
#url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

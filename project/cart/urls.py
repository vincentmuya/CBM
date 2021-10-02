from django.conf.urls import url
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^cart$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^check_out$', views.check_out, name='check_out'),
    url(r'^shipping_info$', views.buyer_info, name='buyer_info'),

]

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url("register", views.register_request, name="register"),
    url("login", views.login_request, name="login"),
    url("logout", views.logout_request, name="logout"),
    # url("register", views.register, name="register"),
    url(r'^sale$', views.on_sale, name='on_sale'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.comp_detail, name='comp_detail'),
    url(r'^(?P<compcategory_slug>[-\w]+)/$', views.category, name='computer_list_by_compcategory'),
    url(r'^search$', views.search_results, name='search_results'),
    url('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    url('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    url("password_reset", views.password_reset_request, name="password_reset"),
    url("digital/press", views.digital_press, name="digital_press"),
    url("lenovo", views.lenovo, name="lenovo"),
    url("dell", views.dell, name="dell"),
    url("hp", views.hp, name="hp"),
    url("anviz", views.anviz, name="anviz"),
    url("software", views.software, name="software"),
    url("apc", views.apc, name="apc"),
    url("quote", views.quote, name="quote"),
    url("request/info", views.request_info, name="request_info"),
    url("received", views.received, name="received"),
    url("new/product", views.new_product, name="new_product"),
    url("aruba", views.arubahpe, name="arubahpe"),
    url("giganet", views.giganet, name="giganet"),
    url(r'^update/(?P<id>\d+)', views.update_item, name="update"),
    url(r'^delete/(?P<id>\d+)', views.delete, name="delete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

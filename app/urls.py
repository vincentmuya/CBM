from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sale$', views.on_sale, name='on_sale'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    url(r'^search$', views.search_results, name='search_results'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='product_list_by_category'),
    url("register", views.register_request, name="register"),
    url("login", views.login_request, name="login"),
    url("logout", views.logout_request, name="logout"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

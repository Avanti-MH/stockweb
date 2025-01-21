from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_home, name='index_home'),
    path('distance_method', views.html_interface, name='html_interface'),
    path('etf_rsi', views.html_interface, name='html_interface'),
    path('backtrader', views.html_interface, name='html_interface'),
    path('pricing', views.html_interface, name='html_interface'),
    path('tracker', views.html_interface, name='html_interface'),
    path('delete', views.html_interface, name='html_interface'),
    path('subscription', views.html_interface, name='html_interface'),
    #path('distance_method', views.index_distance_method, name='index_distance_method'),
    #path('etf_rsi', views.index_etf, name='index_etf'),
]
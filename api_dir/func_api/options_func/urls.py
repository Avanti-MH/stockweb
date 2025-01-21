from django.urls import path
from . import views

urlpatterns = [
    #path('csrf/', views.set_csrf_cookie, name='set_csrf_cookie'),
    path('distance_method_api', views.distance_method_api, name='distance_method_api'),
    path('api/strategies/', views.StrategyListView.as_view(), name='strategy-list'),
    path('api/strategies/<str:strategy_name>/run/', views.RunStrategyView.as_view(), name='run-strategy'),
]
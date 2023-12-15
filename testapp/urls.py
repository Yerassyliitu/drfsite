from django.urls import path

from . import views


urlpatterns = [
    path('auth/login/', views.MyLoginView.as_view(), name='login'),
    path('auth/logout/', views.MyLogoutView.as_view(), name='logout'),
    path('restaurant/create', views.RestaurantCreateView.as_view(), name='restaurant_create'),
    path('image/create/', views.ImageCreateView.as_view(), name='image_create'),
    path('restaurant/all', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>/delete', views.RestaurantDeleteView.as_view(), name='restaurant_delete'),
    path('restaurant/<int:pk>/edit', views.RestaurantEditView.as_view(), name='restaurant_edit'),
    path('order/<str:status>', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
]

from django.urls import path

from Cart import views

app_name = 'Cart'

urlpatterns = [
    path('toggle/', views.ToggleCart.as_view(), name='toggle_cart'),
]
from django.urls import path

from Cart import views

app_name = 'cart'

urlpatterns = [
    path('toggle/', views.ToggleCart.as_view(), name='toggle_cart'),
    path('items/', views.CartItemsView.as_view(), name='items'),
]
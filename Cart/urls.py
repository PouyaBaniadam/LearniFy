from django.urls import path

from Cart import views

app_name = 'cart'

urlpatterns = [
    path('toggle/', views.ToggleCart.as_view(), name='toggle_cart'),
    path('items/', views.CartItemsView.as_view(), name='items'),
    path('discount/apply/', views.ApplyDiscount.as_view(), name='apply_discount'),
    path('delete/<str:course_type>/<int:course_id>', views.DeleteItemFromCartItemsPage.as_view(), name='delete_from_cart_page'),
    path('deposit/slip/add/', views.AddDepositSlipView.as_view(), name='add_deposit_slip'),
]

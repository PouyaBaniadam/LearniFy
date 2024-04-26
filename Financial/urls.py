from django.urls import path

from Financial import views

app_name = 'financial'

urlpatterns = [
    path('cart/toggle/', views.ToggleCart.as_view(), name='toggle_cart'),
    path('cart/items/', views.CartItemsView.as_view(), name='cart_items'),
    path('cart/discount/apply/', views.ApplyDiscount.as_view(), name='apply_discount_for_cart'),
    path('cart/delete/<str:course_type>/<int:course_id>', views.DeleteItemFromCartItemsPage.as_view(),
         name='delete_from_cart_page'),
    path('deposit/slip/add/', views.AddDepositSlipView.as_view(), name='add_deposit_slip'),
]

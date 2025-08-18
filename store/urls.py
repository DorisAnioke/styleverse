from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # --- Home and Search ---
    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),

    # --- Product and Category ---
    path('products/', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category'),

    # --- Cart ---
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),

    # --- Checkout and Order ---
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),

    # --- Order History and Tracking ---
    path('order-history/', views.order_history, name='order_history'),
    path('track/', views.order_tracking_view, name='order_tracking'),

    # --- Reviews ---
    path('my-reviews/', views.user_reviews, name='user_reviews'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('submit-review-from-order/<int:product_id>/', views.submit_review_from_order, name='submit_review_from_order'),

    # --- Wishlist ---
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
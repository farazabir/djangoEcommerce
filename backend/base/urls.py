from django.urls import include, path
from base.views import OrderApiView, OrderItemListCreateApiView, OrderListCreateAPIView, ProductApiView, ProductListCreateAPIView, checkoutSession, stripe_webhook
import user.urls


urlpatterns = [
    path('products', ProductListCreateAPIView.as_view()),
    path('products/<pk>', ProductApiView.as_view()),
    path('orders', OrderListCreateAPIView.as_view()),
    path('orders/<pk>', OrderApiView.as_view()),
    path('order-item', OrderItemListCreateApiView.as_view()),
    path('checkout', checkoutSession.as_view()),
    path('stripe_webhooks', stripe_webhook.as_view()),
    path('', include("user.urls"))
]

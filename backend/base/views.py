import json
from django.conf import settings
from rest_framework.generics import DestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from .serializers import OrderItemSerializer, OrderSerializer, ProductSerializer
from base.models import Order, OrderItem, Product
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = "whsec_d58820d6dc04d88ef528859db6c3c7be5507919f0c6d0ad87034ec25e6a269fe"


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductApiView(RetrieveAPIView, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderApiView(DestroyAPIView, RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemListCreateApiView(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class checkoutSession(APIView):
    def post(self, request):
        data = request.data
        cart = data['cart']
        # print("Cart", cart)
        items = []
        for item in cart:
            items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                    },
                    'unit_amount': int(float(item['price'])*100)
                },
                'quantity': item['quantity']
            })
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url='http://localhost:3000',
            cancel_url='http://localhost:3000/cart'
        )

        print(checkout_session.url)
        response = Response()
        response.data = {
            "message": "success",
            "url": checkout_session.url
        }

        return response


class stripe_webhook(APIView):
    def post(self, request):
        payload = request.body
        print(payload)
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response(status=400)

        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object
        else:
            print('Unhandled event type {}'.format(event.type))

        return Response(status=200)

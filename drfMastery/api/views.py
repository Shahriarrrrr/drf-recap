from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView



class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt = 0)
    serializer_class = ProductSerializer


class ProductDetailApiView(generics.RetrieveAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        lookup_url_kwarg = 'product_id' # if in url <int:pk> is not there but any other name then this is what i have to do, Look in the urls.py


class OrderListApiView(generics.ListAPIView):
      queryset = Order.objects.prefetch_related('items__product')
      serializer_class = OrderSerializer
      

class UserOrderListApiView(generics.ListAPIView):
      queryset = Order.objects.prefetch_related('items__product')
      serializer_class = OrderSerializer
      permission_classes= [IsAuthenticated]

      def get_queryset(self):
            user = self.request.user
            qs = super().get_queryset()
            return qs.filter(user = user)
            return user.accounts.all()


class ProductInfoAPIView(APIView):
      def get(self, request):
            products = Product.objects.all()
            serializer = ProductInfoSerializer({
                  'products' : products,
                  'count' : len(products),
                  'max_price': products.aggregate(max_price=Max('price'))['max_price']

            })
            return Response (serializer.data)


#Old Function Based Views

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)
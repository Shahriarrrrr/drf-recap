from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.views import APIView
from .filters import ProductFilter, InStockFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class ProductListCreateApiView(generics.ListCreateAPIView):
      queryset = Product.objects.all()
      serializer_class = ProductSerializer
      filterset_class = ProductFilter
      filter_backends = [DjangoFilterBackend,
                        filters.SearchFilter,
                        filters.OrderingFilter,
                        InStockFilterBackend
                        ]
      search_fields = ['name', 'description', '=price']
      ordering_fields = ['name', 'price', 'stock']

      def get_permissions(self):
            self.permission_classes = [AllowAny]
            if self.request.method == 'POST':
                  self.permission_classes = [IsAdminUser]
            return super().get_permissions()




#Combined the list and create together by ListCreateAPIView
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
      queryset = Product.objects.all()
      serializer_class = ProductSerializer
      lookup_url_kwarg = 'product_id'
      def get_permissions(self):
            self.permission_classes = [AllowAny]
            if self.request.method in ['PATCH', 'PUT', 'DELETE']:
                  self.permission_classes = [IsAdminUser]

            return super().get_permissions()

# class ProductDetailApiView(generics.RetrieveAPIView):
#         queryset = Product.objects.all()
#         serializer_class = ProductSerializer
#         lookup_url_kwarg = 'product_id' # if in url <int:pk> is not there but any other name then this is what i have to do, Look in the urls.py


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
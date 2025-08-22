from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# --- Product List ---
@swagger_auto_schema(
    method="get",
    operation_description="Retrieve all products",
    responses={200: ProductSerializer(many=True)}
)

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(
        products, 
        many = True
    )
    return Response(serializer.data)


# --- Single Product ---
@swagger_auto_schema(
    method="get",
    operation_description="Retrieve a single product by ID",
    # manual_parameters=[
    #     openapi.Parameter(
    #         "pk", openapi.IN_PATH,
    #         description="ID of the product to retrieve",
    #         type=openapi.TYPE_INTEGER
    #     )
    # ],
    responses={200: ProductSerializer()}
)

@api_view(['GET'])
def single_product(request,pk):
    products = get_object_or_404(Product, pk = pk)
    serializer = ProductSerializer(
        products, 
    )
    return Response(serializer.data)



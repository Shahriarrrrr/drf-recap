from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('products/', views.ProductListCreateApiView.as_view()),
    # path('products/create/', views.ProductCreateAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailApiView.as_view()),
    # path('orders/', views.OrderListApiView.as_view()),
    # path('user-orders/', views.UserOrderListApiView.as_view(), name='user-orders'),
    path('products/info/', views.ProductInfoAPIView.as_view()),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls 
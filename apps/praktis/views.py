# from django.shortcuts import render
# from  rest_framework import generics,permissions,status,filters
# from .models import Product
# from .serializers import ProductSerializer


# class ProductListCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductDetailView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class CartItemListCreateView(generics.ListCreateAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         queryset = CartItem.object.select_related('product','product_size')
    
#         return queryset.order_by(-created_at)
    
#     def perform_create(self, serializer):
#         cart, _ =Cart.objects.get_or_create(user=self.request.user)
#         serializer.save(cart=cart)


# class CartItemListCreateView(generics.ListCreateAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return CartItem.objects.filter(cart__user=self.request.user).select_related('product','product_size').order_by('added_at')
    
#     def perform_create(self, serializer):
#         cart, _ = Cart.objects.get_or_create(user=self.request.user)
#         serializer.save(cart=cart)


# class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CartItemSerializer
#     permissions_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return CartItem.objets.filter(cart__user=self.request.user).select_related('product','product_size').order_by('added_at')
    
# @api_view(['GET'])
# @permissions_classes([AllowAny])
#     def popular_posts(request):
#         posts= Post.objects.filter(status='published').order_by('-views_count')[:10]
#         serializer = PostListSerializer(posts,many=True)
#         return Response(serializer.data)    
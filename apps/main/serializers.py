from rest_framework import serializers
from slugify import slugify
from .models import Product,ProductImage,ProductSize,Size,Category

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','name','slug','products_count']
        read_only_fields = ['slug']

    def get_products_count(self,obj):
        return obj.products.count()
    
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)   
    
    def update(self,instance,validated_data):
        validated_data['slug'] = slugify(validated_data.get('name'.instance.name))
        return super().update(instance,validated_data)
    
class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


class ProductSizeSerializer(serializers.ModelSerializer):
    size = SizeSerializer()  # вкладений серіалізатор

    class Meta:
        model = ProductSize
        fields = ['size', 'stock']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryShortSerializer(read_only=True)
    sizes = ProductSizeSerializer(source='product_sizes', many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','name','slug','category','color',
                  'price','description','main_image',
                  'created_at','updated_at','likes_count']
        read_only_fields = ['slug','created_at']

    def get_likes_count(self,obj):
        return obj.likes.count()
    

    def get_is_liked(self,obj):
        request = self.context.get('request')
        if request and request.user.is_autheticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False



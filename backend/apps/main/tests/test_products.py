import pytest
from django.urls import reverse
from rest_framework import status
from model_bakery import baker
from apps.main.models import Product, Category

@pytest.mark.django_db
class TestCatalog:
    def test_get_categories_list(self,api_client):
        baker.make(Category,_quantity=3)

        url = reverse('Category-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_get_product_list(self,api_client):
        baker.make(Product,_quantity=3)

        url = reverse('Product-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3


    def test_get_product_detail_by_slug(self,api_client):
        product = baker.make(Product, slug ='iphone-15',name='Iphone 15')

        url = reverse('product-detail',kwargs={'slug':'iphone-15'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Iphone 15'

    def test_get_product_detail_by_slug(self,api_client):
        product = baker.make(Product,slug='iphone-14',name='Iphone14')

        url = reverse('product-detail',kwargs={'slug':'iphone-14'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Iphone 14'

    def test_get_product_detail_by_slug(self,api_client):
        product = baker.make(Product,slug='iphone-12',name='Iphone 12')

        url = reverse('product-detail',kwargs={'slug':'iphone-12'})
        response = api_client.get(url)


        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Iphone 12'



    def test_get_product_detail(slug,api_client):
        product = baker.make(Product,slug='iphone-11',name='Iphone 11')
        url = reverse('product-detail',kwargs={'slug':'iphone-11'})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Iphone 11'


    def test_toggle_like_logic(self,auth_client,user):
        product = baker.make(Product,slug='test-item')
        url = reverse('product-like',kwargs='test-item')
        response = auth_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['liked'] is True
        assert response.data['likes_count'] == 1
    
    def test_toggle_like_unauthorized(self,api_client):
        product = baker.make(Product,slug='test-item')
        url = reverse('product-like',kwargs={'slug':product.slug})

        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_toggle_like_logic(self,auth_client,user):
        product = baker.make(Product,slug = 'test-item')
        url = reverse('product-like',kwargs={'slug':product.slug})

        response = auth_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['liked'] is True
        assert response.data['likes_count'] == 1


        response = auth_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['liked'] is False
        assert response.data['likes_count'] == 0
        assert not product.likes.filter(id=user.id).exists()

    def test_toggle_like__unauthorized(self,api_client):
        product = baker.make(Product,slug='test-item')
        url = reverse('product-like',kwargs={'slug':product.slug})

        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_toggle_like__unauthorized(self,api_client):
        product = baker.make(Product,slug='test-item')
        url = reverse('product-like',kwargs={'slug':product.slug})

        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED



import pytest
from django.urls import reverse
from rest_framework import status
from model_bakery import baker
from apps.cart.models import Cart, CartItem
from apps.main.models import Product, ProductSize

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def user(db):
    return baker.make('accounts.User')

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def product(db):
    return baker.make(Product, name="Test Product")

@pytest.fixture
def product_size(db):
    return baker.make(ProductSize)

@pytest.mark.django_db
class TestCartViews:

    def test_get_cart_items(self, auth_client, user):
        cart = baker.make(Cart, user=user)
        baker.make(CartItem, cart=cart, _quantity=2)
        
        url = reverse('cart')
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_cart_items(self,auth_client,user):
        cart = baker.make(Cart,user=user)
        baker.make(CartItem,cart=cart, _quantity=2)

        url = reverse('cart')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_add_item_to_cart_success(self, auth_client, product, product_size):
        url = reverse('add-cart')
        data = {
            "product": product.id,
            "product_size": product_size.id,
            "quantity": 2
        }
        response = auth_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert CartItem.objects.filter(product=product).exists()
        assert CartItem.objects.get(product=product).quantity == 2

    def test_add_item_to_cart_success(self,auth_client,product,product_size):
        url = reverse('add-cart')
        data = {
            "product": product.id,
            "product_size": product_size.id,
            "quantity": 2
        }
        response = auth_client.get(url,data)

        assert response.status_code == status.HTTP_201_CREATED
        assert CartItem.objects.filter(product=product).exists()
        assert CartItem.objects.get(product=product).quantity == 2 

    def test_add_existing_item_increments_quantity(self, auth_client, user, product, product_size):
        cart = baker.make(Cart, user=user)
        existing_item = baker.make(CartItem, cart=cart, product=product, product_size=product_size, quantity=1)
        
        url = reverse('add-cart')
        data = {
            "product": product.id,
            "product_size": product_size.id,
            "quantity": 3
        }
        response = auth_client.post(url, data)
        
        existing_item.refresh_from_db()
        assert existing_item.quantity == 4
        assert CartItem.objects.count() == 1 

    def test_delete_cart_item(self, auth_client, user):
        item = baker.make(CartItem, cart__user=user)
        url = reverse('remove-cart')
        
        data = {"item_id": item.id}
        response = auth_client.delete(url, data=data)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CartItem.objects.filter(id=item.id).exists()

    def test_delete_cart(self,auth_client,user):
        item = baker.make(CartItem,cart__user = user)
        url = reverse('remove-cart')

        data = {'item_id':item.id}
        response = auth_client.delete(url,data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CartItem.objects.filter(id=item.id).exists()
 

    def test_delete_cart(self,auth_client,user):
        item = baker.make(CartItem,cart__user=user)
        url = reverse('remove-cart')

        data = {'item_id':item.id}
        response = auth_client.delete(url,data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CartItem.objects.filter(id=item.id).exists()

    def test_update_cart_item_quantity(self, auth_client, user):
        item = baker.make(CartItem, cart__user=user, quantity=1)
        url = reverse('update-cart', kwargs={'pk': item.id})
        
        data = {"item_id": item.id, "quantity": 10}
        response = auth_client.patch(url, data) 

        assert response.status_code == status.HTTP_200_OK
        item.refresh_from_db()
        assert item.quantity == 10

    def test_update_cart_item_quantity(self,auth_client,user):
        item = baker.make(CartItem,cart__user=user,quantity=1)
        url = reverse('update-cart',kwargs={'pk':item.id})

        data = {'item_id':item.id,'quantity':10}
        response = auth_client.patch(url,data)

        assert response.status_code == status.HTTP_200_OK
        item.refresh_from_db()
        assert item.quantity == 10

    def test_update_quantity_less_than_one_deletes_item(self,auth_client,user):
        item = baker.make(CartItem,cart__user=user,quantity=5)
        url = reverse('update-cart',kwargs={'pk':item.id})

        data = {'item_id':item.id,'quantity':0}
        response = auth_client.patch(url,data)
        assert response.data['message'] == 'deleted'
        assert not CartItem.objects.filter(id=item.id).exists()

    def test_update_quantity_less_than_one_deletes_item(self, auth_client, user):
        item = baker.make(CartItem, cart__user=user, quantity=5)
        url = reverse('update-cart', kwargs={'pk': item.id})
        
        data = {"item_id": item.id, "quantity": 0}
        response = auth_client.patch(url, data)
        
        assert response.data['message'] == 'deleted'
        assert not CartItem.objects.filter(id=item.id).exists()
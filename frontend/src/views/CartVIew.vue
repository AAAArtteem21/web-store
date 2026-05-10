<!-- frontend/src/views/CartView.vue -->
<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()

const total = computed(() =>
  cart.items.reduce((sum, item) => sum + parseFloat(item.product_price) * item.quantity, 0)
)

async function checkout() {
  if (!auth.isAuthenticated) {
    router.push('/login?redirect=/cart')
    return
  }
  try {
    const { data } = await api.post('/api/v1/order/orders/create-from-cart/')
    console.log('ORDER DATA:', data)  // ← добавь
    router.push(`/checkout/${data.order_id}`)
  } catch (e) {
    console.log('CHECKOUT ERROR:', e.response?.data)
    alert('Ошибка при создании заказа')
  }
}
</script>

<template>
  <div class="cart-page">
    <h1 class="page-title">Корзина</h1>

    <div v-if="cart.items.length === 0" class="empty">
      <div class="empty-icon">🛒</div>
      <p>Корзина пуста</p>
      <button class="btn btn-primary" style="margin-top:1.5rem" @click="router.push('/')">
        Перейти в каталог
      </button>
    </div>

    <div v-else class="cart-layout">
      <!-- Список товаров -->
      <div class="cart-items">
        <div
          v-for="item in cart.items"
          :key="item.id"
          class="cart-item card"
        >
          <div class="item-img" @click="router.push(`/product/${item.product_slug}`)">
            <img v-if="item.product_image" :src="item.product_image" :alt="item.product_name" />
            <div v-else class="img-placeholder">🛍</div>
          </div>

          <div class="item-info">
            <p class="item-category">{{ item.product_category }}</p>
            <h3 class="item-name" @click="router.push(`/product/${item.product_slug}`)">
              {{ item.product_name }}
            </h3>
            <p class="item-size">Размер: {{ item.size_name }}</p>
          </div>

          <div class="item-controls">
            <div class="qty-controls">
              <button class="qty-btn" @click="cart.updateItem(item.id, item.quantity - 1)">−</button>
              <span class="qty-value">{{ item.quantity }}</span>
              <button class="qty-btn" @click="cart.updateItem(item.id, item.quantity + 1)">+</button>
            </div>
            <p class="item-price">${{ (parseFloat(item.product_price) * item.quantity).toFixed(2) }}</p>
            <button class="remove-btn" @click="cart.removeItem(item.id)">✕</button>
          </div>
        </div>
      </div>

      <!-- Итого -->
      <div class="cart-summary card">
        <h2 class="summary-title">Итого</h2>

        <div class="summary-rows">
          <div class="summary-row" v-for="item in cart.items" :key="item.id">
            <span>{{ item.product_name }} × {{ item.quantity }}</span>
            <span>${{ (parseFloat(item.product_price) * item.quantity).toFixed(2) }}</span>
          </div>
        </div>

        <div class="summary-divider" />

        <div class="summary-total">
          <span>Итого</span>
          <span>${{ total.toFixed(2) }}</span>
        </div>

        <button class="btn btn-primary checkout-btn" @click="checkout">
          Оформить заказ →
        </button>

        <button class="btn btn-secondary continue-btn" @click="router.push('/')">
          Продолжить покупки
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-page {
  max-width: 1100px;
  margin: 0 auto;
}

.empty {
  text-align: center;
  padding: 5rem 2rem;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.cart-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 768px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  display: grid;
  grid-template-columns: 90px 1fr auto;
  gap: 1.25rem;
  align-items: center;
  padding: 1rem;
}

@media (max-width: 500px) {
  .cart-item {
    grid-template-columns: 70px 1fr;
    grid-template-rows: auto auto;
  }
  .item-controls {
    grid-column: 1 / -1;
  }
}

.item-img {
  width: 90px;
  height: 90px;
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg-card2);
  cursor: pointer;
  flex-shrink: 0;
}

.item-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.item-img:hover img {
  transform: scale(1.05);
}

.img-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: var(--text-muted);
}

.item-info {
  min-width: 0;
}

.item-category {
  font-size: 0.75rem;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.2rem;
}

.item-name {
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0.3rem;
}

.item-name:hover {
  color: var(--primary);
}

.item-size {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.item-controls {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.75rem;
}

.qty-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.qty-btn {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text);
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.qty-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.qty-value {
  font-weight: 700;
  min-width: 20px;
  text-align: center;
}

.item-price {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--primary);
}

.remove-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0.2rem;
  transition: color 0.2s;
}

.remove-btn:hover {
  color: var(--error, #e53e3e);
}

.cart-summary {
  padding: 1.75rem;
  position: sticky;
  top: 1rem;
}

.summary-title {
  font-size: 1.3rem;
  font-weight: 800;
  margin-bottom: 1.25rem;
}

.summary-rows {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.summary-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1rem 0;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
}

.checkout-btn {
  width: 100%;
  padding: 0.9rem;
  margin-bottom: 0.75rem;
}

.continue-btn {
  width: 100%;
  padding: 0.75rem;
  font-size: 0.9rem;
}
</style>
<!-- frontend/src/views/CheckoutView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()

const order = ref(null)
const loading = ref(true)
const paying = ref(false)

async function fetchOrder() {
  loading.value = true
  try {
    const { data } = await api.get(`/api/v1/order/orders/${route.params.orderId}/`)  // ← исправлено
    order.value = data
  } catch {
    order.value = null
  } finally {
    loading.value = false
  }
}

async function pay() {
  paying.value = true
  try {
    const { data } = await api.post(`/api/payment/checkout/${route.params.orderId}/`)
    window.location.href = data.checkout_url
  } catch {
    alert('Ошибка при создании сессии оплаты')
    paying.value = false
  }
}
onMounted(fetchOrder)
</script>

<template>
  <div class="checkout-page">
    <button class="back-btn" @click="router.push('/cart')">← Назад в корзину</button>

    <h1 class="page-title">Оформление заказа</h1>

    <div v-if="loading" class="spinner" />

    <div v-else-if="!order" class="empty">
      <p>😕 Заказ не найден</p>
    </div>

    <div v-else class="checkout-layout">
      <!-- Состав заказа -->
      <div class="order-items card">
        <h2 class="section-title">Ваш заказ #{{ order.id }}</h2>

        <div class="items-list">
          <div
            v-for="item in order.items"
            :key="item.id"
            class="order-item"
          >
            <div class="oi-img">
              <img v-if="item.image" :src="item.image" :alt="item.name" />
              <div v-else class="img-placeholder">🛍</div>
            </div>
            <div class="oi-info">
              <p class="oi-name">{{ item.name }}</p>
              <p class="oi-meta">Размер: {{ item.size }} · Кол-во: {{ item.quantity }}</p>
            </div>
            <p class="oi-price">${{ (item.price * item.quantity).toFixed(2) }}</p>
          </div>
        </div>
      </div>

      <!-- Оплата -->
      <div class="payment-panel card">
        <h2 class="section-title">Оплата</h2>

        <div class="summary-rows">
          <div class="summary-row">
            <span>Товары</span>
            <span>${{ order.total_price }}</span>
          </div>
          <div class="summary-row">
            <span>Доставка</span>
            <span class="free">Бесплатно</span>
          </div>
        </div>

        <div class="summary-divider" />

        <div class="summary-total">
          <span>Итого</span>
          <span>${{ order.total_price }}</span>
        </div>

        <div class="payment-badge">
          <span>🔒</span>
          <span>Безопасная оплата через Stripe</span>
        </div>

        <button
          class="btn btn-primary pay-btn"
          :disabled="paying"
          @click="pay"
        >
          {{ paying ? 'Перенаправляем...' : '💳 Оплатить' }}
        </button>

        <p class="payment-note">
          Нажимая «Оплатить», вы соглашаетесь с условиями обработки платежей через Stripe
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.checkout-page {
  max-width: 960px;
  margin: 0 auto;
}

.back-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: var(--primary);
}

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 768px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
}

.section-title {
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
}

.order-items {
  padding: 1.75rem;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.order-item {
  display: grid;
  grid-template-columns: 64px 1fr auto;
  gap: 1rem;
  align-items: center;
}

.oi-img {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-card2);
  flex-shrink: 0;
}

.oi-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.img-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--text-muted);
}

.oi-name {
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.oi-meta {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.oi-price {
  font-weight: 800;
  color: var(--primary);
  white-space: nowrap;
}

/* Payment panel */
.payment-panel {
  padding: 1.75rem;
  position: sticky;
  top: 1rem;
}

.summary-rows {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.free {
  color: var(--success, #48bb78);
  font-weight: 600;
}

.summary-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1rem 0;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  font-size: 1.3rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
}

.payment-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  background: var(--bg-card2);
  border-radius: 8px;
  padding: 0.6rem 0.9rem;
  margin-bottom: 1rem;
}

.pay-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.payment-note {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-align: center;
  line-height: 1.5;
}

.empty {
  text-align: center;
  padding: 4rem;
  color: var(--text-muted);
}
</style>
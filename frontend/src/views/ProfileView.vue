<!-- frontend/src/views/ProfileView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const router = useRouter()
const auth = useAuthStore()

const orders = ref([])
const loadingOrders = ref(true)
const activeTab = ref('orders')

async function fetchOrders() {
  loadingOrders.value = true
  try {
    const { data } = await api.get('/api/v1/order/orders/')
    console.log('ORDERS:', data)
    orders.value = Array.isArray(data) ? data : data.results || []
  } catch {
    orders.value = []
  } finally {
    loadingOrders.value = false
  }
}

function logout() {
  auth.logout()
  router.push('/')
}

const statusLabel = {
  pending: 'Ожидает оплаты',
  paid: 'Оплачен',
  shipped: 'Отправлен',
  delivered: 'Доставлен',
  cancelled: 'Отменён',
}

const statusClass = {
  pending: 'status-pending',
  paid: 'status-paid',
  shipped: 'status-shipped',
  delivered: 'status-delivered',
  cancelled: 'status-cancelled',
}

onMounted(fetchOrders)
</script>

<template>
  <div class="profile-page">
    <!-- Шапка профиля -->
    <div class="profile-header card">
      <div class="avatar">{{ auth.user?.username?.[0]?.toUpperCase() || '?' }}</div>
      <div class="profile-info">
        <h1 class="profile-name">{{ auth.user?.username }}</h1>
        <p class="profile-email">{{ auth.user?.email }}</p>
      </div>
      <button class="btn btn-secondary logout-btn" @click="logout">Выйти</button>
    </div>

    <!-- Табы -->
    <div class="tabs">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'orders' }"
        @click="activeTab = 'orders'"
      >
        Мои заказы
      </button>
    </div>

    <!-- Заказы -->
    <div v-if="activeTab === 'orders'">
      <div v-if="loadingOrders" class="spinner" />

      <div v-else-if="orders.length === 0" class="empty">
        <div class="empty-icon">📦</div>
        <p>У вас пока нет заказов</p>
        <button class="btn btn-primary" style="margin-top:1.5rem" @click="router.push('/')">
          Перейти в каталог
        </button>
      </div>

      <div v-else class="orders-list">
        <div
          v-for="order in orders"
          :key="order.id"
          class="order-card card"
        >
          <div class="order-header">
            <div>
              <p class="order-num">Заказ #{{ order.id }}</p>
              <p class="order-date">{{ new Date(order.created_at).toLocaleDateString('ru-RU') }}</p>
            </div>
            <div class="order-right">
              <span class="status-badge" :class="statusClass[order.status]">
                {{ statusLabel[order.status] || order.status }}
              </span>
              <p class="order-total">${{ order.total_price }}</p>
            </div>
          </div>

          <div class="order-items">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="order-item"
            >
              <div class="oi-img">
                <img v-if="item.product_image" :src="item.product_image" :alt="item.product_name" />
                <div v-else class="img-placeholder">🛍</div>
              </div>
              <div class="oi-info">
                <p class="oi-name">{{ item.product_name }}</p>
                <p class="oi-meta">Размер: {{ item.size_name }} · {{ item.quantity }} шт.</p>
              </div>
              <p class="oi-price">${{ (item.price * item.quantity).toFixed(2) }}</p>
            </div>
          </div>

          <div v-if="order.status === 'pending'" class="order-actions">
            <button
              class="btn btn-primary btn-sm"
              @click="router.push(`/checkout/${order.id}`)"
            >
              Оплатить →
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.75rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 500px) {
  .profile-header {
    flex-wrap: wrap;
  }
  .logout-btn {
    width: 100%;
  }
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  font-size: 1.8rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 1.4rem;
  font-weight: 800;
  margin-bottom: 0.2rem;
}

.profile-email {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.logout-btn {
  margin-left: auto;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.tab-btn {
  background: none;
  border: none;
  padding: 0.75rem 1.25rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.2s;
}

.tab-btn.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

/* Orders */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.order-card {
  padding: 1.5rem;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

.order-num {
  font-weight: 800;
  margin-bottom: 0.25rem;
}

.order-date {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.order-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.status-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-pending  { background: #fef3c7; color: #92400e; }
.status-paid     { background: #d1fae5; color: #065f46; }
.status-shipped  { background: #dbeafe; color: #1e40af; }
.status-delivered{ background: #d1fae5; color: #065f46; }
.status-cancelled{ background: #fee2e2; color: #991b1b; }

.order-total {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--primary);
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.order-item {
  display: grid;
  grid-template-columns: 56px 1fr auto;
  gap: 1rem;
  align-items: center;
}

.oi-img {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-card2);
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
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

.oi-meta {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.oi-price {
  font-weight: 700;
  color: var(--primary);
  font-size: 0.95rem;
  white-space: nowrap;
}

.order-actions {
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
}

.btn-sm {
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
}

.empty {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}
</style>
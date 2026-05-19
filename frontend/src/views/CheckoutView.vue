<!-- frontend/src/views/CheckoutView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const order = ref(null)
const loading = ref(true)
const paying = ref(false)
const savingAddress = ref(false)
const step = ref(1)

const address = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  company: '',
  address1: '',
  address2: '',
  city: '',
  country: '',
  province: '',
  postal_code: '',
  special_instructions: '',
})

async function fetchOrder() {
  loading.value = true
  try {
    const { data } = await api.get(`/api/v1/order/orders/${route.params.orderId}/`)
    order.value = data
    address.value.first_name = data.first_name || auth.user?.username || ''
    address.value.last_name = data.last_name || ''
    address.value.email = data.email || auth.user?.email || ''
    address.value.phone = data.phone || ''
    address.value.company = data.company || ''
    address.value.address1 = data.address1 || ''
    address.value.address2 = data.address2 || ''
    address.value.city = data.city || ''
    address.value.country = data.country || ''
    address.value.province = data.province || ''
    address.value.postal_code = data.postal_code || ''
    address.value.special_instructions = data.special_instructions || ''
  } catch {
    order.value = null
  } finally {
    loading.value = false
  }
}

async function saveAddress() {
  savingAddress.value = true
  try {
    await api.patch(`/api/v1/order/orders/${route.params.orderId}/`, address.value)
    step.value = 2
  } catch {
    alert('Ошибка при сохранении адреса')
  } finally {
    savingAddress.value = false
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
    <div v-else-if="!order" class="empty"><p>😕 Заказ не найден</p></div>

    <div v-else class="checkout-layout">
      <div class="left-col">

        <!-- Steps -->
        <div class="steps">
          <div class="step" :class="{ active: step === 1, done: step > 1 }" @click="step = 1">
            <div class="step-num">
              <svg v-if="step > 1" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
              <span v-else>1</span>
            </div>
            <span class="step-label">Доставка</span>
          </div>
          <div class="step-line" />
          <div class="step" :class="{ active: step === 2 }">
            <div class="step-num">2</div>
            <span class="step-label">Оплата</span>
          </div>
        </div>

        <!-- Step 1: Address -->
        <div v-if="step === 1" class="form-card card">
          <h2 class="section-title">Адрес доставки</h2>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Имя *</label>
              <input v-model="address.first_name" class="input" placeholder="Артём" />
            </div>
            <div class="form-group">
              <label class="form-label">Фамилия *</label>
              <input v-model="address.last_name" class="input" placeholder="Иванов" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Email *</label>
              <input v-model="address.email" type="email" class="input" placeholder="you@example.com" />
            </div>
            <div class="form-group">
              <label class="form-label">Телефон</label>
              <input v-model="address.phone" class="input" placeholder="+380..." />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Компания (необязательно)</label>
            <input v-model="address.company" class="input" placeholder="Название компании" />
          </div>

          <div class="form-group">
            <label class="form-label">Адрес *</label>
            <input v-model="address.address1" class="input" placeholder="ул. Примерная, 1" />
          </div>

          <div class="form-group">
            <label class="form-label">Квартира / офис (необязательно)</label>
            <input v-model="address.address2" class="input" placeholder="кв. 10" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Город *</label>
              <input v-model="address.city" class="input" placeholder="Киев" />
            </div>
            <div class="form-group">
              <label class="form-label">Страна *</label>
              <input v-model="address.country" class="input" placeholder="Украина" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Область</label>
              <input v-model="address.province" class="input" placeholder="Киевская" />
            </div>
            <div class="form-group">
              <label class="form-label">Индекс</label>
              <input v-model="address.postal_code" class="input" placeholder="01001" />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Комментарий к заказу</label>
            <textarea v-model="address.special_instructions" class="input textarea" placeholder="Особые пожелания..." />
          </div>

          <button class="btn-action" :disabled="savingAddress" @click="saveAddress">
            {{ savingAddress ? 'Сохраняем...' : 'Перейти к оплате →' }}
          </button>
        </div>

        <!-- Step 2: Order review -->
        <div v-if="step === 2" class="order-items card">
          <h2 class="section-title">Заказ #{{ order.id }}</h2>

          <div class="items-list">
            <div v-for="item in order.items" :key="item.id" class="order-item">
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

          <div class="address-summary">
            <div class="address-summary-header">
              <p class="address-summary-title">Адрес доставки</p>
              <button class="edit-btn" @click="step = 1">Изменить</button>
            </div>
            <p class="address-line">{{ address.first_name }} {{ address.last_name }}</p>
            <p v-if="address.address1" class="address-line">{{ address.address1 }}{{ address.address2 ? ', ' + address.address2 : '' }}</p>
            <p v-if="address.city" class="address-line">{{ address.city }}{{ address.postal_code ? ' ' + address.postal_code : '' }}{{ address.country ? ', ' + address.country : '' }}</p>
            <p v-if="address.phone" class="address-line">{{ address.phone }}</p>
          </div>
        </div>

      </div>

      <!-- Right: Payment -->
      <div class="payment-panel card">
        <h2 class="section-title">Итого</h2>

        <div class="summary-rows">
          <div v-for="item in order.items" :key="item.id" class="summary-row">
            <span class="summary-item-name">{{ item.product_name }} × {{ item.quantity }}</span>
            <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
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

        <template v-if="step === 2">
          <div class="payment-badge">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
            </svg>
            Безопасная оплата через Stripe
          </div>
          <button class="btn-action" :disabled="paying" @click="pay">
            {{ paying ? 'Перенаправляем...' : 'Оплатить' }}
          </button>
          <p class="payment-note">Нажимая «Оплатить», вы соглашаетесь с условиями обработки платежей через Stripe</p>
        </template>

        <template v-else>
          <button class="btn-action btn-disabled" disabled>Сначала укажите адрес</button>
        </template>
      </div>

    </div>
  </div>
</template>

<style scoped>
.checkout-page { width: 100%; }

.back-btn {
  background: none; border: none;
  color: var(--text-muted); cursor: pointer;
  font-size: 0.85rem; font-family: 'Inter', sans-serif;
  padding: 0; margin-bottom: 1.5rem;
  transition: color 0.2s; display: block;
}
.back-btn:hover { color: var(--primary); }

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 2rem;
  align-items: start;
}
@media (max-width: 900px) { .checkout-layout { grid-template-columns: 1fr; } }

.left-col { display: flex; flex-direction: column; gap: 1.5rem; }

/* Steps */
.steps {
  display: flex; align-items: center; gap: 0;
  background: white; border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem 1.5rem;
}

.step { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }

.step-num {
  width: 26px; height: 26px; border-radius: 50%;
  border: 1.5px solid var(--border-strong);
  background: white; color: var(--text-muted);
  font-size: 0.75rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.step.active .step-num { background: var(--primary); border-color: var(--primary); color: white; }
.step.done .step-num { background: var(--success); border-color: var(--success); color: white; }

.step-label { font-size: 0.82rem; font-weight: 600; color: var(--text-muted); }
.step.active .step-label { color: var(--primary); }
.step.done .step-label { color: var(--success); }

.step-line { flex: 1; height: 1px; background: var(--border); margin: 0 1rem; }

/* Form */
.form-card { padding: 1.75rem; }
.section-title {
  font-family: 'Syne', sans-serif; font-size: 1.1rem;
  font-weight: 700; margin-bottom: 1.5rem; color: var(--primary);
}

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
@media (max-width: 600px) { .form-row { grid-template-columns: 1fr; } }

.form-group { margin-bottom: 1rem; }

.form-label {
  display: block; font-size: 0.72rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px;
  color: var(--text-muted); margin-bottom: 0.4rem;
}

.textarea { resize: vertical; min-height: 80px; line-height: 1.5; }

.btn-action {
  width: 100%; padding: 1rem;
  background: var(--primary); color: white;
  border: none; border-radius: 8px;
  font-size: 0.95rem; font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer; transition: all 0.2s;
  margin-top: 0.5rem;
}
.btn-action:hover:not(:disabled) { background: #222; transform: translateY(-1px); }
.btn-action:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.btn-disabled { background: var(--bg-card2) !important; color: var(--text-muted) !important; }

/* Order items */
.order-items { padding: 1.75rem; }
.items-list { display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 1.5rem; }

.order-item { display: grid; grid-template-columns: 64px 1fr auto; gap: 1rem; align-items: center; }

.oi-img { width: 64px; height: 64px; border-radius: 8px; overflow: hidden; background: var(--bg-card2); }
.oi-img img { width: 100%; height: 100%; object-fit: cover; }
.img-placeholder { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: var(--text-muted); }

.oi-name { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.2rem; }
.oi-meta { font-size: 0.78rem; color: var(--text-muted); }
.oi-price { font-weight: 700; color: var(--primary); white-space: nowrap; font-size: 0.95rem; }

/* Address summary */
.address-summary { border-top: 1px solid var(--border); padding-top: 1.25rem; }
.address-summary-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; }
.address-summary-title { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); }
.edit-btn { background: none; border: none; color: var(--primary); font-size: 0.8rem; font-weight: 600; cursor: pointer; font-family: 'Inter', sans-serif; text-decoration: underline; }
.address-line { font-size: 0.85rem; color: var(--text-muted); line-height: 1.7; }

/* Payment panel */
.payment-panel { padding: 1.75rem; position: sticky; top: 1rem; }

.summary-rows { display: flex; flex-direction: column; gap: 0.6rem; margin-bottom: 1rem; }
.summary-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted); }
.summary-item-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px; }
.free { color: var(--success); font-weight: 600; }

.summary-divider { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

.summary-total { display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: 800; margin-bottom: 1.5rem; font-family: 'Syne', sans-serif; }

.payment-badge {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.78rem; color: var(--text-muted);
  background: var(--bg-card2); border-radius: 8px;
  padding: 0.6rem 0.9rem; margin-bottom: 1rem;
}

.payment-note { font-size: 0.72rem; color: var(--text-muted); text-align: center; line-height: 1.5; margin-top: 0.75rem; }

.empty { text-align: center; padding: 4rem; color: var(--text-muted); }
</style>
<!-- frontend/src/views/PaymentCancelView.vue -->
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="result-page">
    <div class="result-card card">
      <div class="result-icon cancel-icon">✕</div>
      <h1 class="result-title">Оплата отменена</h1>
      <p class="result-sub">
        Вы отменили оплату. Ваш заказ сохранён — вы можете вернуться и оплатить его позже.
      </p>

      <div class="result-actions">
        <button class="btn btn-primary" @click="router.push('/profile')">
          Мои заказы
        </button>
        <button class="btn btn-secondary" @click="router.push('/cart')">
          Вернуться в корзину
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.result-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.result-card {
  width: 100%;
  max-width: 460px;
  padding: 3rem 2.5rem;
  text-align: center;
}

.result-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 900;
  margin: 0 auto 1.5rem;
}

.cancel-icon {
  background: #fee2e2;
  color: #991b1b;
}

.result-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.75rem;
}

.result-sub {
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.result-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.result-actions .btn {
  width: 100%;
  padding: 0.9rem;
}
</style>
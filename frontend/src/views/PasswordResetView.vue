<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()

const email = ref('')
const sent = ref(false)
const loading = ref(false)

const isLoggedIn = !!localStorage.getItem('access_token')

async function submit() {
  loading.value = true
  try {
    await api.post('/api/v1/auth/password-reset/', { email: email.value })
  } finally {
    sent.value = true
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card">
      <div v-if="sent" style="text-align:center">
        <div style="font-size:3rem">📧</div>
        <h2 class="auth-title" style="margin-top:1rem">Письмо отправлено</h2>
        <p class="auth-sub">Если аккаунт с таким email существует — ссылка уже в пути</p>
        <RouterLink to="/" class="btn btn-primary submit-btn" style="display:block; margin-top:1.5rem">
            На главную
        </RouterLink>
      </div>

      <template v-else>
        <h2 class="auth-title">Сброс пароля</h2>
        <p class="auth-sub">Введи email — пришлём ссылку</p>

        <div class="form-group">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            class="input"
            placeholder="you@example.com"
            @keyup.enter="submit"
          />
        </div>

        <button class="btn btn-primary submit-btn" :disabled="loading" @click="submit">
          {{ loading ? 'Отправляем...' : 'Отправить ссылку' }}
        </button>

        <p class="auth-footer">
          <RouterLink to="/">← На главную</RouterLink>
        </p>
      </template>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
}

.auth-title {
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
}

.auth-sub {
  color: var(--text-muted);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 0.4rem;
}

.submit-btn {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.9rem;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.auth-footer a {
  color: var(--primary);
  font-weight: 600;
}
</style>
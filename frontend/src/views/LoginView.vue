<!-- frontend/src/views/LoginView.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const form = ref({ username: '', password: '' })

async function submit() {
  const ok = await auth.login(form.value.username, form.value.password)
  if (ok) {
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h2 class="auth-title">Вход</h2>
      <p class="auth-sub">Рады видеть тебя снова 👋</p>

      <div class="form-group">
        <label>Имя пользователя</label>
        <input
          v-model="form.username"
          class="input"
          placeholder="username"
          @keyup.enter="submit"
        />
      </div>

      <div class="form-group">
        <label>Пароль</label>
        <input
          v-model="form.password"
          type="password"
          class="input"
          placeholder="••••••••"
          @keyup.enter="submit"
        />
      </div>

      <p v-if="auth.error" class="error-msg">{{ auth.error }}</p>

      <button
        class="btn btn-primary submit-btn"
        :disabled="auth.loading"
        @click="submit"
      >
        {{ auth.loading ? 'Входим...' : 'Войти' }}
      </button>

      <p class="auth-footer">
        Нет аккаунта?
        <RouterLink to="/register">Зарегистрироваться</RouterLink>
      </p>
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
<!-- frontend/src/views/RegisterView.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
})
const localError = ref('')

const success = ref(false)

async function submit() {
  localError.value = ''
  if (form.value.password !== form.value.password2) {
    localError.value = 'Пароли не совпадают'
    return
  }
  const ok = await auth.register({
    username: form.value.username,
    email: form.value.email,
    password: form.value.password,
    password_confirm: form.value.password2,
  })
  if (ok) success.value = true
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card">
      <div v-if="success" style="text-align:center; padding: 1rem 0">
        <div style="font-size:3rem">📧</div>
        <h2 class="auth-title" style="margin-top:1rem">Проверь почту</h2>
        <p class="auth-sub">
          Мы отправили письмо на <strong>{{ form.email }}</strong><br>
          Перейди по ссылке в письме чтобы активировать аккаунт
        </p>
        <RouterLink to="/login" class="btn btn-primary submit-btn" style="display:block; margin-top:1.5rem">
          Перейти ко входу
        </RouterLink>
      </div>

      <template v-else>
        <h2 class="auth-title">Регистрация</h2>
        <p class="auth-sub">Создай аккаунт и начни шопинг 🛍</p>

        <div class="form-group">
          <label>Имя пользователя</label>
          <input v-model="form.username" class="input" placeholder="username" />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" class="input" placeholder="you@example.com" />
        </div>

        <div class="form-group">
          <label>Пароль</label>
          <input v-model="form.password" type="password" class="input" placeholder="••••••••" />
        </div>

        <div class="form-group">
          <label>Подтверди пароль</label>
          <input
            v-model="form.password2"
            type="password"
            class="input"
            placeholder="••••••••"
            @keyup.enter="submit"
          />
        </div>

        <p v-if="localError" class="error-msg">{{ localError }}</p>
        <p v-if="auth.error" class="error-msg">
          {{ typeof auth.error === 'string' ? auth.error : JSON.stringify(auth.error) }}
        </p>

        <button
          class="btn btn-primary submit-btn"
          :disabled="auth.loading"
          @click="submit"
        >
          {{ auth.loading ? 'Создаём аккаунт...' : 'Зарегистрироваться' }}
        </button>

        <p class="auth-footer">
          Уже есть аккаунт?
          <RouterLink to="/login">Войти</RouterLink>
        </p>
      </template>

</div>

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
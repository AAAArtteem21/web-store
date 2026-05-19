<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const email = ref('')
const sent = ref(false)
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    await api.post('/api/v1/users/password-reset/', { email: email.value })
  } finally {
    sent.value = true  // показываем успех даже если email не найден
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
        <RouterLink to="/login" class="btn btn-primary submit-btn" style="display:block; margin-top:1.5rem">
          Вернуться ко входу
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
          <RouterLink to="/login">← Вернуться ко входу</RouterLink>
        </p>
      </template>
    </div>
  </div>
</template>
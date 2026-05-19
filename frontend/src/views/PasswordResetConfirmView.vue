<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()

const form = ref({ new_password: '', confirm: '' })
const error = ref('')
const loading = ref(false)
const success = ref(false)

async function submit() {
  error.value = ''
  if (form.value.new_password !== form.value.confirm) {
    error.value = 'Пароли не совпадают'
    return
  }
  loading.value = true
  try {
    await api.post(
      `/api/v1/users/password-reset/${route.params.uid}/${route.params.token}/`,
      { new_password: form.value.new_password }
    )
    success.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch {
    error.value = 'Ссылка недействительна или истекла'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card">
      <div v-if="success" style="text-align:center">
        <div style="font-size:3rem">✅</div>
        <h2 class="auth-title" style="margin-top:1rem">Готово!</h2>
        <p class="auth-sub">Пароль изменён. Перенаправляем...</p>
      </div>

      <template v-else>
        <h2 class="auth-title">Новый пароль</h2>
        <p class="auth-sub">Придумай новый пароль для аккаунта</p>

        <div class="form-group">
          <label>Новый пароль</label>
          <input v-model="form.new_password" type="password" class="input" />
        </div>
        <div class="form-group">
          <label>Подтверди пароль</label>
          <input v-model="form.confirm" type="password" class="input" @keyup.enter="submit" />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>

        <button class="btn btn-primary submit-btn" :disabled="loading" @click="submit">
          {{ loading ? 'Сохраняем...' : 'Сохранить пароль' }}
        </button>
      </template>
    </div>
  </div>
</template>
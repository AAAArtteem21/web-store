<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const status = ref('loading') // loading | success | error

onMounted(async () => {
  try {
    await api.get(`/api/v1/users/verify-email/${route.params.uid}/${route.params.token}/`)
    status.value = 'success'
    setTimeout(() => router.push('/login'), 3000)
  } catch {
    status.value = 'error'
  }
})
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card" style="text-align:center">
      <div v-if="status === 'loading'">
        <div class="spinner" />
        <p class="auth-sub" style="margin-top:1rem">Проверяем ссылку...</p>
      </div>

      <div v-else-if="status === 'success'">
        <div style="font-size:3rem">✅</div>
        <h2 class="auth-title" style="margin-top:1rem">Email подтверждён!</h2>
        <p class="auth-sub">Перенаправляем на страницу входа...</p>
      </div>

      <div v-else>
        <div style="font-size:3rem">❌</div>
        <h2 class="auth-title" style="margin-top:1rem">Ссылка недействительна</h2>
        <p class="auth-sub">Возможно, она уже была использована или истекла</p>
        <RouterLink to="/register" class="btn btn-primary submit-btn" style="display:block; margin-top:1.5rem">
          Зарегистрироваться снова
        </RouterLink>
      </div>
    </div>
  </div>
</template>
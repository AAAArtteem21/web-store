// frontend/src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

    
  const isAuthenticated = computed(() => !!user.value)

  async function login(username, password) {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/v1/auth/login/', { username, password })
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      user.value = data.user
      await fetchProfile()
      return true
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка входа'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    try {
      await api.post('/api/v1/auth/register/', userData)
      return true  // просто возвращаем true, без токенов
    } catch (e) {
      error.value = e.response?.data || 'Ошибка регистрации'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchProfile() {
    try {
      const { data } = await api.get('/api/v1/auth/profile/')
      user.value = data
    } catch {
      user.value = null
    }
  }
  
  const token = localStorage.getItem('access_token')
  if (token) {
    fetchProfile()
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
  }

  return { user, loading, error, isAuthenticated, login, register, fetchProfile, logout }
})
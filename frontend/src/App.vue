<!-- frontend/src/App.vue -->
<script setup>
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { onMounted } from 'vue'

const auth = useAuthStore()
const cart = useCartStore()
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (token) {
    await auth.fetchProfile()
    await cart.fetchCart()
  }
})

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="app">
    <nav class="navbar">
      <RouterLink to="/" class="nav-logo">🛍 SHOP</RouterLink>

      <div class="nav-links">
        <RouterLink to="/">Каталог</RouterLink>
      </div>

      <div class="nav-actions">
        <RouterLink to="/cart" class="cart-btn">
          🛒
          <span v-if="cart.totalItems > 0" class="cart-badge">{{ cart.totalItems }}</span>
        </RouterLink>

        <template v-if="auth.isAuthenticated">
          <RouterLink to="/profile" class="nav-user">{{ auth.user?.username || 'Профиль' }}</RouterLink>
          <button class="btn-logout" @click="logout">Выйти</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn-login">Войти</RouterLink>
          <RouterLink to="/register" class="btn-register">Регистрация</RouterLink>
        </template>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #6c63ff;
  --primary-dark: #574fd6;
  --accent: #ff6584;
  --bg: #0f0f1a;
  --bg-card: #1a1a2e;
  --bg-card2: #16213e;
  --text: #f0f0f0;
  --text-muted: #9090aa;
  --border: #2a2a4a;
  --success: #4caf50;
  --error: #f44336;
  --radius: 12px;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, sans-serif;
  min-height: 100vh;
}

a {
  text-decoration: none;
  color: inherit;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Navbar ── */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 64px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.nav-logo {
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.nav-links a {
  color: var(--text-muted);
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--primary);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cart-btn {
  position: relative;
  font-size: 1.3rem;
  cursor: pointer;
}

.cart-badge {
  position: absolute;
  top: -6px;
  right: -8px;
  background: var(--accent);
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-user {
  color: var(--text-muted);
  font-size: 0.9rem;
  transition: color 0.2s;
}

.nav-user:hover {
  color: var(--primary);
}

.btn-login,
.btn-register {
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-login {
  color: var(--primary);
  border: 1px solid var(--primary);
}

.btn-login:hover {
  background: var(--primary);
  color: white;
}

.btn-register {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  color: white;
}

.btn-logout {
  background: none;
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.btn-logout:hover {
  border-color: var(--error);
  color: var(--error);
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
}

/* ── Общие компоненты ── */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(108, 99, 255, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: var(--bg-card2);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: all 0.2s;
}

.card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(108, 99, 255, 0.15);
}

.input {
  width: 100%;
  background: var(--bg-card2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.input:focus {
  border-color: var(--primary);
}

.input::placeholder {
  color: var(--text-muted);
}

.error-msg {
  color: var(--error);
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, var(--text), var(--text-muted));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 4rem auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
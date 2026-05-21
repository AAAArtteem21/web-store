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
  router.push('/')
}
</script>

<template>
  <div class="app">
    <nav class="navbar">
      <RouterLink to="/" class="nav-logo">
        <span class="logo-dot">●</span> DRIP
      </RouterLink>

      <div class="nav-center">
        <RouterLink to="/" class="nav-link">Каталог</RouterLink>
        <RouterLink v-if="auth.isAuthenticated" to="/favorites" class="nav-link nav-link--fav">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.5">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          Избранное
        </RouterLink>
      </div>

      <div class="nav-actions">
        <RouterLink to="/cart" class="cart-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 01-8 0"/>
          </svg>
          <span v-if="cart.totalItems > 0" class="cart-badge">{{ cart.totalItems }}</span>
        </RouterLink>

        <template v-if="auth.isAuthenticated">
          <RouterLink to="/profile" class="user-chip">
            {{ auth.user?.username?.[0]?.toUpperCase() || '?' }}
          </RouterLink>
          <button class="btn-logout" @click="logout">Выйти</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn-ghost">Войти</RouterLink>
          <RouterLink to="/register" class="btn-filled">Регистрация</RouterLink>
        </template>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>

    <footer class="footer">
      <div class="footer-inner">
        <span class="footer-logo">DRIP</span>
        <span class="footer-copy">© 2026 — Premium Streetwear</span>
      </div>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --primary: #111110;
  --accent: #d4f344;
  --accent-hover: #bcd832;
  --bg: #f7f6f3;
  --bg-card: #ffffff;
  --bg-card2: #f0efe9;
  --text: #111110;
  --text-muted: #72716b;
  --border: #e5e3dc;
  --border-strong: #c8c5bc;
  --success: #2d7d46;
  --error: #c53030;
  --fav: #e53e3e;
  --radius: 6px;
  --radius-lg: 12px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04);
  --shadow-lg: 0 4px 24px rgba(0,0,0,0.12);
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', system-ui, sans-serif;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

a { text-decoration: none; color: inherit; }

.app { min-height: 100vh; display: flex; flex-direction: column; }

/* Navbar */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  height: 64px;
  background: var(--primary);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-logo {
  font-family: 'Syne', sans-serif;
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: 4px;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.logo-dot { color: var(--accent); font-size: 0.55rem; }

.nav-center { display: flex; gap: 2rem; align-items: center; }

.nav-link {
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.45);
  transition: color 0.2s;
}

.nav-link:hover, .nav-link.router-link-active { color: var(--accent); }

/* Избранное в навбаре — подсветка красным при активном */
.nav-link--fav {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.nav-link--fav.router-link-active {
  color: #ff6b6b;
}

.nav-link--fav:hover {
  color: #ff6b6b;
}

.nav-actions { display: flex; align-items: center; gap: 1rem; }

.cart-btn {
  position: relative;
  color: rgba(255,255,255,0.65);
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.cart-btn:hover { color: var(--accent); }

.cart-badge {
  position: absolute;
  top: -7px; right: -9px;
  background: var(--accent);
  color: var(--primary);
  font-size: 0.55rem;
  font-weight: 800;
  border-radius: 50%;
  width: 16px; height: 16px;
  display: flex; align-items: center; justify-content: center;
}

.user-chip {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: var(--accent);
  color: var(--primary);
  font-size: 0.8rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: opacity 0.2s;
}

.user-chip:hover { opacity: 0.85; }

.btn-ghost {
  font-size: 0.78rem; font-weight: 500;
  color: rgba(255,255,255,0.55);
  padding: 0.4rem 0.9rem;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: var(--radius);
  transition: all 0.2s;
}

.btn-ghost:hover { color: white; border-color: rgba(255,255,255,0.4); }

.btn-filled {
  font-size: 0.78rem; font-weight: 700;
  color: var(--primary);
  background: var(--accent);
  padding: 0.4rem 1rem;
  border-radius: var(--radius);
  transition: background 0.2s;
}

.btn-filled:hover { background: var(--accent-hover); }

.btn-logout {
  background: none;
  border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.35);
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 0.75rem;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s;
}

.btn-logout:hover { border-color: var(--error); color: var(--error); }

/* Main */
.main-content {
  flex: 1;
  padding: 2.5rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* Footer */
.footer { background: var(--primary); padding: 1.25rem 2.5rem; }

.footer-inner {
  max-width: 1400px; margin: 0 auto;
  display: flex; justify-content: space-between; align-items: center;
}

.footer-logo {
  font-family: 'Syne', sans-serif;
  font-size: 0.95rem; font-weight: 800;
  color: var(--accent); letter-spacing: 3px;
}

.footer-copy { font-size: 0.75rem; color: rgba(255,255,255,0.2); }

/* Global Buttons */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: 0.5rem; padding: 0.75rem 1.75rem;
  border-radius: var(--radius); font-weight: 600; font-size: 0.9rem;
  cursor: pointer; border: none; transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: #222; transform: translateY(-1px); box-shadow: var(--shadow-lg); }
.btn-primary:disabled { opacity: 0.45; cursor: not-allowed; transform: none; box-shadow: none; }

.btn-secondary { background: transparent; color: var(--text); border: 1.5px solid var(--border-strong); }
.btn-secondary:hover { border-color: var(--primary); background: var(--primary); color: white; }

/* Card */
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; }

/* Input */
.input {
  width: 100%; background: white;
  border: 1.5px solid var(--border); color: var(--text);
  padding: 0.8rem 1rem; border-radius: var(--radius);
  font-size: 0.9rem; outline: none; transition: border-color 0.2s;
  font-family: 'Inter', sans-serif;
}

.input:focus { border-color: var(--primary); }
.input::placeholder { color: var(--text-muted); }

.error-msg { color: var(--error); font-size: 0.82rem; margin-top: 0.4rem; }

.page-title {
  font-family: 'Syne', sans-serif;
  font-size: 2.5rem; font-weight: 800;
  margin-bottom: 2rem; letter-spacing: -0.5px; color: var(--primary);
}

.spinner {
  width: 28px; height: 28px;
  border: 2px solid var(--border); border-top-color: var(--primary);
  border-radius: 50%; animation: spin 0.7s linear infinite; margin: 4rem auto;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
<!-- frontend/src/views/ProductView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()

const product = ref(null)
const loading = ref(true)
const selectedSize = ref(null)
const quantity = ref(1)
const adding = ref(false)
const addedMsg = ref('')

async function fetchProduct() {
  loading.value = true
  try {
    const { data } = await api.get(`/api/v1/product/${route.params.slug}/`)
    product.value = data
    if (data.sizes?.length > 0) {
      selectedSize.value = data.sizes[0].size.id  // ← исправлено
    }
  } catch {
    product.value = null
  } finally {
    loading.value = false
  }
}

async function addToCart() {
  if (!auth.isAuthenticated) {
    router.push('/login')
    return
  }
  if (!selectedSize.value) return

  adding.value = true
  try {
    await cart.addItem(product.value.id, selectedSize.value, quantity.value)
    addedMsg.value = '✓ Добавлено в корзину!'
    setTimeout(() => (addedMsg.value = ''), 2500)
  } catch {
    addedMsg.value = 'Ошибка при добавлении'
  } finally {
    adding.value = false
  }
}

onMounted(fetchProduct)
</script>

<template>
  <div>
    <div v-if="loading" class="spinner" />

    <div v-else-if="!product" class="empty">
      <p>😕 Товар не найден</p>
      <button class="btn btn-secondary" style="margin-top:1rem" @click="router.push('/')">
        В каталог
      </button>
    </div>

    <div v-else class="product-page">
      <!-- Назад -->
      <button class="back-btn" @click="router.back()">← Назад</button>

      <div class="product-layout">
        <!-- Изображение -->
        <div class="product-gallery">
          <div class="main-img">
            <img v-if="product.main_image" :src="product.main_image" :alt="product.name" />
            <div v-else class="img-placeholder">🛍</div>
          </div>
        </div>

        <!-- Информация -->
        <div class="product-details">
          <p class="product-category">{{ product.category?.name }}</p>
          <h1 class="product-title">{{ product.name }}</h1>
          <p class="product-price">${{ product.price }}</p>

          <p class="product-desc">{{ product.description }}</p>

          <!-- Размеры -->
          <div v-if="product.sizes?.length" class="sizes-section">
            <p class="section-label">Размер</p>
            <div class="sizes-grid">
              <button
                v-for="s in product.sizes"
                :key="s.size.id"
                class="size-btn"
                :class="{ active: selectedSize === s.size.id, disabled: s.stock === 0 }"
                :disabled="s.stock === 0"
                @click="selectedSize = s.size.id"
              >
                {{ s.size.name }}
              </button>
            </div>
          </div>

          <!-- Количество -->
          <div class="qty-section">
            <p class="section-label">Количество</p>
            <div class="qty-controls">
              <button class="qty-btn" @click="quantity = Math.max(1, quantity - 1)">−</button>
              <span class="qty-value">{{ quantity }}</span>
              <button class="qty-btn" @click="quantity++">+</button>
            </div>
          </div>

          <!-- Кнопка -->
          <button
            class="btn btn-primary add-btn"
            :disabled="adding || !selectedSize"
            @click="addToCart"
          >
            {{ adding ? 'Добавляем...' : '🛒 В корзину' }}
          </button>

          <p v-if="addedMsg" class="added-msg">{{ addedMsg }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.back-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: var(--primary);
}

.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

@media (max-width: 768px) {
  .product-layout {
    grid-template-columns: 1fr;
  }
}

.main-img {
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg-card);
  aspect-ratio: 1;
}

.main-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.img-placeholder {
  height: 100%;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5rem;
  color: var(--text-muted);
}

.product-category {
  font-size: 0.8rem;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}

.product-title {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.product-price {
  font-size: 2.2rem;
  font-weight: 900;
  color: var(--primary);
  margin-bottom: 1.5rem;
}

.product-desc {
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.section-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.75rem;
}

.sizes-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.size-btn {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.size-btn:hover,
.size-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.size-btn.disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.qty-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.qty-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text);
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
}

.qty-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.qty-value {
  font-size: 1.2rem;
  font-weight: 700;
  min-width: 30px;
  text-align: center;
}

.add-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
}

.added-msg {
  margin-top: 0.75rem;
  color: var(--success);
  font-weight: 600;
  text-align: center;
}

.empty {
  text-align: center;
  padding: 4rem;
  color: var(--text-muted);
}
</style>
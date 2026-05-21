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
const selectedImage = ref(null)
const quantity = ref(1)
const adding = ref(false)
const addedMsg = ref('')
const liked = ref(false)
const likesCount = ref(0)
const favorited = ref(false)
const favLoading = ref(false)

async function toggleLike() {
  if (!auth.isAuthenticated) { router.push('/login'); return }
  try {
    const { data } = await api.post(`/api/v1/product/${route.params.slug}/like/`)
    liked.value = data.liked
    likesCount.value = data.likes_count
  } catch {}
}

async function toggleFavorite() {
  if (!auth.isAuthenticated) { router.push('/login'); return }
  favLoading.value = true
  try {
    const { data } = await api.post(`/api/v1/product/${route.params.slug}/favorite/`)
    favorited.value = data.favorite
  } catch {}
  finally { favLoading.value = false }
}

async function fetchProduct() {
  loading.value = true
  try {
    const { data } = await api.get(`/api/v1/product/${route.params.slug}/`)
    product.value = data
    liked.value = data.is_liked
    likesCount.value = data.likes_count
    favorited.value = data.is_favorite
    selectedImage.value = data.main_image
    if (data.sizes?.length > 0) selectedSize.value = data.sizes[0].size.id
  } catch {
    product.value = null
  } finally {
    loading.value = false
  }
}

async function addToCart() {
  if (!auth.isAuthenticated) { router.push('/login'); return }
  if (!selectedSize.value) return
  adding.value = true
  try {
    await cart.addItem(product.value.id, selectedSize.value, quantity.value)
    addedMsg.value = 'Добавлено в корзину!'
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
  <div class="product-page">
    <div v-if="loading" class="spinner" />

    <div v-else-if="!product" class="empty">
      <p class="empty-title">Товар не найден</p>
      <button class="btn btn-secondary" style="margin-top:1.5rem" @click="router.push('/')">
        В каталог
      </button>
    </div>

    <template v-else>
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <button class="back-btn" @click="router.push('/')">Каталог</button>
        <span class="breadcrumb-sep">/</span>
        <span class="breadcrumb-current">{{ product.name }}</span>
      </div>

      <div class="product-layout">

        <!-- Gallery -->
        <div class="product-gallery">
          <div class="main-img">
            <img v-if="selectedImage" :src="selectedImage" :alt="product.name" />
            <div v-else class="img-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
              </svg>
            </div>
          </div>

          <!-- Thumbnails -->
          <div v-if="product.images?.length || product.main_image" class="extra-imgs">
            <div
              v-if="product.main_image"
              class="extra-img"
              :class="{ active: selectedImage === product.main_image }"
              @click="selectedImage = product.main_image"
            >
              <img :src="product.main_image" :alt="product.name" />
            </div>
            <div
              v-for="img in product.images"
              :key="img.id"
              class="extra-img"
              :class="{ active: selectedImage === img.image }"
              @click="selectedImage = img.image"
            >
              <img :src="img.image" :alt="product.name" />
            </div>
          </div>
        </div>

        <!-- Details -->
        <div class="product-details">

          <div class="product-header">
            <span class="product-category">{{ product.category?.name }}</span>
            <div class="header-actions">
              <!-- Like -->
              <button class="like-btn" :class="{ liked }" @click="toggleLike">
                <svg width="15" height="15" viewBox="0 0 24 24" :fill="liked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
                </svg>
                {{ likesCount }}
              </button>

              <!-- Favorite -->
              <button
                class="fav-btn"
                :class="{ favorited, loading: favLoading }"
                :title="favorited ? 'Убрать из избранного' : 'В избранное'"
                @click="toggleFavorite"
              >
                <svg width="15" height="15" viewBox="0 0 24 24" :fill="favorited ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
                {{ favorited ? 'В избранном' : 'Избранное' }}
              </button>
            </div>
          </div>

          <h1 class="product-title">{{ product.name }}</h1>
          <p class="product-price">${{ product.price }}</p>

          <p v-if="product.description" class="product-desc">{{ product.description }}</p>

          <div class="divider" />

          <!-- Sizes -->
          <div v-if="product.sizes?.length" class="sizes-section">
            <div class="section-header">
              <p class="section-label">Размер</p>
              <span class="size-guide">Таблица размеров</span>
            </div>
            <div class="sizes-grid">
              <button
                v-for="s in product.sizes"
                :key="s.size.id"
                class="size-btn"
                :class="{ active: selectedSize === s.size.id, unavailable: s.stock === 0 }"
                :disabled="s.stock === 0"
                @click="selectedSize = s.size.id"
              >
                {{ s.size.name }}
              </button>
            </div>
          </div>

          <!-- Quantity -->
          <div class="qty-section">
            <p class="section-label">Количество</p>
            <div class="qty-controls">
              <button class="qty-btn" @click="quantity = Math.max(1, quantity - 1)">−</button>
              <span class="qty-value">{{ quantity }}</span>
              <button class="qty-btn" @click="quantity++">+</button>
            </div>
          </div>

          <!-- Actions -->
          <div class="actions">
            <button
              class="btn-cart"
              :class="{ success: addedMsg }"
              :disabled="adding || !selectedSize"
              @click="addToCart"
            >
              <template v-if="addedMsg">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                {{ addedMsg }}
              </template>
              <template v-else-if="adding">Добавляем...</template>
              <template v-else>В корзину</template>
            </button>
          </div>

          <!-- Meta -->
          <div class="product-meta">
            <div class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
              Бесплатная доставка от $300
            </div>
            <div class="meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
              </svg>
              Возврат в течение 14 дней
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.product-page { width: 100%; }

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  font-size: 0.82rem;
}

.back-btn {
  background: none; border: none;
  color: var(--text-muted); cursor: pointer;
  font-size: 0.82rem; font-family: 'Inter', sans-serif;
  padding: 0; transition: color 0.2s;
}

.back-btn:hover { color: var(--primary); }
.breadcrumb-sep { color: var(--border-strong); }

.breadcrumb-current {
  color: var(--primary); font-weight: 500;
  white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis; max-width: 300px;
}

.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

@media (max-width: 900px) {
  .product-layout { grid-template-columns: 1fr; gap: 2rem; }
}

.main-img {
  border-radius: 12px; overflow: hidden;
  background: var(--bg-card2); aspect-ratio: 1; width: 100%;
}

.main-img img { width: 100%; height: 100%; object-fit: cover; }

.img-placeholder {
  width: 100%; aspect-ratio: 1;
  display: flex; align-items: center; justify-content: center;
  color: var(--border-strong); background: var(--bg-card2); border-radius: 12px;
}

.extra-imgs {
  display: flex; gap: 0.75rem;
  margin-top: 0.75rem; flex-wrap: wrap;
}

.extra-img {
  width: 80px; height: 80px; border-radius: 8px;
  overflow: hidden; border: 1.5px solid var(--border);
  cursor: pointer; transition: border-color 0.2s;
}

.extra-img:hover { border-color: var(--primary); }
.extra-img.active { border-color: var(--primary); border-width: 2px; }
.extra-img img { width: 100%; height: 100%; object-fit: cover; }

.product-header {
  display: flex; align-items: center;
  justify-content: space-between; margin-bottom: 0.75rem;
  flex-wrap: wrap; gap: 0.5rem;
}

.header-actions { display: flex; align-items: center; gap: 0.5rem; }

.product-category {
  font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 2px;
  color: var(--text-muted);
}

/* Like button */
.like-btn {
  display: flex; align-items: center; gap: 0.4rem;
  background: none; border: 1.5px solid var(--border);
  color: var(--text-muted); padding: 0.4rem 0.9rem;
  border-radius: 100px; cursor: pointer;
  font-size: 0.82rem; font-weight: 600;
  font-family: 'Inter', sans-serif; transition: all 0.2s;
}

.like-btn:hover { border-color: #e53e3e; color: #e53e3e; }
.like-btn.liked { border-color: #e53e3e; color: #e53e3e; background: #fff5f5; }

/* Favorite button */
.fav-btn {
  display: flex; align-items: center; gap: 0.4rem;
  background: none; border: 1.5px solid var(--border);
  color: var(--text-muted); padding: 0.4rem 0.9rem;
  border-radius: 100px; cursor: pointer;
  font-size: 0.82rem; font-weight: 600;
  font-family: 'Inter', sans-serif; transition: all 0.2s;
}

.fav-btn:hover { border-color: #d4a017; color: #d4a017; }

.fav-btn.favorited {
  border-color: #d4a017;
  color: #d4a017;
  background: #fffbeb;
}

.fav-btn svg {
  transition: transform 0.2s;
}

.fav-btn:hover svg {
  transform: scale(1.2);
}

.fav-btn.favorited svg {
  color: #f6ad55;
}

.product-title {
  font-family: 'Syne', sans-serif;
  font-size: 2.2rem; font-weight: 800;
  line-height: 1.1; margin-bottom: 1rem;
  color: var(--primary); letter-spacing: -0.5px;
}

.product-price {
  font-family: 'Syne', sans-serif;
  font-size: 2rem; font-weight: 700;
  color: var(--primary); margin-bottom: 1.25rem;
}

.product-desc {
  font-size: 0.9rem; color: var(--text-muted);
  line-height: 1.7; margin-bottom: 1.5rem;
}

.divider { height: 1px; background: var(--border); margin: 1.5rem 0; }

.section-header {
  display: flex; align-items: center;
  justify-content: space-between; margin-bottom: 0.75rem;
}

.section-label {
  font-size: 0.78rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px;
  color: var(--text-muted);
}

.size-guide {
  font-size: 0.78rem; color: var(--text-muted);
  text-decoration: underline; cursor: pointer;
}

.sizes-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.75rem; }

.size-btn {
  min-width: 52px; height: 52px; padding: 0 0.75rem;
  border-radius: 8px; border: 1.5px solid var(--border);
  background: white; color: var(--text);
  font-size: 0.88rem; font-weight: 600;
  font-family: 'Inter', sans-serif; cursor: pointer; transition: all 0.18s;
}

.size-btn:hover { border-color: var(--primary); }
.size-btn.active { background: var(--primary); border-color: var(--primary); color: white; }
.size-btn.unavailable { opacity: 0.35; cursor: not-allowed; text-decoration: line-through; }

.qty-section { margin-bottom: 1.75rem; }

.qty-controls {
  display: flex; align-items: center;
  margin-top: 0.75rem; background: white;
  border: 1.5px solid var(--border); border-radius: 8px; width: fit-content;
}

.qty-btn {
  width: 44px; height: 44px; border: none;
  background: none; color: var(--text); font-size: 1.1rem;
  cursor: pointer; transition: background 0.15s; font-family: 'Inter', sans-serif;
}

.qty-btn:hover { background: var(--bg-card2); }
.qty-btn:first-child { border-radius: 6px 0 0 6px; }
.qty-btn:last-child { border-radius: 0 6px 6px 0; }

.qty-value {
  font-size: 0.95rem; font-weight: 600;
  min-width: 40px; text-align: center;
  border-left: 1px solid var(--border);
  border-right: 1px solid var(--border);
  height: 44px; line-height: 44px;
}

.btn-cart {
  width: 100%; padding: 1rem;
  background: var(--primary); color: white;
  border: none; border-radius: 8px;
  font-size: 0.95rem; font-weight: 600;
  font-family: 'Inter', sans-serif; cursor: pointer;
  transition: all 0.2s; display: flex;
  align-items: center; justify-content: center; gap: 0.5rem;
}

.btn-cart:hover:not(:disabled) { background: #222; transform: translateY(-1px); }
.btn-cart:disabled { opacity: 0.45; cursor: not-allowed; transform: none; }
.btn-cart.success { background: var(--success); }

.product-meta { margin-top: 1.75rem; display: flex; flex-direction: column; gap: 0.6rem; }

.meta-item {
  display: flex; align-items: center;
  gap: 0.5rem; font-size: 0.8rem; color: var(--text-muted);
}

.empty { text-align: center; padding: 6rem 2rem; }

.empty-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem; font-weight: 700; color: var(--primary);
}
</style>
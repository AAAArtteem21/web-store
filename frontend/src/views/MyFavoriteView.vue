<!-- frontend/src/views/MyFavoriteView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()
const products = ref([])
const loading = ref(true)

async function fetchFavorites() {
  loading.value = true
  try {
    const { data } = await api.get('/api/v1/product/favorites/')
    products.value = data
  } catch {
    products.value = []
  } finally {
    loading.value = false
  }
}

async function removeFavorite(slug) {
  try {
    await api.post(`/api/v1/product/${slug}/favorite/`)
    products.value = products.value.filter(p => p.slug !== slug)
  } catch {}
}

onMounted(fetchFavorites)
</script>

<template>
  <div class="fav-page">

    <div class="fav-header">
      <div class="fav-title-row">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="#d4a017" stroke="#d4a017" stroke-width="1.5">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
        <h1 class="page-title" style="margin-bottom:0">Избранное</h1>
        <span v-if="!loading" class="fav-count">{{ products.length }}</span>
      </div>
      <p class="fav-subtitle">Товары, которые вы отметили звёздочкой</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="spinner" />

    <!-- Empty -->
    <div v-else-if="products.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
      </div>
      <p class="empty-title">Пока ничего нет</p>
      <p class="empty-sub">Отмечайте товары звёздочкой, чтобы сохранять их здесь</p>
      <button class="btn btn-primary" @click="router.push('/')">Перейти в каталог</button>
    </div>

    <!-- Grid -->
    <div v-else class="fav-grid">
      <div
        v-for="product in products"
        :key="product.id"
        class="fav-card"
      >
        <!-- Image -->
        <div class="fav-card__img" @click="router.push(`/product/${product.slug}`)">
          <img v-if="product.main_image" :src="product.main_image" :alt="product.name" />
          <div v-else class="fav-card__img-placeholder">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <circle cx="8.5" cy="8.5" r="1.5"/>
              <polyline points="21 15 16 10 5 21"/>
            </svg>
          </div>

          <!-- Remove btn -->
          <button
            class="fav-card__remove"
            title="Убрать из избранного"
            @click.stop="removeFavorite(product.slug)"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.5">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
          </button>
        </div>

        <!-- Info -->
        <div class="fav-card__body" @click="router.push(`/product/${product.slug}`)">
          <span class="fav-card__cat">{{ product.category?.name }}</span>
          <p class="fav-card__name">{{ product.name }}</p>
          <p class="fav-card__price">${{ product.price }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.fav-page { width: 100%; }

.fav-header { margin-bottom: 2.5rem; }

.fav-title-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.4rem;
}

.fav-count {
  background: #fffbeb;
  border: 1.5px solid #f6e05e;
  color: #b7791f;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.15rem 0.6rem;
  border-radius: 100px;
}

.fav-subtitle {
  font-size: 0.88rem;
  color: var(--text-muted);
  margin-left: 2.6rem;
}

/* Empty */
.empty-state {
  text-align: center;
  padding: 6rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty-icon {
  width: 96px; height: 96px;
  border-radius: 50%;
  background: #fffbeb;
  border: 2px solid #f6e05e;
  display: flex; align-items: center; justify-content: center;
  color: #d4a017;
  margin-bottom: 0.5rem;
}

.empty-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem; font-weight: 800;
  color: var(--primary);
}

.empty-sub {
  font-size: 0.88rem;
  color: var(--text-muted);
  max-width: 280px;
  line-height: 1.6;
}

/* Grid */
.fav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.fav-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
  cursor: pointer;
}

.fav-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.fav-card__img {
  position: relative;
  aspect-ratio: 1;
  background: var(--bg-card2);
  overflow: hidden;
}

.fav-card__img img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.fav-card:hover .fav-card__img img {
  transform: scale(1.04);
}

.fav-card__img-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: var(--border-strong);
}

/* Remove button — звёздочка сверху справа */
.fav-card__remove {
  position: absolute;
  top: 10px; right: 10px;
  width: 32px; height: 32px;
  border-radius: 50%;
  background: white;
  border: 1.5px solid #f6e05e;
  color: #d4a017;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.fav-card__remove:hover {
  background: #fff5f5;
  border-color: #e53e3e;
  color: #e53e3e;
  transform: scale(1.1);
}

.fav-card__body {
  padding: 1rem 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.fav-card__cat {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-muted);
}

.fav-card__name {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary);
  line-height: 1.3;
}

.fav-card__price {
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary);
  margin-top: 0.15rem;
}
</style>
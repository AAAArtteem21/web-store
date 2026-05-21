<!-- frontend/src/views/CatalogView.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()
const products = ref([])
const categories = ref([])
const loading = ref(true)
const selectedCategory = ref(null)
const searchQuery = ref('')
const ordering = ref('-created_at')

async function fetchProducts(categorySlug = null) {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (categorySlug) params.append('category', categorySlug)
    params.append('ordering', ordering.value)
    const { data } = await api.get(`/api/v1/product/?${params}`)
    products.value = Array.isArray(data) ? data : data.results || []
  } catch {
    products.value = []
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const { data } = await api.get('/api/v1/product/category/')
    categories.value = Array.isArray(data) ? data : data.results || []
  } catch {
    categories.value = []
  }
}

function selectCategory(slug) {
  selectedCategory.value = slug
  fetchProducts(slug)
}

function setOrdering(value) {
  ordering.value = value
  fetchProducts(selectedCategory.value)
}

const filtered = computed(() => {
  if (!searchQuery.value) return products.value
  return products.value.filter((p) =>
    p.name.toLowerCase().includes(searchQuery.value.toLowerCase()),
  )
})

onMounted(() => {
  fetchCategories()
  fetchProducts()
})
</script>

<template>
  <div class="catalog">

    <!-- Hero -->
    <div class="hero">
      <div class="hero-text">
        <p class="hero-label">Новая коллекция 2026</p>
        <h1 class="hero-title">STREETWEAR<br>REDEFINED.</h1>
        <p class="hero-sub">Одежда для тех, кто выделяется</p>
      </div>
      <div class="hero-search">
        <div class="search-wrap">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          <input v-model="searchQuery" class="search-input" placeholder="Поиск товаров..." />
        </div>
      </div>
    </div>

    <!-- Filters row -->
    <div class="filters-row">
      <div class="categories">
        <button
          class="cat-btn"
          :class="{ active: selectedCategory === null }"
          @click="selectCategory(null)"
        >Все</button>
        <button
          v-for="cat in categories"
          :key="cat.slug"
          class="cat-btn"
          :class="{ active: selectedCategory === cat.slug }"
          @click="selectCategory(cat.slug)"
        >{{ cat.name }}</button>
      </div>

      <div class="sort-group">
        <button class="sort-btn" :class="{ active: ordering === '-created_at' }" @click="setOrdering('-created_at')">Новые</button>
        <button class="sort-btn" :class="{ active: ordering === 'price' }" @click="setOrdering('price')">Цена ↑</button>
        <button class="sort-btn" :class="{ active: ordering === '-price' }" @click="setOrdering('-price')">Цена ↓</button>
        <button class="sort-btn" :class="{ active: ordering === '-likes_count' }" @click="setOrdering('-likes_count')">Популярные</button>
      </div>
    </div>

    <!-- Count -->
    <div v-if="!loading" class="results-count">
      {{ filtered.length }} {{ filtered.length === 1 ? 'товар' : filtered.length < 5 ? 'товара' : 'товаров' }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="spinner" />

    <!-- Empty -->
    <div v-else-if="filtered.length === 0" class="empty">
      <div class="empty-icon">—</div>
      <p class="empty-title">Ничего не найдено</p>
      <p class="empty-sub">Попробуйте изменить фильтры или поисковый запрос</p>
    </div>

    <!-- Grid -->
    <div v-else class="products-grid">
      <div
        v-for="product in filtered"
        :key="product.id"
        class="product-card"
        @click="router.push(`/product/${product.slug}`)"
      >
        <div class="product-img">
          <img v-if="product.main_image" :src="product.main_image" :alt="product.name" />
          <div v-else class="img-placeholder">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
              <polyline points="21 15 16 10 5 21"/>
            </svg>
          </div>
          <div class="img-overlay">
            <button class="overlay-btn" @click.stop="router.push(`/product/${product.slug}`)">
              Смотреть →
            </button>
          </div>
          <div class="likes-pill">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
            </svg>
            {{ product.likes_count || 0 }}
          </div>
            <div v-if="product.is_favorite" class="fav-pill">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
          </div>
        </div>

        <div class="product-info">
          <span class="product-category">{{ product.category?.name }}</span>
          <h3 class="product-name">{{ product.name }}</h3>
          <div class="product-footer">
            <span class="product-price">${{ product.price }}</span>
            <span class="product-arrow">→</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.catalog {
  width: 100%;
}

/* Hero */
.hero {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 1.25rem 0 1.25rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
  gap: 2rem;
  flex-wrap: wrap;
}

.hero-label {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.fav-pill {
  position: absolute;
  top: 12px; left: 12px;
  background: rgba(255,255,255,0.92);
  color: #d4a017;
  padding: 0.25rem 0.5rem;
  border-radius: 100px;
  display: flex; align-items: center;
  backdrop-filter: blur(8px);
}

.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(1.8rem, 3vw, 3rem);
  font-weight: 800;
  line-height: 0.95;
  letter-spacing: -1px;
  color: var(--primary);
  margin-bottom: 1rem;
}

.hero-sub {
  font-size: 0.95rem;
  color: var(--text-muted);
  font-weight: 400;
}

.hero-search {
  flex-shrink: 0;
  width: 320px;
}

.search-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 1rem;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: white;
  border: 1.5px solid var(--border);
  color: var(--text);
  padding: 0.85rem 1rem 0.85rem 2.75rem;
  border-radius: 100px;
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.2s;
  font-family: 'Inter', sans-serif;
}

.search-input:focus { border-color: var(--primary); }
.search-input::placeholder { color: var(--text-muted); }

/* Filters */
.filters-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.cat-btn {
  padding: 0.45rem 1.1rem;
  border-radius: 100px;
  border: 1.5px solid var(--border);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s;
  letter-spacing: 0.2px;
}

.cat-btn:hover { border-color: var(--primary); color: var(--primary); }
.cat-btn.active { background: var(--primary); border-color: var(--primary); color: white; }

.sort-group {
  display: flex;
  gap: 0.4rem;
  background: white;
  border: 1.5px solid var(--border);
  border-radius: 100px;
  padding: 0.25rem;
}

.sort-btn {
  padding: 0.35rem 0.9rem;
  border-radius: 100px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  transition: all 0.18s;
}

.sort-btn:hover { color: var(--primary); }
.sort-btn.active { background: var(--primary); color: white; }

/* Results count */
.results-count {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  letter-spacing: 0.3px;
}

/* Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.product-card {
  cursor: pointer;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  transition: transform 0.25s, box-shadow 0.25s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.1);
}

.product-img {
  height: 300px;
  overflow: hidden;
  background: var(--bg-card2);
  position: relative;
}

.product-img img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.product-card:hover .product-img img { transform: scale(1.04); }

.img-placeholder {
  height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: var(--border-strong);
}

.img-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.35);
  display: flex; align-items: center; justify-content: center;
  opacity: 0;
  transition: opacity 0.25s;
}

.product-card:hover .img-overlay { opacity: 1; }

.overlay-btn {
  background: white;
  color: var(--primary);
  border: none;
  padding: 0.65rem 1.5rem;
  border-radius: 100px;
  font-size: 0.85rem;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: transform 0.2s;
}

.overlay-btn:hover { transform: scale(1.04); }

.likes-pill {
  position: absolute;
  top: 12px; right: 12px;
  background: rgba(255,255,255,0.92);
  color: var(--text);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.6rem;
  border-radius: 100px;
  display: flex; align-items: center; gap: 0.3rem;
  backdrop-filter: blur(8px);
}

.product-info {
  padding: 1.1rem 1.25rem 1.25rem;
}

.product-category {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-muted);
  display: block;
  margin-bottom: 0.35rem;
}

.product-name {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary);
  font-family: 'Syne', sans-serif;
}

.product-arrow {
  font-size: 1rem;
  color: var(--text-muted);
  transition: transform 0.2s, color 0.2s;
}

.product-card:hover .product-arrow {
  transform: translateX(4px);
  color: var(--primary);
}

/* Empty */
.empty {
  text-align: center;
  padding: 6rem 2rem;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 3rem;
  font-weight: 200;
  color: var(--border-strong);
  margin-bottom: 1rem;
  line-height: 1;
}

.empty-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.empty-sub {
  font-size: 0.9rem;
  color: var(--text-muted);
}
</style>
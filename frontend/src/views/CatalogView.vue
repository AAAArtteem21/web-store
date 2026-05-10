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
    <h1 class="page-title">Каталог</h1>

    <!-- Поиск -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        class="input"
        placeholder="🔍 Поиск товаров..."
      />
    </div>

    <!-- Категории -->
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

    <!-- Сортировка -->
    <div class="ordering">
      <span class="ordering-label">Сортировка:</span>
      <button class="sort-btn" :class="{ active: ordering === '-created_at' }" @click="setOrdering('-created_at')">Новые</button>
      <button class="sort-btn" :class="{ active: ordering === 'price' }" @click="setOrdering('price')">Цена ↑</button>
      <button class="sort-btn" :class="{ active: ordering === '-price' }" @click="setOrdering('-price')">Цена ↓</button>
      <button class="sort-btn" :class="{ active: ordering === '-likes_count' }" @click="setOrdering('-likes_count')">❤️ Популярные</button>
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="spinner" />

    <!-- Пусто -->
    <div v-else-if="filtered.length === 0" class="empty">
      <p>😕 Товаров не найдено</p>
    </div>

    <!-- Сетка товаров -->
    <div v-else class="products-grid">
      <div
        v-for="product in filtered"
        :key="product.id"
        class="product-card card"
        @click="router.push(`/product/${product.slug}`)"
      >
        <div class="product-img">
          <img
            v-if="product.main_image"
            :src="product.main_image"
            :alt="product.name"
          />
          <div v-else class="img-placeholder">🛍</div>
          <div class="product-likes">❤️ {{ product.likes_count || 0 }}</div>
        </div>
        <div class="product-info">
          <p class="product-category">{{ product.category?.name }}</p>
          <h3 class="product-name">{{ product.name }}</h3>
          <div class="product-footer">
            <span class="product-price">${{ product.price }}</span>
            <button class="btn btn-primary btn-sm" @click.stop="router.push(`/product/${product.slug}`)">
              Подробнее
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.catalog {
  max-width: 1200px;
  margin: 0 auto;
}

.search-bar {
  margin-bottom: 1.5rem;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.cat-btn {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.cat-btn:hover,
.cat-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.ordering {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.ordering-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 600;
}

.sort-btn {
  padding: 0.3rem 0.9rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.sort-btn:hover,
.sort-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.product-card {
  cursor: pointer;
}

.product-img {
  height: 220px;
  overflow: hidden;
  background: var(--bg-card2);
  position: relative;
}

.product-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .product-img img {
  transform: scale(1.05);
}

.product-likes {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0,0,0,0.6);
  color: white;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  backdrop-filter: blur(4px);
}

.img-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: var(--text-muted);
}

.product-info {
  padding: 1rem;
}

.product-category {
  font-size: 0.75rem;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.3rem;
}

.product-name {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
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
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--primary);
}

.btn-sm {
  padding: 0.4rem 0.9rem;
  font-size: 0.8rem;
}

.empty {
  text-align: center;
  padding: 4rem;
  color: var(--text-muted);
  font-size: 1.2rem;
}
</style>
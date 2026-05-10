// frontend/src/stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const loading = ref(false)

  const totalItems = computed(() => items.value.reduce((s, i) => s + i.quantity, 0))
  const totalPrice = computed(() =>
    items.value.reduce((s, i) => s + parseFloat(i.price) * i.quantity, 0).toFixed(2),
  )

  async function fetchCart() {
    loading.value = true
    try {
      const { data } = await api.get('/api/v1/cart/cart/')
      items.value = data.items || data
    } catch {
      items.value = []
    } finally {
      loading.value = false
    }
  }

  async function addItem(product_id, size_id, quantity = 1) {
    await api.post('/api/v1/cart/add/cart/', {
      product: product_id,
      product_size: size_id,
      quantity
    })
    await fetchCart()
  }

  async function removeItem(item_id) {
    await api.delete('/api/v1/cart/del/cart/', { data: { item_id } })
    await fetchCart()
  }

async function updateItem(item_id, quantity) {
  if (quantity < 1) {
    await removeItem(item_id)
    return
  }
  await api.patch('/api/v1/cart/update/', { item_id, quantity })
  await fetchCart()
}

function clear() {
  items.value = []
}

return { items, loading, totalItems, totalPrice, fetchCart, addItem, removeItem, updateItem, clear }
})
// stores/storeRouting.js
import { apiClient } from '@/main'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useRoutingStore = defineStore('routing', () => {
  const loading = ref(false)
  const routes = ref([])

  // Фильтры (реактивные)
  const filters = ref({
    maxDistance: 50,
    maxDuration: 480,
    difficulty: [] // массив: ['easy', 'medium', ...]
  })

  // Загрузка маршрутов
  const fetchRout = async () => {
    loading.value = true
    try {
      const [response] = await Promise.all([
        apiClient.get('/walking-routes'),
        new Promise(resolve => setTimeout(resolve, 1500))
      ])
      routes.value = response.data.items || response.data
    } catch (err) {
      console.error('Ошибка при загрузке маршрутов:', err)
    } finally {
      loading.value = false
    }
  }

  // Фильтрация
  const filteredRoutes = computed(() => {
    return routes.value.filter(route => {
      // Фильтр по расстоянию
      if (route.distance_km > filters.value.maxDistance) return false

      // Фильтр по длительности
      if (route.duration_minutes > filters.value.maxDuration) return false

      // Фильтр по сложности
      if (
        filters.value.difficulty.length > 0 &&
        !filters.value.difficulty.includes(route.difficulty)
      ) {
        return false
      }

      return true
    })
  })

  // Геттеры
  const getRout = computed(() => routes.value)
  const getFilteredRoutes = computed(() => filteredRoutes.value)
  const getloading = computed(() => loading.value)
  const getFilters = computed(() => filters.value)

  // Управление фильтрами
  const updateFilters = (newFilters) => {
    Object.assign(filters.value, newFilters)
  }

  const clearFilters = () => {
    filters.value = {
      maxDistance: 50,
      maxDuration: 480,
      difficulty: []
    }
  }

  const hasActiveFilters = computed(() => {
    return (
      filters.value.maxDistance < 50 ||
      filters.value.maxDuration < 480 ||
      filters.value.difficulty.length > 0
    )
  })

  return {
    routes,
    loading,
    filters,
    getRout,
    getFilteredRoutes,
    getloading,
    getFilters,
    hasActiveFilters,
    fetchRout,
    updateFilters,
    clearFilters
  }
})
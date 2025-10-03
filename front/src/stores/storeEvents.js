import { apiClient } from '@/main'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEventsStore = defineStore('events', () => {
  const loading = ref(false)
  const events = ref([])

  // Добавляем eventType в фильтры
  const filters = ref({
    startDate: '',
    endDate: '',
    minRating: 0,
    eventType: '' // ← новое поле
  })

  const filteredEvents = computed(() => {
    return events.value.filter(event => {
      // Фильтр по типу события
      if (filters.value.eventType && event.event_type !== filters.value.eventType) {
        return false
      }

      // Фильтр по дате начала
      if (filters.value.startDate && event.start_date < filters.value.startDate + 'T00:00:00') {
        return false
      }
      // Фильтр по дате окончания
      if (filters.value.endDate && event.start_date > filters.value.endDate + 'T23:59:59') {
        return false
      }
      // Фильтр по рейтингу
      if (filters.value.minRating > 0 && event.rating < filters.value.minRating) {
        return false
      }
      return true
    })
  })

  const fetchEvents = async () => {
    loading.value = true
    try {
      const [response] = await Promise.all([
        apiClient.get('/events'),
        new Promise(resolve => setTimeout(resolve, 1500))
      ])
      events.value = response.data.items
    } catch (err) {
      console.error('Ошибка при загрузке событий:', err)
    } finally {
      loading.value = false
    }
  }

  // Обновляем hasActiveFilters — учитываем eventType
  const hasActiveFilters = computed(() => {
    return (
      filters.value.startDate ||
      filters.value.endDate ||
      filters.value.minRating > 0 ||
      !!filters.value.eventType // ← добавлено
    )
  })

  const updateFilters = (newFilters) => {
    Object.assign(filters.value, newFilters)
  }

  const clearFilters = () => {
    filters.value = {
      startDate: '',
      endDate: '',
      minRating: 0,
      eventType: '' // ← сбрасываем
    }
  }

  const getEvent = computed(() => events.value)
  const getloading = computed(() => loading.value)

  const registerForEvent = (eventId) => {
    const event = events.value.find(e => e.id === eventId)
    if (event) event.registered = true
  }

  return {
    events,
    loading,
    getloading,
    fetchEvents,
    filters,
    filteredEvents,
    hasActiveFilters,
    updateFilters,
    clearFilters,
    registerForEvent,
    getEvent
  }
})
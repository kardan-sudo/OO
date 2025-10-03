// src/stores/favoritesStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFavoritesStore = defineStore('favorites', () => {
  // Состояние
  const favoriteEventIds = ref(
    JSON.parse(localStorage.getItem('favoriteEvents')) || []
  )

  // Геттер
  const allFavoriteIds = computed(() => favoriteEventIds.value)

  // Действия
  function toggleFavorite(eventId) {
    const index = favoriteEventIds.value.indexOf(eventId)
    if (index === -1) {
      favoriteEventIds.value.push(eventId)
    } else {
      favoriteEventIds.value.splice(index, 1)
    }
    localStorage.setItem('favoriteEvents', JSON.stringify(favoriteEventIds.value))
  }

  function isFavorite(eventId) {
    return favoriteEventIds.value.includes(eventId)
  }

  return {
    favoriteEventIds,
    allFavoriteIds,
    toggleFavorite,
    isFavorite
  }
})
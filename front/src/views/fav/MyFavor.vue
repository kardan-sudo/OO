<template>
  <div class="div">
    <div v-if="!isLoading && favoriteEventIds.length === 0" class="empty-state">
      <div class="empty-icon">⭐</div>
      <h2>Нет избранных мероприятий</h2>
      <p>Добавьте интересующие вас события в избранное, чтобы видеть их здесь.</p>
      <router-link to="/mer" class="explore-link">Посмотреть мероприятия</router-link>
    </div>

    <div v-else-if="!isLoading" class="events-grid">
      <EventCard  
        v-for="(event, i) in favoriteEventIds" 
        :key="event.id" 
        :event="event"
        :ind="i"
        @register="handleRegister"
      />
    </div>

   
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import EventCard from '../Event/EventCard.vue'

const favoriteEventIds = ref([])
const isLoading = ref(true)

function loadFavoritesFromLocalStorage() {
  try {
    const data = localStorage.getItem('favoriteEvents')
    favoriteEventIds.value = data ? JSON.parse(data) : []
  } catch (error) {
    console.error('Ошибка при загрузке избранных из localStorage:', error)
    favoriteEventIds.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadFavoritesFromLocalStorage()
})

// Если понадобится обработка регистрации
const handleRegister = () => {
  // можно обновить список, если нужно
}
</script>

<style scoped>
.div {
  margin-top: 100px;
  padding: 0 2rem;
}

/* Сетка мероприятий */
.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

/* Состояние "пусто" */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  opacity: 0.7;
}

.empty-state h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

.empty-state p {
  font-size: 1.1rem;
  max-width: 600px;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.explore-link {
  display: inline-block;
  padding: 0.6rem 1.5rem;
  background: var(--primary-gradient);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.explore-link:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Состояние загрузки (опционально) */
.loading-state {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: var(--text-muted);
}
</style>
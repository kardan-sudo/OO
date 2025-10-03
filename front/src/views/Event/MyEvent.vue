<template>
  <div>
    <div>
      
    </div>
    <div class="events-container">
      <h1>Мероприятия в Орле</h1>
      <div class="events-info" v-if="filteredEvents.length === 0">
        <p>Мероприятия не найдены по выбранным фильтрам</p>
      </div>
      <div  class="events-grid" v-else>
        <EventCard  
          v-for="(event,i) in filteredEvents" 
          :key="event.id" 
          :event="event"
          :ind="i"
          @register="handleRegister"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useEventsStore } from '@/stores/storeEvents'
import EventCard from './EventCard.vue'

const eventsStore = useEventsStore()

const filteredEvents = computed(() => eventsStore.filteredEvents)

const handleRegister = (eventId) => {
  eventsStore.registerForEvent(eventId)
}
</script>

<style scoped>
.events-container {
  margin: 0 auto;
  padding: 2rem;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.events-info {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-size: 1.1rem;
}

h1 {
  color: #1e293b;
  text-align: center;
  margin-bottom: 2rem;
}
</style>
  
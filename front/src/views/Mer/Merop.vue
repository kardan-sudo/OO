<script setup>
import MyFiltr from '../Filter/MyFiltr.vue';
import Carta from '../Karta/Carta.vue'
import MyEvent from '../Event/MyEvent.vue';
import { computed, onMounted } from 'vue';
import { useEventsStore } from '@/stores/storeEvents';
import { storeToRefs } from 'pinia';
import MyLoad from '@/Load/MyLoad.vue';
const ev = useEventsStore()
const {getloading}  = storeToRefs(useEventsStore())
const load = computed(()=>getloading.value)
onMounted(()=>{
ev.fetchEvents()
})
</script>

<template>
  <div>
     <div v-if="load" class="load">
      <MyLoad/>
     </div>
    <div v-else>
      <h1>Мероприятия Орла</h1>
      <div class="main-container">
        <div class="content-grid">
          <div data-aos = "fade-right" class="events-section">
            <Carta/>
          </div>
          <div data-aos = "fade-left" class="filters-section">
            <MyFiltr />
          </div>
        </div>
        <div data-aos = "fade-up">
          <MyEvent />
        </div>
      </div>
    </div>
    </div>
</template>

<style scoped>
h1 {
  color: var(--text-primary);
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2.5rem;
  font-weight: 700;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.load {
  position: fixed;
  top: 50%;
  left: 50%;
   transform: translate(-50%, -50%) scale(0.5); /* 1 - 0.3 = 0.7 → на 30% меньше */
  z-index: 1000000;
  margin: 0;
  transform-origin: center; /* чтобы масштабирование было от центра */
}
.main-container {
  width: 100%;
  padding: 1rem;
  background: var(--bg-secondary);
  min-height: 100vh;
}

.content-grid {
  display: grid;
  grid-template-columns: 70% 1fr;
  gap: 2rem;
  margin: 0 auto;
  align-items: start;
 
}

.events-section {
  min-width: 0;
  position: sticky;
  top: 5rem;
  height: fit-content;
  max-height: calc(100vh - 6rem);
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
  overflow: hidden;
}

.filters-section {
  min-width: 0;
  position: sticky;
  top: 5rem;
  height: fit-content;
  max-height: calc(100vh - 6rem);
  overflow-y: auto;
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
}

/* Стили для скроллбара в filters-section */
.filters-section::-webkit-scrollbar {
  width: 6px;
}

.filters-section::-webkit-scrollbar-track {
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
}

.filters-section::-webkit-scrollbar-thumb {
  background: var(--border-medium);
  border-radius: var(--radius-sm);
}

.filters-section::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}

/* Адаптивность для мобильных устройств */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    min-height: auto;
  }
  
  .events-section {
    position: static;
    max-height: none;
    order: 2;
  }
  
  .filters-section {
    position: static;
    max-height: none;
    order: 1;
  }
  
  h1 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 0.5rem;
    background: var(--bg-primary);
  }
  
  .content-grid {
    gap: 1rem;
  }
  
  .events-section,
  .filters-section {
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
  }
  
  h1 {
    font-size: 1.75rem;
    margin-bottom: 1rem;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 1.5rem;
  }
  
  .main-container {
    padding: 0.25rem;
  }
}

/* Плавные переходы для всех интерактивных элементов */
.events-section,
.filters-section {
  transition: all var(--transition-normal);
}

.events-section:hover,
.filters-section:hover {
  box-shadow: var(--shadow-lg);
}
</style>
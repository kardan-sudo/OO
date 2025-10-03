<script setup>
import MyLoad from '@/Load/MyLoad.vue';
import CardVict from './CardVict.vue';
import { useVictStore } from '@/stores/storeVict';
import { storeToRefs } from 'pinia';
import { ref, onMounted, computed } from 'vue';
const qz = useVictStore()
const { getVict } = useVictStore();
const {getloading} = storeToRefs(useVictStore())
const load = computed(()=>getloading.value)
onMounted(async () => {
  try {
    await qz.fetchEvents(); // предполагается, что fetchEvents возвращает Promise
  } finally {
   
  }
});

</script>

<template>
  <div>
    <div v-if="load" class="load">
     <MyLoad/>
    </div>
    <div v-else class="container">
      
      <!-- Показываем загрузку или карточки -->
      <div v-if="loading" class="loading">
        Загрузка...
      </div>
  
      <div 
        v-else
        class="cards-container"
      >
        <CardVict
          data-aos="flip-left"
          v-for="(value, index) in getVict"
          :key="value.id || index"
          :quiz="value"
          class="card-item"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  margin-top: 100px;
  padding: 0 20px;
}

.title {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;

  transform: translateY(30px);
  transition: all 0.8s ease;
}

.cards-container.loaded {
  opacity: 1;
  transform: translateY(0);
}

.card-item {
  flex: 0 1 calc(33.333% - 30px);
  min-width: 300px;
  max-width: 400px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  animation: cardEntrance 0.6s ease-out forwards;
}

/* Анимация появления карточек с задержкой */
.card-item:nth-child(1) { animation-delay: 0.1s; }
.card-item:nth-child(2) { animation-delay: 0.2s; }
.card-item:nth-child(3) { animation-delay: 0.3s; }
.card-item:nth-child(4) { animation-delay: 0.4s; }
.card-item:nth-child(5) { animation-delay: 0.5s; }
.card-item:nth-child(6) { animation-delay: 0.6s; }

/* Эффекты при наведении */
.card-item:hover {
  transform: translateY(-10px) scale(1.03);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}
/* Адаптивность */
@media (max-width: 1200px) {
  .card-item {
    flex: 0 1 calc(50% - 30px);
  }
}

@media (max-width: 768px) {
  .container {
    margin-top: 60px;
    padding: 0 15px;
  }
  
  .title {
    font-size: 2rem;
    margin-bottom: 30px;
  }
  
  .cards-container {
    gap: 20px;
  }
  
  .card-item {
    flex: 0 1 100%;
    min-width: auto;
    max-width: 400px;
  }
}

/* Дополнительные эффекты для плавности */
.card-item {
  border-radius: 12px;
  overflow: hidden;
  will-change: transform;
  backface-visibility: hidden;
}

/* Эффект при загрузке для всей сетки */
.cards-container {
  perspective: 1000px;
}

.card-item {
  transform-style: preserve-3d;
}
</style>
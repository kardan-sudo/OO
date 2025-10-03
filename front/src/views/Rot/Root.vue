<template>
  <div>
    <div v-if="load" class="load">
      <MyLoad />
    </div>
    <div v-else class="routes-grid">
      <!-- Левая колонка: список маршрутов -->
      <div class="routes-column">
        <div class="routes-scroll-container" data-aos="fade-right">
          <OneRouting
            v-for="route in routes"
            :key="route.id"
            :route="route"
            @click="selectRoute(route)"
            class="clickable-route"
          />
        </div>
      </div>

      <!-- Центральная колонка: фото выбранного маршрута -->
      <div class="center-column" data-aos="fade-down">
        <MyRoutingImg data-aos = "fade-down" v-if="selectedRoute.img" :photo-url="selectedRoute.img" :srcc="selectedRoute.sr" :key="selectedRoute.sr" />
        <div v-else class="placeholder">
          <h2>Выберите маршрут</h2>
          <p>Нажмите на любой маршрут слева, чтобы увидеть его фото</p>
        </div>
      </div>

      <!-- Правая колонка: фильтры -->
      <div class="filters-column" data-aos="fade-left">
        <FiltrRout />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import OneRouting from './R/OneRouting.vue'
import FiltrRout from './F/FiltrRout.vue'
import MyLoad from '@/Load/MyLoad.vue'
import { useRoutingStore } from '@/stores/storeRouting'
import { storeToRefs } from 'pinia'
import MyRoutingImg from './MyRoutingImg.vue'

const routingStore = useRoutingStore()
const { getloading } = storeToRefs(routingStore)
const routes = computed(() => routingStore.getRout)
const load = computed(() => getloading.value)

// 👇 состояние выбранного маршрута
const selectedRoute = ref({img:'',sr:''
})

const selectRoute = (route) => {
  selectedRoute.value.img = route.photo_url
  selectedRoute.value.sr = route.url
  console.log(route,'Маршрут')
}

onMounted(() => {
  routingStore.fetchRout()
})
</script>

<style scoped>
.clickable-route {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-route:hover {
  background-color: #f8fafc;
}

.center-column {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.placeholder {
  color: #64748b;
}

.placeholder h2 {
  margin-bottom: 0.5rem;
}
.routes-grid {
  margin-top: 100px;
  display: grid;
  grid-template-columns: 20% 55% 25%;
  gap: 1rem;
  padding: 20px;
  width: 100%;
  min-height: 400px;
  align-items: start;
}

/* Контейнер для скролла — только в левой колонке */
.routes-scroll-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: calc(100vh - 200px); /* оставляет место под шапку и отступы */
  overflow-y: auto;
  padding-right: 8px; /* компенсация полосы прокрутки (опционально) */
}

/* Стили для колонок (для ясности) */
.routes-column,
.center-column,
.filters-column {
  display: flex;
  flex-direction: column;
}

/* Скроллбар (опционально — для красоты в Chrome) */
.routes-scroll-container::-webkit-scrollbar {
  width: 6px;
}
.routes-scroll-container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}
.routes-scroll-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}
.routes-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Адаптивность */
@media (max-width: 768px) {
  .routes-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 16px;
    margin-top: 60px;
  }

  .routes-scroll-container {
    max-height: none; /* на мобильных — скролл всей страницы */
    overflow-y: visible;
  }
}
</style>
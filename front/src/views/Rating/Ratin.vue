<template>
  <div>

  <div  class="rating-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1 class="page-title">Рейтинг мероприятий</h1>
      <p class="page-subtitle">Лучшие события города по оценкам участников</p>
    </div>

    <!-- Подиум для топ-3 -->
    <TopThree :top-events="topEvents"/>

    <!-- Остальной рейтинг -->
   <OtherRating   v-for="rt in otherEvents" :event="rt" />
  </div>
   </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEventsStore } from '@/stores/storeEvents'
import TopThree from './TopThree.vue';
import OtherRating from './OtherRating.vue';
import { storeToRefs } from 'pinia';
import MyLoad from '@/Load/MyLoad.vue';
const ev = useEventsStore()
const {loading} = storeToRefs(useEventsStore());
const events = computed(() => ev.getEvent)

const topEvents = computed(() => {
  return [...events.value]
    .sort((a, b) => b.rating - a.rating)
    .slice(0, 3)
})

const otherEvents = computed(() => {
  return [...events.value]
    .sort((a, b) => b.rating - a.rating)
    .slice(3)
})
console.log(otherEvents.value)
const viewEventDetails = (eventId) => {
  console.log('Просмотр мероприятия:', eventId)
  // Навигация к деталям мероприятия
}
onMounted(()=>{
  ev.fetchEvents()
})
console.log(topEvents,'top')
</script>

<style scoped>
.rating-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* Заголовок страницы */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 3rem;
  font-weight: 800;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
  letter-spacing: -1px;
}

.page-subtitle {
  font-size: 1.2rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Секции */
.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 2rem;
  text-align: center;
}

/* Подиум */
.podium-section {
  margin-bottom: 4rem;
}

.podium {
  display: grid;
  grid-template-columns: 1fr 1.2fr 1fr;
  gap: 2rem;
  align-items: end;
  max-width: 900px;
  margin: 0 auto;
}

.podium-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all var(--transition-normal);
}

.podium-item:hover {
  transform: translateY(-10px);
}

/* Пьедестал */
.podium-pedestal {
  position: relative;
  width: 100%;
  margin-bottom: 2rem;
}

.pedestal-base {
  width: 100%;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  position: relative;
  overflow: hidden;
}

.podium-item.first-place .pedestal-base {
  height: 120px;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, #FFD700, #FFEC8B);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
}

.podium-item.second-place .pedestal-base {
  height: 90px;
  background: linear-gradient(135deg, #C0C0C0, #E8E8E8);
  box-shadow: 0 8px 25px rgba(192, 192, 192, 0.3);
}

.podium-item.third-place .pedestal-base {
  height: 70px;
  background: linear-gradient(135deg, #CD7F32, #E8B886);
  box-shadow: 0 6px 20px rgba(205, 127, 50, 0.3);
}

.rank-badge {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  box-shadow: var(--shadow-lg);
}

.podium-item.first-place .rank-badge {
  background: var(--primary-gradient);
}

.podium-item.second-place .rank-badge {
  background: var(--accent-gradient);
}

.podium-item.third-place .rank-badge {
  background: var(--secondary-gradient);
}

/* Контент на подиуме */
.podium-content {
  width: 100%;
}

.event-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  transition: all var(--transition-normal);
  border: 1px solid var(--border-light);
}

.event-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-2xl);
}

.event-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.event-card:hover .event-image img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 50%, rgba(0, 0, 0, 0.3));
}

.crown-icon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: var(--primary-gradient);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  box-shadow: var(--shadow-lg);
  animation: crownGlow 2s ease-in-out infinite alternate;
}

@keyframes crownGlow {
  from {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
  }
  to {
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
  }
}

.event-info {
  padding: 1.5rem;
}

.event-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.event-rating {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--success-gradient);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: 1rem;
}

.event-description {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.event-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

/* Список рейтинга */
.rating-list-section {
  margin-top: 3rem;
}

.rating-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rating-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  transition: all var(--transition-normal);
  position: relative;
}

.rating-item:hover {
  transform: translateX(10px);
  box-shadow: var(--shadow-lg);
  border-color: var(--border-medium);
}

.rating-item.featured {
  border-left: 4px solid transparent;
  border-image: var(--primary-gradient) 1;
}

.rank-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-muted);
  min-width: 50px;
  text-align: center;
}

.event-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.rating-item .event-image {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  overflow: hidden;
  flex-shrink: 0;
}

.rating-item .event-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.event-details {
  flex: 1;
}

.rating-item .event-title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.rating-item .event-description {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.event-meta {
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.event-meta > div {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.details-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  flex-shrink: 0;
}

.details-btn:hover {
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

/* Адаптивность */
@media (max-width: 768px) {
  .rating-page {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .podium {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .podium-item {
    order: 2;
  }

  .podium-item.first-place {
    order: 1;
  }

  .rating-item {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .event-content {
    flex-direction: column;
    text-align: center;
  }

  .event-meta {
    justify-content: center;
  }

  .rank-number {
    align-self: flex-start;
  }
}

/* Анимации */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.podium-item {
  animation: fadeInUp 0.6s ease-out;
}

.podium-item.first-place {
  animation-delay: 0.1s;
}

.podium-item.second-place {
  animation-delay: 0.2s;
}

.podium-item.third-place {
  animation-delay: 0.3s;
}

.rating-item {
  animation: fadeInUp 0.6s ease-out;
}

.rating-item:nth-child(1) { animation-delay: 0.4s; }
.rating-item:nth-child(2) { animation-delay: 0.5s; }
.rating-item:nth-child(3) { animation-delay: 0.6s; }
</style>
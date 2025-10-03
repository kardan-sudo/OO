<template>
  <div class="place-card-wrapper">
    <div class="place-card">
      <div data-aos="fade-right" class="card-image">
        <img :src="place.photo_url" :alt="place.name" loading="lazy" />
        <div class="card-overlay">
          <div class="place-badge">
            {{ place.type }}
          </div>
          <!-- Кнопка избранного УДАЛЕНА -->
        </div>
      </div>

      <div data-aos="fade-left" class="card-content">
        <h3 class="place-name">{{ place.name }}</h3>
        
        <!-- Новое: spot_type как бейдж -->
        <div v-if="place.spot_type" class="spot-type-badge">
          {{ translateSpotType(place.spot_type) }}
        </div>

        <!-- Новое: title как подзаголовок -->
        <p v-if="place.title" class="place-title">
          {{ place.title }}
        </p>

        <p class="place-location">
          <i class="pi pi-map-marker"></i>
          {{ place.address }}
        </p>

        <p class="place-description">{{ place.description }}</p>

        <!-- Новое: история -->
        <div v-if="place.history" class="place-history">
          <div class="history-header">
            <i class="pi pi-book"></i>
            <span>История</span>
          </div>
          <p class="history-text">{{ place.history }}</p>
        </div>

        <!-- Обновлённые статы: только рейтинг -->
        <div class="place-stats" v-if="place.rating != null">
          <div class="stat">
            <i class="pi pi-star-fill"></i>
            <span>{{ place.rating }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  place: {
    type: Object,
    required: true,
  },
})
function translateSpotType(spotType) {
  const translations = {
    PARK: "Парк",
    ESTATE: "Усадьба",
    CASTLE: "Крепость",
    MONUMENT: "Памятник",
    NATURAL: "Природа",
    HISTORICAL: "История",
    ARCHITECTURAL: "Архитектура",
    RELOGIOS: "Религия"
  };

  return translations[spotType] ?? spotType; // возвращает оригинальное значение, если нет перевода
}
</script>

<style scoped>
.place-card-wrapper {

  border-radius: var(--radius-lg);
  overflow: hidden;
  isolation: isolate;
  border: #f59e0b;
}

/* Градиентный бордер — без изменений */
.place-card-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 2.5px;
  background: var(--primary-gradient);
  border-radius: var(--radius-lg);
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box, 
    linear-gradient(#fff 0 0);
  mask-composite: exclude;
  -webkit-mask-composite: xor;
  pointer-events: none;
  z-index: 1;
}

.place-card-wrapper::after {
  content: '';
  position: absolute;
  inset: 2.5px;
  border-radius: calc(var(--radius-lg) - 2.5px);
  box-shadow: inset 0 0 0 1px rgba(102, 126, 234, 0.15);
  pointer-events: none;
  z-index: 1;
}

.place-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 2;
}

.place-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
}

.card-image {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-normal);
}

.place-card:hover .card-image img {
  transform: scale(1.04);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background: linear-gradient(
    to top,
    var(--bg-overlay) 0%,
    transparent 50%,
    transparent 100%
  );
  opacity: 0;
  transition: opacity var(--transition-normal);
  pointer-events: none;
}

.place-card:hover .card-overlay {
  opacity: 1;
}

.place-badge {
  background: var(--primary-gradient);
  color: var(--text-on-gradient);
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 600;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  pointer-events: none;
}

/* Новое: бейдж типа локации */
.spot-type-badge {
  display: inline-block;
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  border: 1px solid #bae6fd;
}

/* Новое: подзаголовок title */
.place-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
  line-height: 1.5;
  font-style: italic;
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.place-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.place-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.9375rem;
  margin: 0 0 1rem 0;
}

.place-location .pi {
  color: var(--text-muted);
  font-size: 1rem;
}

.place-description {
  color: var(--text-secondary);
  font-size: 0.9375rem;
  line-height: 1.6;
  margin: 0 0 1.25rem 0;
  flex-grow: 1;
}

/* Новое: блок истории */
.place-history {
  margin: 1.25rem 0;
  padding: 1rem;
  background: rgba(248, 250, 252, 0.6);
  border-radius: var(--radius-md);
  border-left: 3px solid #94a3b8;
}

.history-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: #475569;
  font-weight: 600;
  font-size: 0.95rem;
}

.history-header .pi {
  color: #64748b;
}

.history-text {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
}

/* Статы: только рейтинг */
.place-stats {
  display: flex;
  gap: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-light);
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-primary);
  font-weight: 600;
}

.stat .pi {
  color: #f59e0b;
  font-size: 1.125rem;
}

.stat span {
  font-size: 0.9375rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .place-card-wrapper::before {
    padding: 2px;
  }

  .place-card-wrapper::after {
    inset: 2px;
    border-radius: calc(var(--radius-lg) - 2px);
  }

  .card-content {
    padding: 1.25rem;
  }
}
</style>
<template>
  <div class="filters-container compact">
    <div class="filters-header">
      <h3 class="filters-title">Фильтры</h3>
      <button 
        class="clear-filters-btn" 
        @click="clearFilters"
        :disabled="!hasActiveFilters"
      >
        <span class="pi pi-times"></span>
      </button>
    </div>

    <div class="filters-content">
      <!-- Фильтр по типу события -->
      <div class="filter-group">
        <label class="filter-label">Тип события</label>
        <div class="event-type-filters">
          <label
            v-for="type in eventTypes"
            :key="type.value"
            class="event-type-radio"
            :class="{ active: localFilters.eventType === type.value }"
          >
            <input
              type="radio"
              name="eventType"
              :value="type.value"
              v-model="localFilters.eventType"
              @change="applyFilters"
            />
            <span class="radio-label">{{ type.label }}</span>
          </label>
        </div>
      </div>

      <!-- Фильтр по рейтингу -->
      <div class="filter-group">
        <label class="filter-label">Рейтинг</label>
        <div class="rating-filters">
          <button 
            v-for="rating in ratingOptions" 
            :key="rating.value"
            class="rating-btn"
            :class="{ 
              active: localFilters.minRating === rating.value,
              disabled: localFilters.minRating > rating.value
            }"
            @click="toggleRating(rating.value)"
            :title="rating.label"
          >
            <span class="rating-stars">
              <span 
                v-for="star in 5" 
                :key="star"
                class="star"
                :class="{
                  'filled': star <= rating.value
                }"
              >
                ★
              </span>
            </span>
            <span class="rating-value">{{ rating.value }}+</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Статус активных фильтров -->
    <div class="filters-status" v-if="hasActiveFilters">
      <div class="active-filters">
        <div class="filter-tags">
          <span 
            v-if="localFilters.eventType" 
            class="filter-tag"
          >
            {{ localFilters.eventType }}
            <span class="tag-remove" @click="clearEventTypeFilter">×</span>
          </span>
          <span 
            v-if="localFilters.minRating > 0" 
            class="filter-tag"
          >
            {{ localFilters.minRating }}+★
            <span class="tag-remove" @click="clearRatingFilter">×</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useEventsStore } from '@/stores/storeEvents'

const eventsStore = useEventsStore()

// Локальные фильтры
const localFilters = ref({ ...eventsStore.filters })

// Типы событий
const eventTypes = [
  { value: 'Концерты', label: 'Концерты' },
  { value: 'Выставки', label: 'Выставки' },
  { value: 'Праздники', label: 'Праздники' },
  { value: 'Спектакли', label: 'Спектакли' }
]

// Опции рейтинга
const ratingOptions = [
  { value: 1, label: '1+ звезда' },
  { value: 2, label: '2+ звезды' },
  { value: 3, label: '3+ звезды' },
  { value: 4, label: '4+ звезды' },
  { value: 5, label: '5 звезд' }
]

// Вычисляемые свойства
const hasActiveFilters = computed(() => {
  return eventsStore.hasActiveFilters
})

// Методы
const applyFilters = () => {
  eventsStore.updateFilters({ ...localFilters.value })
}

const clearFilters = () => {
  localFilters.value = {
    startDate: '',
    endDate: '',
    minRating: 0,
    eventType: ''
  }
  eventsStore.clearFilters()
}

const clearEventTypeFilter = () => {
  localFilters.value.eventType = ''
  applyFilters()
}

const clearRatingFilter = () => {
  localFilters.value.minRating = 0
  applyFilters()
}

const toggleRating = (rating) => {
  localFilters.value.minRating = localFilters.value.minRating === rating ? 0 : rating
  applyFilters()
}

// Синхронизация с хранилищем
watch(() => eventsStore.filters, (newFilters) => {
  localFilters.value = { ...newFilters }
}, { deep: true })
</script>

<style scoped>
.filters-container.compact {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(100, 116, 139, 0.1);
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.filters-title {
  margin: 0;
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid #dc2626;
  color: #dc2626;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.clear-filters-btn:hover:not(:disabled) {
  background: #dc2626;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(220, 38, 38, 0.3);
}

.clear-filters-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: #cbd5e1;
  color: #cbd5e1;
}

.filter-group {
  margin-bottom: 1.25rem;
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-label {
  display: block;
  margin-bottom: 0.5rem;
  color: #475569;
  font-weight: 500;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Стили для радиокнопок типов событий */
.event-type-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.event-type-radio {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.event-type-radio:hover {
  border-color: #3b82f6;
  background: #eff6ff;
}

.event-type-radio.active {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border-color: #3b82f6;
}

.event-type-radio input {
  display: none;
}

.event-type-radio.active .radio-label {
  color: white;
}

/* Рейтинг */
.rating-filters {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.25rem;
}

.rating-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.4rem 0.25rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.7rem;
}

.rating-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 1px 4px rgba(59, 130, 246, 0.2);
}

.rating-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border-color: #3b82f6;
  box-shadow: 0 1px 6px rgba(59, 130, 246, 0.3);
}

.rating-btn.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.rating-stars {
  display: flex;
  gap: 1px;
}

.star {
  color: #cbd5e1;
  font-size: 0.7rem;
  line-height: 1;
}

.star.filled {
  color: #fbbf24;
}

.rating-btn.active .star {
  color: white;
}

.rating-value {
  font-weight: 600;
  font-size: 0.65rem;
}

/* Активные фильтры */
.filters-status {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.active-filters {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-tags {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.filter-tag {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.3rem 0.6rem;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 500;
  white-space: nowrap;
}

.tag-remove {
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: bold;
  padding: 1px;
  border-radius: 50%;
  width: 14px;
  height: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
  line-height: 1;
}

.tag-remove:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Адаптивность */
@media (max-width: 768px) {
  .filters-container.compact {
    padding: 0.75rem;
  }

  .event-type-filters {
    flex-direction: column;
    align-items: flex-start;
  }

  .active-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .filter-tags {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .filters-header {
    flex-direction: row;
    gap: 0.5rem;
  }

  .clear-filters-btn {
    width: 28px;
    height: 28px;
    font-size: 0.7rem;
  }
}
</style>
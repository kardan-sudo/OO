<template>
    <div class="filters-container compact">
      <div class="filters-header">
        <h3 class="filters-title">Фильтры маршрутов</h3>
        <button 
          class="clear-filters-btn" 
          @click="clearFilters"
          :disabled="!hasActiveFilters"
        >
          <span class="pi pi-times"></span>
        </button>
      </div>
  
      <div class="filters-content">
        <!-- Фильтр по протяженности -->
        <div class="filter-group">
          <label class="filter-label">
            Протяженность: до {{ filters.maxDistance }} км
          </label>
          <div class="slider-container">
            <input 
              type="range" 
              v-model="filters.maxDistance"
              min="1"
              max="50"
              step="1"
              class="slider"
              @input="applyFilters"
            />
            <div class="slider-labels">
              <span>1 км</span>
              <span>25 км</span>
              <span>50 км</span>
            </div>
          </div>
        </div>
  
        <!-- Фильтр по длительности -->
        <div class="filter-group">
          <label class="filter-label">
            Длительность: до {{ formatDuration(filters.maxDuration) }}
          </label>
          <div class="slider-container">
            <input 
              type="range" 
              v-model="filters.maxDuration"
              min="30"
              max="480"
              step="30"
              class="slider"
              @input="applyFilters"
            />
            <div class="slider-labels">
              <span>30 мин</span>
              <span>4 ч</span>
              <span>8 ч</span>
            </div>
          </div>
        </div>
  
        <!-- Фильтр по сложности -->
        <div class="filter-group">
          <label class="filter-label">Сложность</label>
          <div class="difficulty-filters">
            <button 
              v-for="difficulty in difficultyOptions" 
              :key="difficulty.value"
              class="difficulty-btn"
              :class="{ 
                active: filters.difficulty.includes(difficulty.value),
                [difficulty.value]: true
              }"
              @click="toggleDifficulty(difficulty.value)"
            >
              <span class="difficulty-icon pi" :class="difficulty.icon"></span>
              <span class="difficulty-text">{{ difficulty.label }}</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Статус фильтров -->
      <div class="filters-status" v-if="hasActiveFilters">
        <div class="active-filters">
          <div class="filter-tags">
            <span 
              v-if="filters.maxDistance < 50" 
              class="filter-tag"
            >
              До {{ filters.maxDistance }} км
              <span class="tag-remove" @click="clearDistanceFilter">×</span>
            </span>
            <span 
              v-if="filters.maxDuration < 480" 
              class="filter-tag"
            >
              До {{ formatDuration(filters.maxDuration) }}
              <span class="tag-remove" @click="clearDurationFilter">×</span>
            </span>
            <span 
              v-for="diff in filters.difficulty" 
              :key="diff"
              class="filter-tag"
            >
              {{ getDifficultyLabel(diff) }}
              <span class="tag-remove" @click="removeDifficulty(diff)">×</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script setup>
import { ref, computed, watch } from 'vue'
import { useRoutingStore } from '@/stores/storeRouting'

const routingStore = useRoutingStore()

// Синхронизируем локальные фильтры с хранилищем
const filters = ref({ ...routingStore.filters })

// Опции сложности
const difficultyOptions = [
  { value: 'easy', label: 'Легкий', icon: 'pi-walking' },
  { value: 'medium', label: 'Средний', icon: 'pi-mountain' },
  { value: 'hard', label: 'Сложный', icon: 'pi-arrow-up-right' }
]

// Вычисляемые свойства
const hasActiveFilters = computed(() => routingStore.hasActiveFilters)

// Применяем фильтры в хранилище
const applyFilters = () => {
  routingStore.updateFilters({ ...filters.value })
}

// Очистка
const clearFilters = () => {
  routingStore.clearFilters()
  filters.value = { ...routingStore.filters }
}

// Вспомогательные функции
const formatDuration = (minutes) => {
  return minutes < 60 ? `${minutes} мин` : `${minutes / 60} ч`
}

const getDifficultyLabel = (value) => {
  return difficultyOptions.find(d => d.value === value)?.label || value
}

// Управление сложностью
const toggleDifficulty = (difficulty) => {
  const index = filters.value.difficulty.indexOf(difficulty)
  if (index > -1) {
    filters.value.difficulty.splice(index, 1)
  } else {
    filters.value.difficulty.push(difficulty)
  }
  applyFilters()
}

const removeDifficulty = (difficulty) => {
  const index = filters.value.difficulty.indexOf(difficulty)
  if (index > -1) {
    filters.value.difficulty.splice(index, 1)
    applyFilters()
  }
}

// Очистка отдельных фильтров
const clearDistanceFilter = () => {
  filters.value.maxDistance = 50
  applyFilters()
}

const clearDurationFilter = () => {
  filters.value.maxDuration = 480
  applyFilters()
}

// Синхронизация при изменении извне (например, при сбросе)
watch(
  () => routingStore.filters,
  (newFilters) => {
    filters.value = { ...newFilters }
  },
  { deep: true }
)
</script>
  
  <style scoped>
  .filters-container.compact {
    background: var(--bg-primary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-xl);
    padding: 1.5rem;
    box-shadow: var(--shadow-lg);
    backdrop-filter: blur(20px);
  }
  
  .filters-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-light);
  }
  
  .filters-title {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .clear-filters-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: transparent;
    border: 2px solid var(--border-medium);
    color: var(--text-secondary);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: 0.9rem;
    transition: all var(--transition-normal);
  }
  
  .clear-filters-btn:hover:not(:disabled) {
    background: var(--secondary-gradient);
    color: var(--text-on-gradient);
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .clear-filters-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .filter-group {
    margin-bottom: 2rem;
  }
  
  .filter-group:last-child {
    margin-bottom: 0;
  }
  
  .filter-label {
    display: block;
    margin-bottom: 1rem;
    color: var(--text-primary);
    font-weight: 600;
    font-size: 0.95rem;
  }
  
  /* Стили для ползунков */
  .slider-container {
    margin-bottom: 0.5rem;
  }
  
  .slider {
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: var(--bg-secondary);
    outline: none;
    -webkit-appearance: none;
    appearance: none;
  }
  
  .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--primary-gradient);
    cursor: pointer;
    border: 2px solid var(--bg-primary);
    box-shadow: var(--shadow-md);
    transition: all var(--transition-normal);
  }
  
  .slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    box-shadow: var(--shadow-lg);
  }
  
  .slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--primary-gradient);
    cursor: pointer;
    border: 2px solid var(--bg-primary);
    box-shadow: var(--shadow-md);
    transition: all var(--transition-normal);
  }
  
  .slider::-moz-range-thumb:hover {
    transform: scale(1.2);
    box-shadow: var(--shadow-lg);
  }
  
  .slider-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
    color: var(--text-muted);
    font-size: 0.8rem;
    font-weight: 500;
  }
  
  /* Стили для кнопок сложности */
  .difficulty-filters {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }
  
  .difficulty-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 0.5rem;
    background: var(--bg-secondary);
    border: 2px solid var(--border-light);
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: all var(--transition-normal);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
  }
  
  .difficulty-btn:hover {
    transform: translateY(-2px);
    border-color: var(--border-medium);
    box-shadow: var(--shadow-sm);
  }
  
  .difficulty-btn.active {
    color: var(--text-on-gradient);
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  .difficulty-btn.easy.active {
    background: var(--success-gradient);
  }
  
  .difficulty-btn.medium.active {
    background: var(--accent-gradient);
  }
  
  .difficulty-btn.hard.active {
    background: var(--secondary-gradient);
  }
  
  .difficulty-icon {
    font-size: 1.25rem;
    transition: all var(--transition-normal);
  }
  
  .difficulty-btn.active .difficulty-icon {
    transform: scale(1.1);
  }
  
  .difficulty-text {
    font-size: 0.8rem;
    font-weight: 600;
  }
  
  /* Статус фильтров */
  .filters-status {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-light);
  }
  
  .active-filters {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .filter-tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    flex: 1;
  }
  
  .filter-tag {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--primary-gradient);
    color: var(--text-on-gradient);
    padding: 0.5rem 0.875rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    white-space: nowrap;
    box-shadow: var(--shadow-sm);
  }
  
  .tag-remove {
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    padding: 2px;
    border-radius: 50%;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background var(--transition-fast);
    line-height: 1;
  }
  
  .tag-remove:hover {
    background: rgba(255, 255, 255, 0.2);
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .filters-container.compact {
      padding: 1.25rem;
    }
  
    .difficulty-filters {
      grid-template-columns: 1fr;
      gap: 0.5rem;
    }
  
    .difficulty-btn {
      flex-direction: row;
      justify-content: center;
      padding: 0.875rem 1rem;
    }
  
    .active-filters {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.75rem;
    }
  
    .filter-tags {
      width: 100%;
    }
  }
  
  @media (max-width: 480px) {
    .filters-header {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start;
    }
  
    .clear-filters-btn {
      align-self: stretch;
      justify-content: center;
    }
  }
  
  /* Темная тема */
  @media (prefers-color-scheme: dark) {
    .filters-container.compact {
      background: var(--bg-primary);
      border-color: var(--border-light);
    }
  
    .slider {
      background: var(--bg-secondary);
    }
  
    .difficulty-btn {
      background: var(--bg-secondary);
      border-color: var(--border-light);
    }
  
    .difficulty-btn:hover {
      border-color: var(--border-medium);
    }
  
    .filters-status {
      border-color: var(--border-light);
    }
  }
  </style>
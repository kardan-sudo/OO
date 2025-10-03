<template>
  <div class="admin-applications">
    <h3>📊 Управление заявками</h3>
    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner">⏳</div>
      <p>Загрузка заявок...</p>
    </div>

    <div v-else>

    <div class="applications-controls">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Поиск по названию или организатору..."
          class="search-input"
        >
        <span class="search-icon">🔍</span>
      </div>
      
      <div class="filter-buttons">
        <button 
          v-for="type in eventTypes" 
          :key="type"
          @click="toggleFilter(type)"
          :class="['filter-btn', { active: activeFilters.includes(type) }]"
        >
          {{ type }}
        </button>
      </div>
    </div>

    <div class="applications-list">
      <div 
        v-for="application in filteredApplications" 
        :key="application.id"
        class="application-card"
        :class="{ expanded: expandedCard === application.id }"
      >
        <!-- Краткая информация -->
        <div class="card-header" @click="toggleCard(application.id)">
          <div class="card-main-info">
            <h4 class="event-name">{{ application.eventName }}</h4>
            <div class="event-meta">
              <span class="event-type">{{ application.eventType }}</span>
              <span class="event-date">📅 {{ formatDate(application.startDate) }}</span>
              <span class="event-organizer">👤 {{ application.organizer }}</span>
            </div>
          </div>
          <div class="card-arrow">
            {{ expandedCard === application.id ? '▲' : '▼' }}
          </div>
        </div>

        <!-- Подробная информация -->
        <div v-if="expandedCard === application.id" class="card-details">
          <div class="details-grid">
            <div class="detail-item">
              <label>Тип мероприятия:</label>
              <span>{{ application.eventType }}</span>
            </div>
            <div class="detail-item">
              <label>Дата начала:</label>
              <span>{{ formatDate(application.startDate) }}</span>
            </div>
            <div class="detail-item">
              <label>Дата окончания:</label>
              <span>{{ formatDate(application.endDate) }}</span>
            </div>
            <div class="detail-item">
              <label>Адрес:</label>
              <span>{{ application.address }}</span>
            </div>
            <div v-if="application.coordinateX && application.coordinateY" class="detail-item">
              <label>Координаты:</label>
              <span>X: {{ application.coordinateX }}, Y: {{ application.coordinateY }}</span>
            </div>
            <div class="detail-item">
              <label>Организатор:</label>
              <span>{{ application.organizer }}</span>
            </div>
            <div class="detail-item full-width">
              <label>Описание:</label>
              <p>{{ application.description }}</p>
            </div>
            <div v-if="application.website" class="detail-item">
              <label>Веб-сайт:</label>
              <a :href="application.website" target="_blank" class="website-link">{{ application.website }}</a>
            </div>
            <div v-if="application.phone" class="detail-item">
              <label>Телефон:</label>
              <a :href="`tel:${application.phone}`" class="phone-link">{{ application.phone }}</a>
            </div>
          </div>
          
          <div class="card-actions">
            <button class="btn-approve" @click="approveApplication(application.id)">
              ✅ Одобрить
            </button>
            <button class="btn-reject" @click="rejectApplication(application.id)">
              ❌ Отклонить
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="filteredApplications.length === 0" class="no-applications">
        <div class="no-applications-icon">📭</div>
        <h4>Нет заявок для рассмотрения</h4>
        <p>Попробуйте изменить параметры поиска или фильтры</p>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>

import { ref, computed, onMounted } from 'vue'
import { useApplicationsStore } from '../stores/applications'

const applicationsStore = useApplicationsStore()
const applications = ref(applicationsStore.applications) // Инициализируем пустым массивом
const expandedCard = ref(null)
const searchQuery = ref('')
const activeFilters = ref([])
const isLoading = ref(true) // Добавляем состояние загрузки

const eventTypes = ['Концерты', 'Выставки', 'Праздники', 'Спектакли']

onMounted(() => {
  // Имитируем загрузку данных
  setTimeout(() => {
    
    isLoading.value = false
  }, 500)
})

const toggleCard = (id) => {
  expandedCard.value = expandedCard.value === id ? null : id
}

const toggleFilter = (type) => {
  const index = activeFilters.value.indexOf(type)
  if (index > -1) {
    activeFilters.value.splice(index, 1)
  } else {
    activeFilters.value.push(type)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не указана'
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const filteredApplications = computed(() => {
  if (isLoading.value || !applications.value) {
    return []
  }

  let filtered = applications.value

  // Поиск по названию и организатору
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(app => 
      app.eventName?.toLowerCase().includes(query) ||
      app.organizer?.toLowerCase().includes(query)
    )
  }

  // Фильтрация по типу
  if (activeFilters.value.length > 0) {
    filtered = filtered.filter(app => 
      activeFilters.value.includes(app.eventType)
    )
  }

  return filtered
})

const approveApplication = (id) => {
  const application = applications.value.find(app => app.id === id)
  if (application) {
    alert(`Заявка "${application.eventName}" одобрена!`)
    // Обновляем данные в хранилище и локально
    applicationsStore.applications = applicationsStore.applications.filter(app => app.id !== id)
    applications.value = applications.value.filter(app => app.id !== id)
  }
}

const rejectApplication = (id) => {
  const application = applications.value.find(app => app.id === id)
  if (application) {
    alert(`Заявка "${application.eventName}" отклонена!`)
    // Обновляем данные в хранилище и локально
    applicationsStore.applications = applicationsStore.applications.filter(app => app.id !== id)
    applications.value = applications.value.filter(app => app.id !== id)
  }
}
</script>


<style scoped>



.admin-applications {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.applications-controls {
  display: flex;
  gap: 20px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 12px 45px 12px 15px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}

.filter-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 20px;
  background: white;
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.filter-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.filter-btn.active:hover {
  background: #2563eb;
  border-color: #2563eb;
  color: white;
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.application-card {
  border: 2px solid #f1f5f9;
  border-radius: 12px;
  background: #fafafa;
  transition: all 0.3s ease;
  overflow: hidden;
}

.application-card:hover {
  border-color: #e2e8f0;
  background: white;
}

.application-card.expanded {
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.card-header:hover {
  background: #f8fafc;
}

.card-main-info {
  flex: 1;
}

.event-name {
  margin: 0 0 12px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
}

.event-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.event-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: #64748b;
}

.event-type {
  background: #e0f2fe;
  color: #0369a1;
  padding: 4px 12px;
  border-radius: 15px;
  font-weight: 600;
  font-size: 0.8rem;
}

.card-arrow {
  color: #64748b;
  font-size: 1.2rem;
  margin-left: 15px;
}

.card-details {
  padding: 0 20px 20px 20px;
  border-top: 1px solid #e2e8f0;
  margin-top: -10px;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin: 20px 0;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item label {
  font-weight: 600;
  color: #64748b;
  font-size: 0.85rem;
}

.detail-item span,
.detail-item p {
  color: #1e293b;
  margin: 0;
}

.website-link,
.phone-link {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.3s ease;
}

.website-link:hover,
.phone-link:hover {
  color: #2563eb;
  text-decoration: underline;
}

.card-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.btn-approve,
.btn-reject {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.btn-approve {
  background: #dcfce7;
  color: #166534;
}

.btn-reject {
  background: #fecaca;
  color: #991b1b;
}

.btn-approve:hover {
  background: #bbf7d0;
  transform: translateY(-1px);
}

.btn-reject:hover {
  background: #fca5a5;
  transform: translateY(-1px);
}

.no-applications {
  text-align: center;
  padding: 60px 40px;
  background: #f8fafc;
  border-radius: 12px;
  color: #64748b;
}

.no-applications-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.no-applications h4 {
  margin: 0 0 10px 0;
  color: #475569;
}

.no-applications p {
  margin: 0;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .admin-applications {
    padding: 20px;
  }
  
  .applications-controls {
    flex-direction: column;
    gap: 15px;
  }
  
  .search-box {
    min-width: 100%;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .card-header {
    padding: 15px;
  }
  
  .event-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .card-actions {
    flex-direction: column;
  }
  
  .btn-approve,
  .btn-reject {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .admin-applications {
    padding: 15px;
  }
  
  .card-header {
    padding: 12px;
  }
  
  .event-name {
    font-size: 1.1rem;
  }
  
  .btn-approve,
  .btn-reject {
    padding: 10px 20px;
  }
}
</style>
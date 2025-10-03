<template>
  <div class="container">
    <div class="header">
      <div>
        <h1>🎭 Система мониторинга культурных событий</h1>
        <p>Автоматический сбор информации с сайтов музеев, театров и афиш города Орёл</p>
      </div>
      <div class="stats">
        <div class="stat-item" v-for="stat in stats" :key="stat.label">
          <div class="stat-number">{{ stat.number }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <div class="tabs">
      <div
        v-for="tab in tabs"
        :key="tab.id"
        class="tab"
        :class="{ active: activeTab === tab.id }"
        @click="showSection(tab.id)"
      >
        {{ tab.label }}
      </div>
    </div>

    <div   class="content">
      <!-- Секция собранных событий -->
      <div v-show="activeTab === 'events'" class="section">
        <div class="section-title">
          <span>События, ожидающие проверки</span>
          <button class="btn btn-primary" @click="verifyAll">✅ Проверить все</button>
        </div>

        <div v-for="event in events" :key="event.id" class="event-card">
          <div class="event-header">
            <div>
              <div class="event-title">{{ event.title }}</div>
              <div class="event-source">{{ event.source }}</div>
            </div>
            <span :class="['badge', `badge-${event.type}`]">{{ event.typeLabel }}</span>
          </div>
          <div class="event-details">
            <div class="event-detail">
              <i>📅</i> {{ event.date }}
            </div>
            <div class="event-detail">
              <i>⏰</i> {{ event.time }}
            </div>
            <div class="event-detail">
              <i>📍</i> {{ event.location }}
            </div>
            <div class="event-detail">
              <i>💰</i> {{ event.price }}
            </div>
          </div>
          <div class="event-actions">
            <button class="btn btn-success" @click="verifyEvent(event.id)">✅ Подтвердить</button>
            <button class="btn btn-danger" @click="rejectEvent(event.id)">❌ Отклонить</button>
            <button class="btn" @click="editEvent(event.id)">✏️ Редактировать</button>
          </div>
        </div>
      </div>

      <!-- Секция источников данных -->
      <div  data-aos = "fade-right" v-show="activeTab === 'sources'" class="section">
        <div class="section-title">
          <span>Отслеживаемые источники</span>
          <button class="btn btn-primary" @click="startParsing">🔄 Запустить обход всех источников</button>
        </div>

        <div class="url-list">
          <div v-for="source in sources" :key="source.id" class="url-item">
            <div class="url-info">
              <div class="url-title">{{ source.title }}</div>
              <a :href="source.url" class="url-link" target="_blank">{{ source.url }}</a>
              <div class="last-check">{{ source.lastCheck }}</div>
            </div>
            <div class="url-actions">
              <span :class="['status', `status-${source.status}`]">{{ source.statusLabel }}</span>
              <button class="btn btn-primary" @click="parseSource(source.id)">Парсить</button>
              <button class="btn btn-danger" @click="deleteSource(source.id)">Удалить</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Секция добавления источника -->
      <div  data-aos = "fade-right" v-show="activeTab === 'add-source'" class="section">
        <div class="section-title">
          <span>Добавить новый источник для отслеживания</span>
        </div>

        <div class="url-list">
          <div class="form-group">
            <label>Название источника</label>
            <input v-model="newSource.title" type="text" class="form-control" placeholder="Например: Орловский театр кукол">
          </div>

          <div class="form-group">
            <label>URL страницы с событиями</label>
            <input v-model="newSource.url" type="url" class="form-control" placeholder="https://example.com/events">
          </div>

          <div class="form-group">
            <label>Тип событий</label>
            <select v-model="newSource.type" class="form-control">
              <option v-for="type in eventTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>Периодичность проверки</label>
            <select v-model="newSource.frequency" class="form-control">
              <option v-for="freq in frequencies" :key="freq.value" :value="freq.value">{{ freq.label }}</option>
            </select>
          </div>

          <button class="btn btn-success" style="width: 100%; padding: 15px; font-size: 16px;" @click="addSource">
            ➕ Добавить источник и начать отслеживание
          </button>
        </div>
      </div>

      <!-- Секция настроек -->
      <div  data-aos = "fade-right" v-show="activeTab === 'settings'" class="section">
        <div class="section-title">
          <span>Настройки парсинга и уведомлений</span>
        </div>

        <div class="url-list">
          <div class="form-group">
            <label>Автоматическая проверка источников</label>
            <select v-model="settings.autoCheck" class="form-control">
              <option value="enabled">Включена (рекомендуется)</option>
              <option value="disabled">Выключена</option>
            </select>
          </div>

          <div class="form-group">
            <label>Уведомлять о новых событиях</label>
            <select v-model="settings.notifications" class="form-control">
              <option value="immediately">Сразу после обнаружения</option>
              <option value="verified">Только после проверки</option>
              <option value="disabled">Не уведомлять</option>
            </select>
          </div>

          <div class="form-group">
            <label>Электронная почта для уведомлений</label>
            <input v-model="settings.email" type="email" class="form-control" placeholder="admin@culture-orel.ru">
          </div>

          <div class="form-group">
            <label>Автоматическая публикация проверенных событий</label>
            <select v-model="settings.autoPublish" class="form-control">
              <option value="enabled">Включена</option>
              <option value="disabled">Только после ручного подтверждения</option>
            </select>
          </div>

          <button class="btn btn-primary" style="width: 100%; padding: 15px; font-size: 16px;" @click="saveSettings">
            💾 Сохранить настройки
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// Реактивные данные
const activeTab = ref('events')

const stats = ref([
  { number: 47, label: 'Отслеживаемых источников' },
  { number: 156, label: 'Собранных событий' },
  { number: 23, label: 'Ожидают проверки' }
])

const events = ref([
  {
    id: 1,
    title: 'Выставка "Орловские художники XX века"',
    source: 'Источник: Орловский музей изобразительных искусств',
    type: 'museum',
    typeLabel: 'МУЗЕЙ',
    date: '15 января - 28 февраля 2024',
    time: '10:00 - 18:00 (вт-вс)',
    location: 'ул. Октябрьская, 29',
    price: '200-350 руб.'
  },
  {
    id: 2,
    title: 'Спектакль "Ревизор"',
    source: 'Источник: Орловский государственный театр',
    type: 'theater',
    typeLabel: 'ТЕАТР',
    date: '20 января 2024, 19:00',
    time: 'Продолжительность: 2ч 30м',
    location: 'пл. Ленина, 2',
    price: '400-1200 руб.'
  },
  {
    id: 3,
    title: 'Концерт симфонического оркестра',
    source: 'Источник: Орловская филармония',
    type: 'concert',
    typeLabel: 'КОНЦЕРТ',
    date: '25 января 2024, 18:30',
    time: 'Продолжительность: 2ч',
    location: 'ул. Ленина, 23',
    price: '300-800 руб.'
  }
])

const sources = ref([
  {
    id: 1,
    title: 'Орловский музей изобразительных искусств',
    url: 'https://ogii.ru/events',
    lastCheck: 'Последняя проверка: 2 часа назад • Найдено событий: 5',
    status: 'verified',
    statusLabel: 'АКТИВЕН'
  },
  {
    id: 2,
    title: 'Орловский государственный театр',
    url: 'https://orelteatr.ru/afisha',
    lastCheck: 'Последняя проверка: 1 час назад • Найдено событий: 8',
    status: 'verified',
    statusLabel: 'АКТИВЕН'
  },
  {
    id: 3,
    title: 'Орловская филармония',
    url: 'https://orelfilarmonia.ru/concerts',
    lastCheck: 'Последняя проверка: 30 минут назад • Найдено событий: 12',
    status: 'verified',
    statusLabel: 'АКТИВЕН'
  },
  {
    id: 4,
    title: 'Краеведческий музей Орла',
    url: 'https://okmuseum.ru/exhibitions',
    lastCheck: 'Последняя проверка: 5 часов назад • ОШИБКА ПАРСИНГА',
    status: 'error',
    statusLabel: 'ОШИБКА'
  }
])

const newSource = reactive({
  title: '',
  url: '',
  type: 'museum',
  frequency: '24'
})

const settings = reactive({
  autoCheck: 'enabled',
  notifications: 'verified',
  email: 'admin@culture-orel.ru',
  autoPublish: 'disabled'
})

const tabs = ref([
  { id: 'events', label: 'Собранные события' },
  { id: 'sources', label: 'Источники данных' },
  { id: 'add-source', label: 'Добавить источник' },
  { id: 'settings', label: 'Настройки парсинга' }
])

const eventTypes = ref([
  { value: 'museum', label: 'Музейные выставки' },
  { value: 'theater', label: 'Театральные постановки' },
  { value: 'concert', label: 'Концерты' },
  { value: 'festival', label: 'Фестивали' },
  { value: 'exhibition', label: 'Выставки' },
  { value: 'lecture', label: 'Лекции' }
])

const frequencies = ref([
  { value: '1', label: 'Каждый час' },
  { value: '6', label: 'Каждые 6 часов' },
  { value: '12', label: 'Каждые 12 часов' },
  { value: '24', label: 'Раз в сутки' },
  { value: '168', label: 'Раз в неделю' }
])

// Методы
const showSection = (sectionId) => {
  activeTab.value = sectionId
}

const verifyEvent = (eventId) => {
  alert(`Событие #${eventId} подтверждено и опубликовано!`)
  // TODO: API вызов для подтверждения события
}

const rejectEvent = (eventId) => {
  if (confirm(`Вы уверены, что хотите отклонить событие #${eventId}?`)) {
    alert(`Событие #${eventId} отклонено!`)
    // TODO: API вызов для отклонения события
  }
}

const editEvent = (eventId) => {
  alert(`Редактирование события #${eventId}`)
  // TODO: Открыть форму редактирования
}

const verifyAll = () => {
  if (confirm('Подтвердить все события, ожидающие проверки?')) {
    alert('Все события подтверждены и опубликованы!')
    // TODO: Массовое подтверждение через API
  }
}

const parseSource = (sourceId) => {
  alert(`Запущен парсинг источника #${sourceId}`)
  // TODO: API вызов для запуска парсинга
}

const startParsing = () => {
  alert('Запущен обход всех источников данных...')
  // TODO: API вызов для массового парсинга
}

const deleteSource = (sourceId) => {
  if (confirm(`Удалить источник #${sourceId}?`)) {
    // TODO: API вызов для удаления
    alert(`Источник #${sourceId} удалён`)
  }
}

const addSource = () => {
  if (!newSource.title || !newSource.url) {
    alert('Заполните название и URL')
    return
  }
  // TODO: API вызов для добавления источника
  alert('Источник добавлен!')
  // Сброс формы
  Object.assign(newSource, { title: '', url: '', type: 'museum', frequency: '24' })
}

const saveSettings = () => {
  // TODO: API вызов для сохранения настроек
  alert('Настройки сохранены!')
}
</script>

<style scoped>
/* Все стили из оригинала, скопированные сюда для scoped */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  background: white;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #2c3e50, #34495e);
  color: white;
  padding: 30px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 28px;
  font-weight: 300;
}

.stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #3498db;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
  margin-top: 5px;
}

.tabs {
  display: flex;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.tab {
  padding: 20px 30px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab.active {
  border-bottom-color: #3498db;
  color: #3498db;
  background: white;
}

.content {
  padding: 30px;
}

.section {
  /* display: none; теперь управляется v-show */
}

.section-title {
  font-size: 24px;
  margin-bottom: 25px;
  color: #2c3e50;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn {
  padding: 12px 25px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-success {
  background: #27ae60;
  color: white;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.url-list {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.url-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.url-item:hover {
  border-color: #3498db;
  background: #f8f9fa;
}

.url-info {
  flex: 1;
}

.url-actions {
  display: flex;
  gap: 10px;
}

.url-title {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 5px;
}

.url-link {
  color: #3498db;
  text-decoration: none;
  font-size: 14px;
}

.url-link:hover {
  text-decoration: underline;
}

.last-check {
  font-size: 12px;
  color: #7f8c8d;
  margin-top: 5px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
}

.event-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  border-left: 4px solid #3498db;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.event-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
}

.event-source {
  color: #7f8c8d;
  font-size: 14px;
}

.event-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.event-detail {
  display: flex;
  align-items: center;
  gap: 8px;
}

.event-detail i {
  color: #3498db;
}

.event-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
}

.badge-museum {
  background: #e8f6f3;
  color: #1abc9c;
}

.badge-theater {
  background: #fef9e7;
  color: #f39c12;
}

.badge-concert {
  background: #f4ecf7;
  color: #8e44ad;
}

.status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-verified {
  background: #d1ecf1;
  color: #0c5460;
}

.status-error {
  background: #f8d7da;
  color: #721c24;
}
</style>

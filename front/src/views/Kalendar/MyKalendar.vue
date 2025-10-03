<template>
  <div class="event-calendar">
    <div class="calendar-header">
      <button @click="prevMonth" class="nav-btn"><</button>
      <h2>{{ currentMonthName }} {{ currentYear }}</h2>
      <button @click="nextMonth" class="nav-btn">></button>
    </div>

    <div class="calendar-grid">
      <!-- Заголовки дней недели -->
      <div class="day-header" v-for="day in weekdays" :key="day">
        {{ day }}
      </div>

      <!-- Пустые ячейки до начала месяца -->
      <div v-for="i in blankDays" :key="'blank-' + i" class="empty-day"></div>

      <!-- Дни месяца -->
      <div
        v-for="day in daysInMonth"
        :key="day"
        class="calendar-day"
        :class="{
          'has-event': dayEvents[day]?.length,
          'today': isToday(currentYear, currentMonth, day)
        }"
        @mouseenter="showTooltip($event, day)"
        @mouseleave="hideTooltip"
      >
        {{ day }}
        <div
          v-if="dayEvents[day]?.length"
          class="event-indicator"
          :style="{ backgroundColor: getWarmColor(dayEvents[day].length) }"
        ></div>
      </div>
    </div>

    <!-- Tooltip с деталями события -->
    <div
      v-if="tooltip.visible"
      class="event-tooltip"
      :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }"
    >
      <div v-for="event in tooltip.events" :key="event.id" class="tooltip-event">
        <h4>{{ event.title }}</h4>
        <p><strong>Дата:</strong> {{ formatDate(event.date) }}</p>
        <p v-if="event.location"><strong>Место:</strong> {{ event.location }}</p>
        <p v-if="event.description">{{ event.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Пример данных событий (замените на ваши)
const props = defineProps({
  events: {
    type: Array,
    default: () => []
  }
})

// Состояние календаря
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())

// Tooltip
const tooltip = ref({
  visible: false,
  x: 0,
  y: 0,
  events: []
})

// Названия дней недели
const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

// Вычисляемое: название текущего месяца
const currentMonthName = computed(() => {
  const months = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ]
  return months[currentMonth.value]
})

// Количество дней в месяце
const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
})

// Количество пустых дней до начала месяца
const blankDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
  // В JS: 0 = воскресенье, нам нужно чтобы понедельник был первым
  return firstDay === 0 ? 6 : firstDay - 1
})

// Группируем события по дню месяца
const dayEvents = computed(() => {
  const map = {}
  props.events.forEach(event => {
    const date = new Date(event.date)
    if (
      date.getFullYear() === currentYear.value &&
      date.getMonth() === currentMonth.value
    ) {
      const day = date.getDate()
      if (!map[day]) map[day] = []
      map[day].push(event)
    }
  })
  return map
})

// Навигация
const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

// Проверка, сегодняшний ли день
const isToday = (year, month, day) => {
  const today = new Date()
  return (
    today.getFullYear() === year &&
    today.getMonth() === month &&
    today.getDate() === day
  )
}

// Показать тултип
const showTooltip = (event, day) => {
  const events = dayEvents.value[day] || []
  if (events.length === 0) return

  tooltip.value = {
    visible: true,
    x: event.pageX + 10,
    y: event.pageY + 10,
    events
  }
}

// Скрыть тултип
const hideTooltip = () => {
  tooltip.value.visible = false
}

// Форматирование даты для отображения
const formatDate = (isoDate) => {
  const date = new Date(isoDate)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

// Генерация тёплого цвета (от оранжевого к красному)
const getWarmColor = (count) => {
  // Чем больше событий — тем "горячее" цвет
  const hue = Math.max(0, 30 - count * 5) // от 30 (оранжевый) до 0 (красный)
  return `hsl(${hue}, 80%, 60%)`
}
</script>

<style scoped>
.event-calendar {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 20px;
  position: relative; 
  z-index: 1000000;
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.calendar-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.nav-btn {
  background: #f0f4ff;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  font-size: 1.2rem;
  cursor: pointer;
  color: #4a6cf7;
  transition: background 0.2s;
}

.nav-btn:hover {
  background: #e0e7ff;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.day-header {
  text-align: center;
  font-weight: 600;
  color: #64748b;
  padding: 8px 0;
  font-size: 0.9rem;
}

.empty-day {
  height: 50px;
}

.calendar-day {
  position: relative;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: default;
  transition: background 0.2s;
}

.calendar-day.has-event {
  cursor: pointer;
  background: #667eea;
}

.calendar-day.today {
  background: #e0f2fe;
  font-weight: bold;
  color: #0ea5e9;
}

.calendar-day.has-event:hover {
  background: #667eea;
  transform: scale(1.03);
  z-index: 2;
}

.event-indicator {
  position: absolute;
  bottom: 4px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ff6b35;
}

.event-tooltip {
  position: fixed;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  padding: 12px;
  max-width: 300px;
  z-index: 1000;
  pointer-events: none;
  font-size: 0.95rem;
  line-height: 1.5;
}

.tooltip-event {
  margin-bottom: 10px;
}

.tooltip-event:last-child {
  margin-bottom: 0;
}

.tooltip-event h4 {
  margin: 0 0 6px 0;
  color: #333;
  font-size: 1rem;
}

.tooltip-event p {
  margin: 4px 0;
  color: #555;
  font-size: 0.9rem;
}

.tooltip-event strong {
  color: #4a5568;
}
</style>
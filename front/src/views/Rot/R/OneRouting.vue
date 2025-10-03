<template>
  <div  class="route-card">
    <h3 class="route-title">{{ route.title }}</h3>
    <div class="route-details">
      <div class="detail-item">
        <span class="detail-icon">📍</span>
        <span class="detail-text">{{ route.location || 'Не указано' }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-icon">📏</span>
        <span class="detail-text">{{ route.distance_km ? `${route.distance_km} км` : 'Не указано' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  route: {
    type: Object,
    required: true,
    default: () => ({
      id: 1,
      title: 'Исторический центр Орла',
      description: 'Прогулка по самым значимым историческим местам города...',
      rating: 4.8,
      duration: '2-3 часа',
      distance_km: 5.2,
      difficulty: 'Легкий',
      category: 'История',
      location: 'Орел, Центральный район',
      features: ['Бесплатно', 'Для семьи', 'Фото-точки'],
      featured: true,
      saved: false
    })
  }
})

const emit = defineEmits(['explore', 'save'])

const handleExplore = () => {
  emit('explore', props.route.id)
}

const handleSave = () => {
  emit('save', props.route.id)
}
</script>

<style scoped>
.route-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border-left: 4px solid #8b5cf6;
  transition: all 0.25s ease;
  margin-bottom: 24px;
}

.route-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.route-title {
  margin: 0 0 16px 0;
  font-size: 1.25rem; /* 20px */
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
}

.route-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  color: #475569;
  font-size: 0.95rem;
}

.detail-icon {
  flex-shrink: 0;
  font-size: 1.1rem;
  line-height: 1;
  margin-top: 2px;
}

.detail-text {
  line-height: 1.5;
}
</style>
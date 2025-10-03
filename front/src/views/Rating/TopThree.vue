<template>
      <div class="podium-section">
        <h2 class="section-title">Топ-3 мероприятия</h2>
        <div class="podium">
          <!-- Второе место -->
          <div data-aos="fade-right" data-aos-delay="500" class="podium-item second-place">
            <div class="podium-pedestal">
              <div class="pedestal-base"></div>
              <div class="rank-badge">2</div>
            </div>
            <div class="podium-content">
              <div class="event-card">
                <div class="event-image">
                  <img :src="topEvents[1]?.photo_url" :alt="topEvents[1]?.title" />
                  <div class="image-overlay"></div>
                </div>
                <div class="event-info">
                  <h3 class="event-title">{{ topEvents[1]?.title }}</h3>
                  <div class="event-rating">
                    <span class="pi pi-star-fill"></span>
                    <span class="rating-value">{{ topEvents[1]?.rating }}</span>
                  </div>
                 
                  <div class="event-stats">
                    <div class="stat">
                      <span class="pi pi-users"></span>
                      <span>{{ topEvents[1]?.participants }} участников</span>
                    </div>
                    <div class="stat">
                      <span class="pi pi-calendar"></span>
                      <span>{{ topEvents[1]?.date }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Первое место -->
          <div data-aos="fade-down" data-aos-delay="900" class="podium-item first-place">
            <div class="podium-pedestal">
              <div class="pedestal-base"></div>
              <div class="rank-badge">1</div>
            </div>
            <div class="podium-content">
              <div class="event-card">
                <div class="event-image">
                  <img :src="topEvents[0]?.photo_url" :alt="topEvents[0]?.title" />
                  <div class="image-overlay"></div>
                  <div class="crown-icon">
                    <span class="pi pi-crown"></span>
                  </div>
                </div>
                <div class="event-info">
                  <h3 class="event-title">{{ topEvents[0]?.title }}</h3>
                  <div class="event-rating">
                    <span class="pi pi-star-fill"></span>
                    <span class="rating-value">{{ topEvents[0]?.rating }}</span>
                  </div>
                
                  <div class="event-stats">
                    <div class="stat">
                      <span class="pi pi-users"></span>
                      <span>{{ topEvents[0]?.participants }} участников</span>
                    </div>
                    <div class="stat">
                      <span class="pi pi-calendar"></span>
                      <span>{{ topEvents[0]?.date }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Третье место -->
          <div data-aos="fade-left" data-aos-delay="50" class="podium-item third-place">
            <div class="podium-pedestal">
              <div class="pedestal-base"></div>
              <div class="rank-badge">3</div>
            </div>
            <div class="podium-content">
              <div class="event-card">
                <div class="event-image">
                  <img :src="topEvents[2]?.photo_url" :alt="topEvents[2]?.title" />
                  <div class="image-overlay"></div>
                </div>
                <div class="event-info">
                  <h3 class="event-title">{{ topEvents[2]?.title }}</h3>
                  <div class="event-rating">
                    <span class="pi pi-star-fill"></span>
                    <span class="rating-value">{{ topEvents[2]?.rating }}</span>
                  </div>
                 
                  <div class="event-stats">
                    <div class="stat">
                      <span class="pi pi-users"></span>
                      <span>{{ topEvents[2]?.participants }} участников</span>
                    </div>
                    <div class="stat">
                      <span class="pi pi-calendar"></span>
                      <span>{{ topEvents[2]?.date }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  </template>
  
  <script setup>
import { computed } from 'vue'

const props = defineProps({
  topEvents: {
    type: Array,
    required: true,
    validator: (value) => {
      if (!Array.isArray(value) || value.length !== 3) {
        console.warn('PodiumComponent: topEvents должен быть массивом из 3 элементов')
        return false
      }
      
      // Проверяем обязательные поля для каждого мероприятия
      return value.every((event, index) => {
        const hasRequiredFields = event && 
          typeof event === 'object' && 
          'id' in event && 
          'title' in event && 
          'rating' in event &&
          'image' in event
        
        if (!hasRequiredFields) {
          console.warn(`PodiumComponent: мероприятие ${index} отсутствуют обязательные поля (id, title, rating, image)`)
        }
        
        return hasRequiredFields
      })
    }
  },
  
  // Опциональные пропсы
  title: {
    type: String,
    default: 'Топ-3 мероприятия'
  },
  
  showAnimations: {
    type: Boolean,
    default: true
  },
  
  compact: {
    type: Boolean,
    default: false
  }
})




// Вычисляемые свойства для адаптации данных
const firstPlaceEvent = computed(() => props.topEvents[0])
const secondPlaceEvent = computed(() => props.topEvents[1]) 
const thirdPlaceEvent = computed(() => props.topEvents[2])

// Форматирование чисел
const formatParticipants = (count) => {
  if (count >= 1000) {
    return `${(count / 1000).toFixed(1)}k`
  }
  return count.toString()
}

// CSS классы на основе пропсов
const podiumClasses = computed(() => ({
  'podium-section': true,
  'compact-mode': props.compact,
  'no-animations': !props.showAnimations
}))

  </script>
  
  <style scoped>
 
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
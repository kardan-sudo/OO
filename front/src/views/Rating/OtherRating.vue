<template>
    <div data-aos = "flip-up" class="rating-item" >
      <div class="rank-number">
            {{ event.rating }}
        <span class="star"  >★</span>
    </div>
      <div class="event-content">
        <div class="event-image">
          <img :src="event.photo_url" :alt="event.title" />
        </div>
        <div class="event-details">
          <h3 class="event-title">{{ event.title }}</h3>
          <p class="event-description">{{ event.description }}</p>
          <div class="event-meta">
            <div class="rating">
              <span class="pi pi-star-fill"></span>
              <span>{{ event.rating }}</span>
            </div>
            <div class="participants">
              <span class="pi pi-users"></span>
              <span>{{ event.participants }}</span>
            </div>
            <div class="date">
              <span class="pi pi-calendar"></span>
              <span>{{ formattedDate }}</span>
            </div>
          </div>
        </div>
      </div>
      <button class="details-btn" @click="handleDetailsClick">
        <span class="pi pi-arrow-right"></span>
      </button>
    </div>
  </template>
  
  <script setup>
  import { computed, onMounted } from 'vue'
  import { useEventsStore } from '@/stores/storeEvents'
  const ev = useEventsStore()
  const props = defineProps({
    // Обязательные пропсы
    event: {
      type: Object,
      required: true,
      validator: (value) => {
        const requiredFields = ['id', 'title', 'description', 'rating', 'participants', 'date', 'image']
        return requiredFields.every(field => field in value)
      }
    },
    // Опциональные пропсы
    showRank: {
      type: Boolean,
      default: true
    },
    
    showImage: {
      type: Boolean,
      default: true
    },
    
    showDescription: {
      type: Boolean,
      default: true
    },
    
    showMeta: {
      type: Boolean,
      default: true
    },
    
    compact: {
      type: Boolean,
      default: false
    },
    
    clickable: {
      type: Boolean,
      default: true
    },
    
    // Кастомные классы
    customClasses: {
      type: Object,
      default: () => ({})
    }
  })
      console.log(props.rank);
  // Emits для обработки событий
  const emit = defineEmits(['details-click', 'rank-click', 'image-click'])
  
  // Вычисляемые свойства
  const formattedDate = computed(() => {
    if (!props.event.date) return ''
    
    try {
      const date = new Date(props.event.date)
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    } catch {
      return props.event.date
    }
  })
  
  const formattedParticipants = computed(() => {
    const participants = props.event.participants
    if (participants >= 1000) {
      return `${(participants / 1000).toFixed(1)}k`
    }
    return participants.toString()
  })
  
  const ratingColor = computed(() => {
    const rating = props.event.rating
    if (rating >= 4.5) return 'high-rating'
    if (rating >= 4.0) return 'medium-rating'
    return 'low-rating'
  })
  

  
  // CSS классы на основе пропсов
  const componentClasses = computed(() => ({
    'rating-item': true,
    'featured': props.event.featured,
    'compact': props.compact,
    'clickable': props.clickable,
    'no-image': !props.showImage,
    'no-description': !props.showDescription,
    'no-meta': !props.showMeta,
    ...props.customClasses
  }))
  onMounted(()=>{
    ev.fetchEvents()
  })
  </script>
  
  <style scoped>
  .star {
  color: #f59e0b;
  font-size: 1.1rem;
}
.star.active {
  color: #f59e0b;
}
  .rating-item {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1rem;
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
  
  .rating-item.compact {
    padding: 1rem;
    gap: 1rem;
  }
  
  .rating-item.clickable {
    cursor: pointer;
  }
  
  .rating-item.no-image .event-image {
    display: none;
  }
  
  .rating-item.no-description .event-description {
    display: none;
  }
  
  .rating-item.no-meta .event-meta {
    display: none;
  }
  
  /* Rank number */
  .rank-number {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-muted);
    min-width: 50px;
    text-align: center;
    transition: color var(--transition-normal);
  }
  
  .rating-item:hover .rank-number {
    color: var(--text-primary);
  }
  
  .rating-item.featured .rank-number {
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  /* Event content */
  .event-content {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex: 1;
  }
  
  .rating-item.compact .event-content {
    gap: 1rem;
  }
  
  /* Event image */
  .event-image {
    width: 80px;
    height: 80px;
    border-radius: var(--radius-md);
    overflow: hidden;
    flex-shrink: 0;
    cursor: pointer;
    transition: transform var(--transition-normal);
  }
  
  .event-image:hover {
    transform: scale(1.05);
  }
  
  .rating-item.compact .event-image {
    width: 60px;
    height: 60px;
  }
  
  .event-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  /* Event details */
  .event-details {
    flex: 1;
  }
  
  .rating-item.compact .event-details {
    min-width: 0;
  }
  
  .event-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    line-height: 1.3;
  }
  
  .rating-item.compact .event-title {
    font-size: 1rem;
    margin-bottom: 0.25rem;
  }
  
  .event-description {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.4;
    margin-bottom: 0.5rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .rating-item.compact .event-description {
    font-size: 0.85rem;
    -webkit-line-clamp: 1;
  }
  
  /* Event meta */
  .event-meta {
    display: flex;
    gap: 1.5rem;
    font-size: 0.85rem;
    color: var(--text-muted);
  }
  
  .rating-item.compact .event-meta {
    gap: 1rem;
    font-size: 0.8rem;
  }
  
  .event-meta > div {
    display: flex;
    align-items: center;
    gap: 0.3rem;
  }
  
  .rating.high-rating {
    color: #10b981;
  }
  
  .rating.medium-rating {
    color: #f59e0b;
  }
  
  .rating.low-rating {
    color: #ef4444;
  }
  
  /* Details button */
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
  
  .rating-item.compact .details-btn {
    width: 35px;
    height: 35px;
  }
  
  /* Адаптивность */
  @media (max-width: 768px) {
    .rating-item {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }
  
    .event-content {
      flex-direction: column;
      text-align: center;
      gap: 1rem;
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
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .rating-item {
    animation: fadeInUp 0.5s ease-out;
  }
  </style>
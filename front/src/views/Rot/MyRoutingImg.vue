<!-- components/ImagePreview.vue -->
<template>
  <div class="image-preview">

    <a 
      :href="srcc" 
      target="_blank"
      rel="noopener noreferrer"
      class="image-link"
    >
      Построить маршрут в Яндекс картах
    </a>
    <img 
      :src="photoUrl" 
      :alt="`Фото маршрута`"
      class="preview-image"
      @error="handleError"
    />
  </div>
</template>

<script setup>
defineProps({
  photoUrl: {
    type: String,
    required: true
  },
  srcc: {
    type: String,
    required: true
  }
})

const handleError = (e) => {
  console.error('Не удалось загрузить фото:', e.target.src)
  e.target.src = '/images/placeholder.jpg'
}
</script>

<style scoped>
.image-preview {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.25rem; /* отступ между ссылкой и изображением */
  margin-top: 0;
}

/* Стилизованная ссылка */
.image-link {
  font-size: 0.95rem;
  color: #3b82f6; /* синий цвет (tailwind-like) */
  text-decoration: none;
  padding: 8px 16px;
  background: rgba(59, 130, 246, 0.08); /* светлый фон под ссылку */
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, 0.2);
  transition: all 0.25s ease;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
  font-weight: 500;
}

.image-link:hover {
  background: rgba(59, 130, 246, 0.15);
  color: #2563eb;
  border-color: rgba(59, 130, 246, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.image-link:active {
  transform: translateY(0);
}

.preview-image {
  max-width: 100%;
  max-height: 80vh;
  width: auto;
  height: auto;
  border-radius: 16px;
  box-shadow: 
    0 10px 30px -10px rgba(0, 0, 0, 0.25),
    0 20px 40px -20px rgba(0, 0, 0, 0.2);
  object-fit: contain;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.preview-image:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 
    0 12px 35px -8px rgba(0, 0, 0, 0.3),
    0 24px 48px -16px rgba(0, 0, 0, 0.25);
}
</style>
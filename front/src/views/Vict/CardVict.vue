<template>
  <div class="quiz-card" data-aos="fade-up">
    <!-- Верхняя часть с градиентом -->
    <div class="quiz-header">
      <div class="header-overlay"></div>
      <div class="quiz-badge">
        {{ quiz.prize }}
      </div>
      <div class="header-shape"></div>
    </div>

    <!-- Основной контент -->
    <div class="quiz-content">
      <!-- Заголовок и описание -->
      <div class="quiz-info">
        <div class="title-wrapper">
          <h3 class="quiz-title">{{ quiz.title }}</h3>
          <div class="title-accent"></div>
        </div>
        <p class="quiz-description">{{ quiz.description }}</p>
      </div>

      <!-- Упрощённая статистика: только количество вопросов -->
      <div class="quiz-stats">
        <div class="stat-item">
          <div class="stat-icon">
            <i class="pi pi-question"></i>
          </div>
          <span class="stat-value">{{ quiz.questions_count }}</span>
          <span class="stat-label">вопросов</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  quiz: {
    type: Object,
    required: true,
    validator: (q) => q.title && q.description && q.prize !== undefined && q.questions_count !== undefined
  }
})
</script>

<style scoped>
/* Цветовая палитра — твои тона, но с живостью */
.quiz-card,
.quiz-card * {
  --primary-500: #8b5cf6;
  --primary-600: #7c3aed;
  --primary-700: #6d28d9;
  --accent-500: #6366f1;
  --accent-600: #4f46e5;
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --text-primary: #1e1b4b;
  --text-secondary: #4c4a73;
  --text-muted: #7c7a9d;
  --border-light: #e5e7eb;
  --border-medium: #d1d5db;
  --primary-gradient: linear-gradient(135deg, var(--accent-500), var(--primary-500));
  --shadow-sm: 0 2px 6px rgba(139, 92, 246, 0.12);
  --shadow-lg: 0 10px 25px rgba(109, 40, 217, 0.15);
  --shadow-xl: 0 20px 40px rgba(109, 40, 217, 0.2);
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 18px;
  --transition-normal: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.quiz-card {
  position: relative;
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  transition: var(--transition-normal);
  max-width: 400px;
  margin: 0 auto;
  border: 1px solid var(--border-light);
}

.quiz-card:hover {
  transform: translateY(-8px) scale(1.015);
  box-shadow: var(--shadow-xl);
  border-color: var(--primary-500);
}

/* Хедер — насыщенный градиент */
.quiz-header {
  position: relative;
  height: 120px;
  padding: 16px;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  overflow: hidden;
  background: var(--primary-gradient); /* яркий градиент */
}

.header-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, transparent 100%);
}

.header-shape {
  position: absolute;
  bottom: -15px;
  left: -15px;
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
}

/* Бейдж — теперь с насыщенным фоном */
.quiz-badge {
  position: relative;
  z-index: 2;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  
  /* Цветной градиент вместо полупрозрачного */
  background: linear-gradient(135deg, var(--accent-600), var(--primary-600));
  color: white;
  box-shadow: 0 4px 12px rgba(109, 40, 217, 0.3);
  
  white-space: normal;
  word-break: break-word;
  text-align: center;
  max-width: calc(100% - 32px);
  line-height: 1.3;
}

.quiz-content {
  padding: 20px 20px 24px;
  position: relative;
  z-index: 2;
}

.title-wrapper {
  position: relative;
  margin-bottom: 12px;
}

/* Заголовок — градиентный текст */
.quiz-title {
  font-size: 1.4rem;
  font-weight: 800;
  margin-bottom: 6px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  /* Градиентный текст из твоей палитры */
  background: linear-gradient(135deg, var(--primary-600), var(--accent-500));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-accent {
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 36px;
  height: 3px;
  background: var(--primary-gradient); /* яркая акцентная полоса */
  border-radius: 2px;
}

.quiz-description {
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 20px;
  font-size: 0.93rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Статистика — цветной фон */
.quiz-stats {
  display: flex;
  justify-content: center;
  padding: 16px;
  background: rgba(139, 92, 246, 0.04); /* очень мягкий фиолетовый тон */
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
  border: 2px solid var(--primary-500); /* цветная рамка */
}

.stat-icon i {
  font-size: 16px;
  color: var(--primary-600); /* насыщенный фиолетовый */
}

.stat-value {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--primary-700); /* тёмно-фиолетовый */
}

.stat-label {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

/* Адаптивность */
@media (max-width: 480px) {
  .quiz-card {
    max-width: 100%;
  }
  
  .quiz-header {
    height: 110px;
    padding: 12px;
  }
  
  .quiz-badge {
    font-size: 11px;
    padding: 5px 10px;
    max-width: calc(100% - 24px);
  }
  
  .quiz-content {
    padding: 16px;
  }
  
  .quiz-title {
    font-size: 1.25rem;
  }
  
  .quiz-description {
    font-size: 0.9rem;
    -webkit-line-clamp: 4;
  }
}
</style>
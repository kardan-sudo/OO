<template>
  <div class="achievements">
    <h3>🏆 Ачивки пользователя</h3>
    <div class="achievements-list">
      <div 
        v-for="achievement in getUser.achievements" 
        :key="achievement.id"
        :class="['achievement-item', { 'earned': achievement.earned }]"
      >
        <span class="achievement-icon">
          {{ achievement.earned ? '✅' : '⭕' }}
        </span>
        <span class="achievement-name">{{ achievement.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/useUserStore';
import { storeToRefs } from 'pinia';

const {getUser} = storeToRefs(useUserStore())
</script>

<style scoped>
.achievements {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.achievements-list {
  margin-top: 15px;
}

.achievement-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 8px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.achievement-item.earned {
  background: #f8fff9;
  border-left: 4px solid #28a745;
}

.achievement-item:not(.earned) {
  background: #f8f9fa;
  border-left: 4px solid #6c757d;
}

.achievement-icon {
  margin-right: 10px;
  font-size: 16px;
}

.achievement-name {
  font-weight: 500;
}


@media (max-width: 960px) {
  .achievements {
    padding: 15px;
  }
  
  .achievement-item {
    padding: 12px 8px;
  }
  
  h3 {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .achievements {
    padding: 12px;
  }
  
  .achievement-name {
    font-size: 14px;
  }
  
  .achievement-icon {
    font-size: 14px;
    margin-right: 8px;
  }
}
</style>
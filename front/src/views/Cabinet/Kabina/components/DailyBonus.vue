<template>

  <div class="daily-bonus">
    <div class="Text_">
        <h3>🎁 Уровень: {{ getUser.consecutive_days }}</h3>
    <h3>Ваш уровень орла:</h3>
    <h1>{{LevelEagle}} </h1>
    </div>
    <div class="UnderImage">
        <img :src="LevelEagleImg" alt=""></img>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/useUserStore'
import { computed } from 'vue'
import eagle1 from '../Eagles/StoneEagle.png'
import eagle2 from '../Eagles/StoneEagle.png'
import eagle3 from '../Eagles/СopperEagle.png'
import eagle4 from '../Eagles/SiliverEagle.png'
import eagle5 from '../Eagles/GoldEagle.png'
import eagle6 from '../Eagles/TitanEagle.png'
import eagle7 from '../Eagles/LazurEagle.png'
import eagle8 from '../Eagles/GranatEagle.png'
import eagle9 from '../Eagles/BriliantEagle.png'
import { storeToRefs } from 'pinia'

const eagleImages = [
    eagle1, eagle2, eagle3, eagle4, eagle5, eagle6, eagle7, eagle8, eagle9,
    // ... добавьте остальные изображения
]

const {getUser} = storeToRefs(useUserStore())



const LevelEagleImg = computed(() => {
    const level = getUser.consecutive_days / 10
    switch (Math.floor(level)) {
        case 0: return eagleImages[0]
        case 1: return eagleImages[1]
        case 2: return eagleImages[2]
        case 3: return eagleImages[3]
        case 4: return eagleImages[4]
        case 5: return eagleImages[5]
        case 6: return eagleImages[6]
        case 7: return eagleImages[7]
        case 8: return eagleImages[8]
        default: return eagleImages[8]
    }
})

const LevelEagle = computed(() => {
    const level = getUser.consecutive_days / 10
    switch (Math.floor(level)) {
        case 0: return "деревянный"
        case 1: return "каменный"
        case 2: return "медный"
        case 3: return "серебрянный"
        case 4: return "золотой"
        case 5: return "титановый"
        case 6: return "лазурный"
        case 7: return "гранатовый"
        case 8: return "брильянтовый"
        default: return "брильянтовый"
    }
})

</script>

<style scoped>
.Text_ {
    width: 300px;
}

img {
    max-width: 200px;
    margin-left: 10px;
}

.UnderImage
 {
width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
 }

.daily-bonus {
display: flex;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}


.level {
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.progress {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.progress-bar {
  flex: 1;
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: bold;
  color: #333;
  min-width: 40px;
}

.collect-btn {
  width: 100%;
  padding: 12px;
  background: #ffc107;
  color: #212529;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.collect-btn:disabled {
  background: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

.collect-btn:not(:disabled):hover {
  background: #e0a800;
  transform: translateY(-2px);
}

@media (max-width: 960px) {
  .daily-bonus {
    flex-direction: column;
    text-align: center;
    padding: 15px;
  }
  
  .Text_ {
    width: 100%;
    margin-bottom: 20px;
  }
  
  img {
    max-width: 150px;
    margin-left: 0;
  }
  
  h3 {
    font-size: 1.2rem;
  }
  
  h1 {
    font-size: 1.8rem;
  }
}

@media (max-width: 480px) {
  .daily-bonus {
    padding: 12px;
  }
  
  img {
    max-width: 120px;
  }
  
  h3 {
    font-size: 1.1rem;
  }
  
  h1 {
    font-size: 1.5rem;
  }
}
</style>
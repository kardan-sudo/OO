<template>
  <div class="dna-wrapper">
    <div class="dna-container">
      <div class="dna-strand" :style="dnaStyle">
        <div class="axis"></div>
        
        <!-- Сферы -->
        <div
          v-for="(sphere, index) in spheres"
          :key="'sphere-' + index"
          class="sphere-3d"
          :class="{
            'pulse': true,
            'blue-sphere': sphere.color === 0,
            'red-sphere': sphere.color === 1
          }"
          :style="sphere.style"
        >
          <div class="sphere-surface">
            <div class="shine"></div>
          </div>
        </div>
        
        <!-- Штанги -->
        <div
          v-for="(rod, index) in rods"
          :key="'rod-' + index"
          class="connection-rod"
          :style="rod.style"
        ></div>
        
        <!-- Парящие частицы -->
        <div
          v-for="(particle, index) in particles"
          :key="'particle-' + index"
          class="particle"
          :style="particle.style"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDNKStore } from '../stores/DNKstore'
import { storeToRefs } from 'pinia'
// Пропсы

const DNKdata = useDNKStore()


// Константы
const nodesCount = 12
const sphereSize = ref(24)
const rodThickness = ref(5)

// Реактивные данные
const spheres = ref([])
const rods = ref([])
const particles = ref([])

// Адаптивные размеры
const containerSize = computed(() => {
  if (typeof window === 'undefined') return { width: 300, height: 400 }
  
  const width = window.innerWidth
  if (width < 480) {
    sphereSize.value = 16
    rodThickness.value = 4
    return { width: 180, height: 280 }
  } else if (width < 768) {
    sphereSize.value = 18
    rodThickness.value = 4
    return { width: 200, height: 300 }
  } else if (width < 1024) {
    sphereSize.value = 20
    rodThickness.value = 4
    return { width: 250, height: 350 }
  } else {
    sphereSize.value = 24
    rodThickness.value = 5
    return { width: 300, height: 400 }
  }
})

const radius = computed(() => containerSize.value.width * 0.27)
const height = computed(() => containerSize.value.height * 0.85)

// Стиль для DNA strand
const dnaStyle = computed(() => ({
  transform: 'translate(-50%, -50%)'
}))

// Инициализация сфер с цветами из массива
const initializeSpheres = () => {
  const newSpheres = []

  for (let i = 0; i < nodesCount; i++) {
    const angle = (i / nodesCount) * Math.PI * 2
    const y = (i / (nodesCount - 1)) * height.value - height.value / 2

    // Позиции для объемного эффекта
    const leftX = Math.cos(angle) * radius.value
    const rightX = Math.cos(angle + Math.PI) * radius.value
    const leftZ = Math.sin(angle) * 25
    const rightZ = Math.sin(angle + Math.PI) * 25

    // Проверяем наличие данных и берём значения или 0
    const leftColor = (DNKdata.DNKdata && DNKdata.DNKdata[i * 2] !== undefined) ? DNKdata.DNKdata[i * 2] : 0
    const rightColor = (DNKdata.DNKdata && DNKdata.DNKdata[i * 2 + 1] !== undefined) ? DNKdata.DNKdata[i * 2 + 1] : 0

    // Левая сфера
    newSpheres.push({
      color: leftColor,
      style: {
        transform: `translate(-50%, -50%) translateX(${leftX}px) translateY(${y}px) translateZ(${leftZ}px)`
      }
    })

    // Правая сфера
    newSpheres.push({
      color: rightColor,
      style: {
        transform: `translate(-50%, -50%) translateX(${rightX}px) translateY(${y}px) translateZ(${rightZ}px)`
      }
    })
  }

  spheres.value = newSpheres
}


// Инициализация штанг
const initializeRods = () => {
  const newRods = []
  
  for (let i = 0; i < nodesCount; i++) {
    const angle = (i / nodesCount) * Math.PI * 2
    const y = (i / (nodesCount - 1)) * height.value - height.value / 2
    
    // Позиции для объемного эффекта
    const leftX = Math.cos(angle) * radius.value
    const rightX = Math.cos(angle + Math.PI) * radius.value
    const leftZ = Math.sin(angle) * 25
    const rightZ = Math.sin(angle + Math.PI) * 25
    
    // Расчет параметров штанги
    const dx = rightX - leftX
    const dz = rightZ - leftZ
    const rodLength = Math.sqrt(dx * dx + dz * dz)
    const rodCenterX = (leftX + rightX) / 2
    const rodCenterY = y
    const rodCenterZ = (leftZ + rightZ) / 2
    const rodAngle = Math.atan2(dz, dx) * 180 / Math.PI
    
    // Смещаем штангу чтобы она не пронизывала шарики
    const adjustedLength = rodLength - sphereSize.value
    const offset = sphereSize.value / 2
    
    newRods.push({
      style: {
        width: `${adjustedLength}px`,
        height: `${rodThickness.value}px`,
        transform: `translate(-50%, -50%) translateX(${rodCenterX}px) translateY(${rodCenterY}px) translateZ(${rodCenterZ}px) rotateY(${-rodAngle}deg) translateX(${offset}px)`
      }
    })
  }
  
  rods.value = newRods
}

// Инициализация частиц
const initializeParticles = () => {
  const newParticles = []
  const particleCount = window.innerWidth < 768 ? 4 : 6
  const particleSize = window.innerWidth < 480 ? '4px' : '6px'
  
  for (let i = 0; i < particleCount; i++) {
    const animationDuration = 3 + Math.random() * 4
    const maxX = containerSize.value.width * 0.8
    const maxY = containerSize.value.height * 0.6
    const maxZ = 60
    
    newParticles.push({
      style: {
        width: particleSize,
        height: particleSize,
        transform: `translate(-50%, -50%) translateX(${(Math.random() - 0.5) * maxX}px) translateY(${(Math.random() - 0.5) * maxY}px) translateZ(${(Math.random() - 0.5) * maxZ}px)`,
        opacity: '0.5',
        animation: `particleFloat ${animationDuration}s infinite ease-in-out`,
        boxShadow: '0 0 8px rgba(135, 206, 235, 0.6)'
      }
    })
  }
  
  particles.value = newParticles
}

// Реинициализация при изменении размера окна
const handleResize = () => {
  initializeSpheres()
  initializeRods()
  initializeParticles()
}

// Инициализация при монтировании
onMounted(() => {
  initializeSpheres()
  initializeRods()
  initializeParticles()
  
  // Добавляем обработчик изменения размера окна
  window.addEventListener('resize', handleResize)
})

// Убираем обработчик при размонтировании
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', handleResize)
  }
})
</script>

<style scoped>
.dna-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}



@keyframes titleGlow {
  0% {
    text-shadow: 
      0 0 10px rgba(74, 144, 226, 0.7),
      0 0 20px rgba(74, 144, 226, 0.5),
      0 0 30px rgba(74, 144, 226, 0.3);
  }
  100% {
    text-shadow: 
      0 0 15px rgba(74, 144, 226, 0.9),
      0 0 25px rgba(74, 144, 226, 0.7),
      0 0 35px rgba(74, 144, 226, 0.5);
  }
}

@keyframes borderGlow {
  0% {
    opacity: 0.3;
    box-shadow: 0 0 10px rgba(74, 144, 226, 0.3);
  }
  100% {
    opacity: 0.6;
    box-shadow: 0 0 20px rgba(74, 144, 226, 0.5);
  }
}

.dna-container {
  position: relative;
  width: 300px;
  height: 400px;
  margin: 0 auto;
  perspective: 1200px;
}

.dna-strand {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-style: preserve-3d;
  animation: swing 6s infinite ease-in-out;
}

/* 3D сфера */
.sphere-3d {
  position: absolute;
  transform-style: preserve-3d;
  width: 24px;
  height: 24px;
}

.sphere-surface {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  transform-style: preserve-3d;
  box-shadow: 
    0 0 25px rgba(74, 144, 226, 0.9),
    inset -8px -8px 15px rgba(0, 0, 0, 0.6),
    inset 5px 5px 10px rgba(255, 255, 255, 0.4);
}

/* Синие шарики (0) */
.blue-sphere .sphere-surface {
  background: radial-gradient(circle at 30% 30%, #5b9eea, #365dc8);
}

/* Красные шарики (1) */
.red-sphere .sphere-surface {
  background: radial-gradient(circle at 30% 30%, #0805a7, #010344);
}

/* Горизонтальные штанги */
.connection-rod {
  position: absolute;
  transform-style: preserve-3d;
  background: linear-gradient(90deg, #1e3a8a, #4a90e2, #87ceeb);
  border-radius: 4px;
  box-shadow: 0 0 12px rgba(74, 144, 226, 0.7);
}

@keyframes swing {
  0%, 100% {
    transform: translate(-50%, -50%) rotateY(-45deg);
  }
  50% {
    transform: translate(-50%, -50%) rotateY(45deg);
  }
}

.pulse {
  animation: pulse 4s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.3);
  }
}

@keyframes particleFloat {
  0%, 100% {
    transform: translate(-50%, -50%) translateX(var(--start-x, 0)) translateY(var(--start-y, 0)) translateZ(var(--start-z, 0));
    opacity: 0.3;
  }
  50% {
    transform: translate(-50%, -50%) translateX(calc(var(--start-x, 0) * 1.2)) translateY(calc(var(--start-y, 0) * 1.2)) translateZ(calc(var(--start-z, 0) + 20px));
    opacity: 0.8;
  }
}

/* Центральная ось */
.axis {
  position: absolute;
  width: 2px;
  height: 100%;
  background: linear-gradient(to bottom, transparent, #4a90e2, transparent);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.2;
  filter: blur(1px);
}

/* Блик для сфер */
.shine {
  position: absolute;
  width: 30%;
  height: 30%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
  top: 20%;
  left: 20%;
  filter: blur(1px);
}

/* Парящие частицы */
.particle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, #87ceeb, #4a90e2);
}

/* Адаптивность */
@media (max-width: 768px) {
  .dna-container {
    width: 250px;
    height: 350px;
    perspective: 800px;
  }
  
  .sphere-3d {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .dna-container {
    width: 200px;
    height: 300px;
    perspective: 600px;
  }
  
  .sphere-3d {
    width: 18px;
    height: 18px;
  }
  
  .genetic-code-title h2 {
    font-size: 1.1rem;
    padding: 8px 16px;
  }
}

@media (max-width: 360px) {
  .dna-container {
    width: 180px;
    height: 280px;
  }
  
  .sphere-3d {
    width: 16px;
    height: 16px;
  }
}
</style>
<template>
    <!-- Модальное окно с поздравлением -->
    <div class="reward-modal" v-if="showReward" :class="{ 'closing': isClosing }">
        <div class="reward-content">
            <div class="reward-layout">
                <div class="image-container">
                    <img :src="currentEagleImage" class="reward-image" :class="{'new-eagle': isNewEagle}">
                </div>
                <div class="text-container">
                    <h3>Поздравляем!</h3>
                    <p v-if="currentDay%10==0 && currentDay<91">Ваш орел вырос</p>
                    <p>Вы достигли <span class="eagle-level">{{ currentDay }} дня</span></p>
                    <p v-if="currentDay%10!==0">Ещё {{ 10 - currentDay%10}} дня до бонуса</p>
                    <button class="thanks-btn" @click="closeReward" :disabled="isClosing">
                        {{ isClosing ? '...' : 'Спасибо' }}
                    </button>
                </div>
            </div>
        </div>
    </div>


    <!-- Модальное окно с бонусной картой -->
    <div class="reward-modal" v-if="showBonusCard" :class="{ 'closing': isClosingBonusCard }">
        <div class="reward-content">
            <div class="reward-layout">
                <div class="text-container">
                    <h3>Поздравляем!</h3>
                    <p>Вы получили бонус</p>
                    <p>{{ bonusText }}</p>
                    <button class="thanks-btn" @click="closeRewardBonus" :disabled="isClosingBonusCard">
                        {{ isClosingBonusCard ? '...' : 'Спасибо' }}
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Анимация смены орла -->
    <div class="eagle-transition" v-if="showEagleTransition && currentDay<91">
        <div class="transition-container">
            <img :src="oldEagleImage" class="eagle-old" :class="{'fading': isTransitioning}">
            <img :src="transitionNewImage" class="eagle-new" :class="{'appearing': isTransitioning}">
        </div>
    </div>
    
    <div class="progression-tree">
        <div 
            class="tree-container"
            ref="treeContainer"
            :class="{ 'no-transition': isDragging }
            "
            @mousedown="startDrag"
            @mousemove="onDrag"
            @mouseup="stopDrag"
            @mouseleave="stopDrag"
            :style="{ transform: `translateX(${scrollPosition}px)` }"
        >
            <!-- Летающий орел находится внутри контейнера, чтобы он автоматически смещался при transform -->
            <div class="flying-eagle" :class="{ jumping: isJumping }" :style="{ left: eagleLeft + 'px' }">
                <img :src="currentEagleImage" class="eagle-flying">
            </div>


            <div
                v-for="(day, index) in progressionDays" 
                :key="index"
                class="day-item"
                :class="{ 
                    'completed': day.isCompleted,
                    'future': !day.isCompleted,
                    'eagle-perch': (index + 1) % 10 === 0,
                    'current-eagle': index === currentDay - 1
                }"
            >
                <!-- Линия между уровнями -->
                <div 
                    v-if="index < progressionDays.length && index != 0"
                    class="connection-line"
                    :class="{ 
                        'completed': day.isCompleted,
                    }"
                >
                    <div 
                        class="line-fill"
                        :class="{ 'animating': !day.isCompleted }"
                    ></div>
                </div>

                <!-- Точка уровня -->
                <div class="level-dot"
                @mouseenter="showBonus(index + 1, $event)"
                @mouseleave="hideBonus">
                    <div class="inner-dot">
                        
                    </div>
                    <span class="day-number">День {{ index + 1 }}</span>
                    
                    <!-- Орел на точках кратных 10 -->
                    <div class="eagle-perch-spot" v-if="(index + 1) % 10 === 0">
                        <img 
                            :src="getEagleForLevel(index + 1)" 
                            class="eagle-on-perch"
                            :class="{'completed': day.isCompleted}"
                            @click="jumpToEagle(index + 1)"
                        >
                    </div>
                </div>
                
 
            </div>
        </div>
        
        <!-- Индикатор прокрутки -->
        <div class="scroll-indicator" v-if="showScrollIndicator">
            ← Перетащите для прокрутки →
        </div>
        
        <div class="controls">
            <button @click="completeDay" :disabled="currentDay >= totalDays || IsLogined === true || loggedInToday === true">      
                Получить уровень
            </button>
            <button @click="centerTree">
                Где я?
            </button>
        </div>
    </div>

  <teleport to="body">
    <div 
      class="bonus-popup" 
      v-if="bonusVisible"
      :style="{ left: popupX + 'px', top: popupY + 'px' }"
    >
      <BonusCard :level="bonusLevel"/>
    </div>

  </teleport>

</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

// Импортируем изображения орлов (замените на ваши пути)
import eagle1 from '../../../../assets/Eagles/TreeEagle.png'
import eagle2 from '../../../../assets/Eagles/StoneEagle.png'
import eagle3 from '../../../../assets/Eagles/СopperEagle.png'
import eagle4 from '../../../../assets/Eagles/SiliverEagle.png'
import eagle5 from '../../../../assets/Eagles/GoldEagle.png'
import eagle6 from '../../../../assets/Eagles/TitanEagle.png'
import eagle7 from '../../../../assets/Eagles/LazurEagle.png'
import eagle8 from '../../../../assets/Eagles/GranatEagle.png'
import eagle9 from '../../../../assets/Eagles/BriliantEagle.png'

// ... добавьте остальные изображения

import { useBonusStore } from '../stores/storeBonus'

const store = useBonusStore()
const bonusText = computed(() => store.bonusText(currentDay.value))

const LastLogin = ref(new Date());
LastLogin.value = new Date('2025-9-30T18:00:00');


const IsLogined = ref(false)


import BonusCard from './BonusCard.vue'

const totalDays = ref(3650)
const currentDay = ref(5)
const showReward = ref(false)
const isClosing = ref(false)

const showBonusCard = ref(false)
const isClosingBonusCard = ref(false)

// Система орлов
const eagleImages = [
    eagle1, eagle2, eagle3, eagle4, eagle5, eagle6, eagle7, eagle8, eagle9,
    // ... добавьте остальные изображения
]


const showEagleTransition = ref(false)
const isTransitioning = ref(false)
const oldEagleImage = ref('')
const transitionNewImage = ref('')
const currentEagleLevel = ref(1)
const isNewEagle = ref(false)

// Drag & Drop переменные
const isDragging = ref(false)
const startX = ref(0)
const scrollPosition = ref(0)
const treeContainer = ref(null)
const showScrollIndicator = ref(true)

// Позиционирование/измерения
const cellWidth = ref(165.33)
const baseEagleLeftOffset = ref(20) // смещение для выравнивания орла по центру точки

// Стиль для летающего орла
const isJumping = ref(false)
const currentEagleImage = ref('')


const bonusVisible = ref(false)
const bonusLevel = ref(0)
const popupX = ref(0)
const popupY = ref(0)

const showBonus = (level, event) => {
  if (level % 10 !== 0) return
  bonusLevel.value = level
  bonusVisible.value = true
  const rect = event.currentTarget.getBoundingClientRect()
  popupX.value = rect.left + rect.width / 2
  popupY.value = rect.bottom + 12
}

const hideBonus = () => {
  bonusVisible.value = false
}

const wasLoggedInToday = () => {
  const now = new Date();
  return LastLogin.value.getFullYear() === now.getFullYear() &&
        LastLogin.value.getMonth() === now.getMonth() &&
        LastLogin.value.getDate() === now.getDate();
};

    
  


// Получаем орла для конкретного уровня
const getEagleForLevel = (dayNumber) => {
    const level = Math.floor(dayNumber / 10) + 1
    return eagleImages[Math.min(level - 1, eagleImages.length - 1)] || eagleImages[0]
}

const progressionDays = computed(() => {
    return Array.from({ length: currentDay.value + 100 }, (_, index) => ({
        day: index + 1,
        isCompleted: index < currentDay.value
    }))
})


// ---- Вспомогательные функции для измерений и центрирования ----
const computeLayout = () => {
    if (!treeContainer.value) return
    const items = treeContainer.value.querySelectorAll('.day-item')
    if (!items || items.length === 0) return

    if (items.length >= 2) {
        const r1 = items[0].getBoundingClientRect()
        const r2 = items[1].getBoundingClientRect()
        const measured = Math.abs(r2.left - r1.left)
        if (measured > 10) cellWidth.value = measured
    }

    // вычислим смещение орла так, чтобы он был по центру .inner-dot
    const firstInner = items[0].querySelector('.inner-dot')
    const treeRect = treeContainer.value.getBoundingClientRect()
    const eagleImgWidth = 80 // соответствует .eagle-flying

    if (firstInner) {
        const innerRect = firstInner.getBoundingClientRect()
        baseEagleLeftOffset.value = (innerRect.left - treeRect.left) + innerRect.width / 2 - eagleImgWidth / 2
    }
}

const calculateMaxScroll = () => {
    if (!treeContainer.value) return 0
    const containerWidth = treeContainer.value.parentElement.clientWidth
    const treeWidth = treeContainer.value.scrollWidth
    return Math.max(0, treeWidth - containerWidth) + 100
}

const centerOnDay = (dayNumber) => {
  if (!treeContainer.value) return;

  const container = treeContainer.value.parentElement;
  const containerWidth = container.clientWidth || window.innerWidth;
  const maxScroll = calculateMaxScroll();

  const targetIndex = Math.max(0, dayNumber - 1);

  // Получаем позицию элемента относительно контейнера
  const items = treeContainer.value.querySelectorAll('.day-item');
  if (items.length === 0 || targetIndex >= items.length) return;

  const targetElement = items[targetIndex];
  const targetRect = targetElement.getBoundingClientRect();
  const containerRect = container.getBoundingClientRect();

  // Центрируем по середине выбранного дня
  const targetCenter = (targetRect.left - containerRect.left) + (targetRect.width / 2);

  // Смещение устанавливаем так, чтобы центр дня совпал с центром контейнера
  let newScroll = scrollPosition.value + containerWidth / 2 - targetCenter;

  // Ограничиваем прокрутку в заданных рамках (мин и макс)
  newScroll = Math.min(0, Math.max(-maxScroll, newScroll));

  scrollPosition.value = newScroll;
};



const centerTree = () => {
    centerOnDay(currentDay.value)
}

// ---- Основная логика прогресса ----
const completeDay = async () => {
    if (currentDay.value >= totalDays.value || IsLogined.value) return

    

    currentDay.value++
    await nextTick()
    computeLayout()
    IsLogined.value = true
    isJumping.value = false


    await new Promise(resolve => setTimeout(resolve, 500)) // столько же, сколько в CSS
    isJumping.value = false

    if (currentDay.value % 10 === 0) {
        await showEagleTransitionAnimation()
    } else {
        showReward.value = true
    }
}

// Анимация смены орла
const showEagleTransitionAnimation = async () => {
    const newLevel = Math.floor(currentDay.value / 10)
    oldEagleImage.value = eagleImages[Math.max(0, newLevel - 1)] || eagleImages[0]
    transitionNewImage.value = eagleImages[Math.min(newLevel, eagleImages.length - 1)] || eagleImages[eagleImages.length - 1]

    // не обновляем текущую картинку на странице пока идёт анимация (watch ниже это учитывает)
    showEagleTransition.value = true
    await new Promise(resolve => setTimeout(resolve, 80))
    isTransitioning.value = true

    await new Promise(resolve => setTimeout(resolve, 1400))

    isTransitioning.value = false
    showEagleTransition.value = false

    // Обновим глобальную картинку и пометку о новом орле для glow в модалке
    currentEagleImage.value = transitionNewImage.value
    isNewEagle.value = true
    showReward.value = true
}

const closeReward = async () => {
    if (isClosing.value) return
    
    isClosing.value = true
    await new Promise(resolve => setTimeout(resolve, 300))
    showReward.value = false
    isClosing.value = false
    isNewEagle.value = false
    if (currentDay.value % 10 == 0) {
        showBonusCard.value = true
    }
}

const closeRewardBonus = async () => {
    if (isClosingBonusCard.value) return
    isClosingBonusCard.value = true
    await new Promise(resolve => setTimeout(resolve, 300))
    showBonusCard.value = false
    isClosingBonusCard.value = false
}

// Прыжок к определенному орлу
const jumpToEagle = (dayNumber) => {
    if (dayNumber <= currentDay.value) {
        centerOnDay(dayNumber)
    }
}

// Функции для drag & drop
const startDrag = (event) => {
    isDragging.value = true
    startX.value = event.clientX - scrollPosition.value
    document.body.style.userSelect = 'none'
    showScrollIndicator.value = false
    // слушаем global mouseup на случай, если пользователь отпустит за пределами элемента
    document.addEventListener('mouseup', stopDrag)
}

const onDrag = (event) => {
    if (!isDragging.value) return
    const x = event.clientX - startX.value
    const maxScroll = calculateMaxScroll()
    scrollPosition.value = Math.max(Math.min(x, 0), -maxScroll)
}

const stopDrag = () => {
    isDragging.value = false
    document.body.style.userSelect = ''
    document.removeEventListener('mouseup', stopDrag)
}

const onWheel = (event) => {
    event.preventDefault()
    const maxScroll = calculateMaxScroll()
    scrollPosition.value = Math.max(Math.min(scrollPosition.value + event.deltaY, 0), -maxScroll)
}

// ---- Жизненный цикл и наблюдатели ----
const loggedInToday = ref(false);


onMounted(() => {
  loggedInToday.value = wasLoggedInToday();
  currentDay.value--
});

onMounted(async () => {
    await nextTick()
    computeLayout()
    setTimeout(() => {
        showScrollIndicator.value = false
    }, 5000)

    const container = treeContainer.value
    if (container) {
        container.addEventListener('wheel', onWheel, { passive: false })
    }

    window.addEventListener('resize', computeLayout)
})

onUnmounted(() => {
    const container = treeContainer.value
    if (container) {
        container.removeEventListener('wheel', onWheel)
    }
    window.removeEventListener('resize', computeLayout)
    document.removeEventListener('mouseup', stopDrag)
})

// Следим за изменением currentDay: обновляем картинку орла только если нет перехода (чтобы переход отображался корректно)
watch(currentDay, async (newDay) => {
    if (!showEagleTransition.value) {
        currentEagleImage.value = getEagleForLevel(newDay)
    }
    currentEagleLevel.value = Math.floor(newDay / 10) + 1
    await nextTick()
    computeLayout()
}, { immediate: true })

const eagleLeft = ref(0)

watch(currentDay, async (newDay) => {
    await nextTick()
    eagleLeft.value = getEagleLeftForDay(newDay - 1)
}, { immediate: true })


watch(scrollPosition, () => {
  bonusVisible.value = false
})

const getEagleLeftForDay = (dayIndex) => {
    if (!treeContainer.value) return 0
    const items = treeContainer.value.querySelectorAll('.day-item')
    if (items.length <= dayIndex) return 0

    const inner = items[dayIndex].querySelector('.inner-dot')
    const treeRect = treeContainer.value.getBoundingClientRect()
    const eagleWidth = 80

    if (inner) {
        const innerRect = inner.getBoundingClientRect()
        return (innerRect.left - treeRect.left) + innerRect.width / 2 - eagleWidth / 2
    }
    return 0
}


</script>

<style scoped>
/* Стили для орлов на точках */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

* {
    font-family: 'Poppins', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.bonus-popup {
   
  position: absolute; /* фиксируем относительно окна */
  transform: translateX(-50%);
  z-index: 1500;
  animation: fadeInUp 0.25s ease;
  pointer-events: none;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translate(-50%, 10px); }
  to { opacity: 1; transform: translate(-50%, 0); }
}




.eagle-perch-spot {
    position: absolute;
    top: -40px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
}

.eagle-on-perch {
    width: 44px;
    height: 44px;
    object-fit: contain;
    cursor: pointer;
    transition: all 0.35s ease;
    filter: grayscale(0.75);
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
    border-radius: 50%;
    background: #eef6ff;
}

.eagle-on-perch.completed {
    filter: grayscale(0);
    transform: scale(1.18);
    box-shadow: 0 6px 18px rgba(26, 115, 232, 0.45);
}

.eagle-on-perch:hover {
    transform: scale(1.3);
    box-shadow: 0 8px 22px rgba(26, 115, 232, 0.6);
}

/* Летающий орел */
.flying-eagle {
    position: absolute;
    top: -38px;
    z-index: 35;
    pointer-events: none;
    transition: left 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.flying-eagle.jumping {
    transition: left 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}


.eagle-flying {
    width: 81px;
    height: 98px;
    object-fit: contain;
    filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.28));
}

/* Анимация смены орла */
.eagle-transition {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
}

.transition-container {
    position: relative;
    width: 200px;
    height: 200px;
}

.eagle-old, .eagle-new {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: all 1s ease;
}

.eagle-old.fading {
    opacity: 0;
    transform: scale(0.5);
}

.eagle-new {
    opacity: 0;
    transform: scale(0.5);
}

.eagle-new.appearing {
    opacity: 1;
    transform: scale(1.2);
}

/* Стили для модального окна */
.eagle-level {
    color: #ff9800;
    font-weight: 700;
    font-size: 1.3em;
    letter-spacing: 0.03em;
}

.reward-image.new-eagle {
    animation: eagleGlow 2.5s ease-in-out infinite alternate;
}


@keyframes eagleGlow {
    0%, 100% { transform: scale(1); filter: brightness(1); }
    50% { transform: scale(1.12); filter: brightness(1.3); }
}

/* Остальные стили остаются без изменений */
.reward-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease-out;
}

.reward-modal.closing {
    animation: fadeOut 0.3s ease-in forwards;
}

.reward-content {
    background: white;
    padding: 36px 40px;
    border-radius: 20px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
    animation: scaleIn 0.35s ease-out;
    max-width: 420px;
    width: 420px;
}

.reward-layout {
    display: flex;
    align-items: center;
    gap: 28px;
}

.image-container .reward-image {
    width: 120px;
    height: 120px;
    object-fit: contain;
    border-radius: 18px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.text-container {
    flex: 1;
    text-align: center; /* Текст слева */
}

.text-container h3 {
    font-weight: 600;
    font-size: 26px;
    color: #1a237e;
    margin-bottom: 16px;
    letter-spacing: 0.02em;
}

.text-container p {
    font-size: 17px;
    font-weight: 500;
    color: #424242;
    margin-bottom: 12px;
}

.points {
    color: #3a993e;
    font-weight: bold;
    font-size: 20px;
}

.thanks-btn {
    background: #1a73e8;
    color: white;
    border: none;
    padding: 14px 38px;
    border-radius: 30px;
    font-size: 17px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 6px 18px rgba(26, 115, 232, 0.38);
    user-select: none;
}

.thanks-btn:hover:not(:disabled) {
    background: #135ab9;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(19, 90, 185, 0.5);
}

.thanks-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes fadeOut {
    from {
        opacity: 1;
    }
    to {
        opacity: 0;
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes scaleOut {
    from {
        opacity: 1;
        transform: scale(1);
    }
    to {
        opacity: 0;
        transform: scale(0.8);
    }
}


/* Дерево */
.progression-tree {
    padding: 40px 20px;
    font-family: 'Arial', sans-serif;
    overflow: hidden;
    position: relative; /* ✅ нужно, чтобы орёл летал внутри дерева */
    cursor: grab;
}

.progression-tree:active {
    cursor: grabbing;
}

.tree-container {
    display: flex;
    align-items: center;
    justify-content: flex-start; /* Выравниваем по левому краю */
    position: relative;
    min-height: 120px;
    transition: transform 0.25s ease; /* Плавная прокрутка */
    width: max-content; /* Ширина по содержимому */
}

.tree-container.no-transition {
    transition: none !important;
}

.day-item {
    display: flex;
    align-items: center;
    position: relative;
    z-index: 2;
    flex-shrink: 0;
}

.day-number {
    margin-top: 10px;
    font-size: 13px;
    font-weight: 600;
    color: #3f51b5;
    user-select: none;
}

/* Остальные стили ... оставлены без изменений */
.level-dot {
    
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.inner-dot {
    width: 54px;
    height: 54px;
    background: #f0f4ff;
    border: 3.5px solid #9fb8ff;
    border-radius: 50%;
    box-shadow: 0 4px 12px rgba(26, 115, 232, 0.24);
    font-weight: 700;
    font-size: 16px;
    color: #1a237e;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    user-select: none;
    cursor: default;
}

.day-item.completed .inner-dot {
    background: #1a73e8;
    border-color: #0d47a1;
    color: #f0f4ff;
    box-shadow: 0 6px 18px rgba(19, 64, 228, 0.65);
}

.day-item.future .inner-dot {
    background: #f5f7ff;
    border-color: #c0ccff;
    color: #9ea7cc;
    box-shadow: none;
}

.day-item.completed .day-number {
    color: #0015ff;
    font-weight: bold;
}
/* Стили для соединительных линий - ПОДНИМАЕМ ВЫШЕ */
.connection-line {
    position: relative;
    width: 88px;
    height: 22px;
    background: #d6d6d6;
    margin: 0 22px;
    margin-bottom: -12px;
    border-radius: 25px;
    overflow: hidden;
    flex-shrink: 0;
    top: -14px;
    margin-top: -14px;
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
}

.line-fill {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #1a73e8, #42a5f5);
    transition: width 0.5s ease;
}

.connection-line.completed .line-fill {
    width: 100%;
}

/* Индикатор прокрутки */
.scroll-indicator {
    text-align: center;
    color: #5c6bc0;
    font-size: 13px;
    margin-top: 12px;
    font-weight: 600;
    animation: fadeBlink 2s infinite;
    position: absolute;
    bottom: 14px;
    left: 0;
    right: 0;
}

@keyframes fadeBlink {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

.controls {
    margin-top: 44px;
    text-align: center;
}

.controls button {
    padding: 12px 28px;
    margin: 0 14px;
    border: none;
    border-radius: 8px;
    background: #1a73e8;
    color: white;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 6px 14px rgba(26, 115, 232, 0.36);
    transition: background 0.3s ease, transform 0.2s ease;
}

.controls button:hover:not(:disabled) {
    background: #134a9b;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(19, 74, 155, 0.48);
}

.controls button:disabled {
    background: #cfd8dc;
    cursor: not-allowed;
    box-shadow: none;
}


</style>
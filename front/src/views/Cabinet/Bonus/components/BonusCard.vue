<template>
  <div class="bonus-card">
    <h4>Бонус за уровень {{ level }}</h4>
    <p>{{ bonusText }}</p>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue'

import { useBonusStore } from '../stores/storeBonus'



const props = defineProps({
  level: {
    type: Number,
    required: true
  }
})

const store = useBonusStore()
const bonusText = computed(() => store.bonusText(props.level))

</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');


* {
    font-family: 'Poppins', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Карточка бонуса */
.bonus-card {
    min-width: 200px;
    max-width: 260px;
    padding: 20px 24px;
    background: linear-gradient(135deg, #f0f9ff 0%, #d9f0ff 100%);
    border-radius: 16px;
    border: 2px solid #1a73e8;
    box-shadow: 0 8px 20px rgba(26, 115, 232, 0.35);
    font-size: 15px;
    text-align: center;
    pointer-events: none;
    transition: transform 0.2s ease;
}

.bonus-card h4 {
    font-size: 18px;
    margin-bottom: 8px;
    color: #1a73e8;
    font-weight: 600;
}

.bonus-card p {
    font-weight: 600;
    color: #176f3d;
    margin: 0;
}


</style>

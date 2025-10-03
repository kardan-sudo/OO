<script setup>
import imgLoad from '../assets/Untitled.svg'
</script>

<template>
  <div>
     <div  class="load">
        <img :src="imgLoad" alt="">
      </div>
  
    </div>
</template>

<style scoped>

.load {
  position: fixed;
  top: 50%;
  left: 50%;
   transform: translate(-50%, -50%) scale(0.5); /* 1 - 0.3 = 0.7 → на 30% меньше */
  z-index: 1000000;
  margin: 0;
  transform-origin: center; /* чтобы масштабирование было от центра */
}

</style>
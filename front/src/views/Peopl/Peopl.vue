<script setup>
import { computed, onMounted } from 'vue';
import HeadPlace from './HeadPlace.vue';
import PlaceOne from './placeOne.vue';
import { usePlaceStore } from '@/stores/storePlace';
import { storeToRefs } from 'pinia';
import imgload from '../../assets/Untitled.svg'
import MyLoad from '@/Load/MyLoad.vue';
 const {getPlace}= usePlaceStore()
 const {getloading} = storeToRefs(usePlaceStore())
 const pl = usePlaceStore()
 const load = computed(()=>getloading.value)
 onMounted(()=>{
  pl.fetchEvents()
 })
</script>

<template>
  <div>
    <div v-if="load" class="load">
     <MyLoad/>
    </div>
    <div v-else class="div" >
      <HeadPlace/>
      <div class="place"> 
          <PlaceOne   v-for="value in getPlace" :key="value.id" :place="value" />
      </div>
    </div>
  </div>
    
</template>

<style scoped>
.div{
  margin-top: 100px;
}
.load {
  position: fixed;
  top: 50%;
  left: 50%;
   transform: translate(-50%, -50%) scale(0.5); /* 1 - 0.3 = 0.7 → на 30% меньше */
  z-index: 1000000;
  margin: 0;
  transform-origin: center; /* чтобы масштабирование было от центра */
}
.place {
  display: grid;
  margin-top: 14rem;
  grid-template-columns: repeat(3, 1fr); /* Две колонки */
  gap: 1rem;
}


</style>

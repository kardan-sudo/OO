import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDNKStore = defineStore('applications', () => {


  const DNKdata = ref([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1])

  return {
    DNKdata
  }
})
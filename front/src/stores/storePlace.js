import { apiClient } from '@/main'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const usePlaceStore = defineStore('place', () => {
  const loading = ref(false)
  const place = ref([ ])
  const getPlace = computed(() => {
    return place.value
  })
const fetchEvents = async () => {
  loading.value = true;

  try {
    // Выполняем запрос и ждём минимум 1500 мс
    const [response] = await Promise.all([
      apiClient.get('/scenic-spots'),
      new Promise(resolve => setTimeout(resolve, 1500)) // ← таймаут 1.5 сек
    ]);

    place.value = response.data.items || response.data; // защита на случай, если нет .items
    console.log(place.value);
  } catch (err) {
    console.error('Ошибка при загрузке достопримечательностей:', err);
  } finally {
    loading.value = false;
  }
};
  const getloading = computed(() =>  loading.value)
  return {
    getloading,
    fetchEvents,
    getPlace
  }
})
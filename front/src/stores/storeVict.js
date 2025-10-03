import { apiClient } from '@/main'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useVictStore = defineStore('victorin', () => {
  const loading = ref(false)
  const quiz = ref([]
  )
const fetchEvents = async () => {
  loading.value = true;

  try {
    // Выполняем запрос и ждём минимум 1500 мс
    const [response] = await Promise.all([
      apiClient.get('/quizzes'),
      new Promise(resolve => setTimeout(resolve, 1500)) // ← задержка 1.5 секунды
    ]);

    quiz.value = response.data.items || response.data; // защита на случай, если данные — массив напрямую
    console.log(quiz.value, 'quz');
  } catch (err) {
    console.error('Ошибка при загрузке квизов:', err);
  } finally {
    loading.value = false;
  }
};
  const getVict = computed(() => {
    return quiz.value
  })
    const getloading = computed(() => {
    return loading.value
  })

  return {
    getloading,
    fetchEvents,
    getVict
  }
})
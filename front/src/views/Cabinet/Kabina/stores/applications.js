import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useApplicationsStore = defineStore('applications', () => {
  const applications = ref([
    // Тестовые данные для демонстрации
    {
      id: 1,
      eventName: 'Концерт классической музыки',
      eventType: 'Концерты',
      startDate: '2024-03-15',
      endDate: '2024-03-15',
      address: 'Москва, ул. Тверская, д. 1',
      coordinateX: 55.7558,
      coordinateY: 37.6173,
      organizer: 'Московская филармония',
      description: 'Вечер классической музыки с участием известных исполнителей',
      website: 'https://meloman.ru',
      phone: '+7 (495) 123-45-67',
      status: 'pending',
      createdAt: '2024-01-15'
    },
    {
      id: 2,
      eventName: 'Выставка современного искусства',
      eventType: 'Выставки',
      startDate: '2024-03-20',
      endDate: '2024-04-20',
      address: 'Санкт-Петербург, Невский проспект, д. 20',
      coordinateX: 59.9343,
      coordinateY: 30.3351,
      organizer: 'Государственный Эрмитаж',
      description: 'Экспозиция работ современных художников',
      website: 'https://hermitage.ru',
      phone: '+7 (812) 987-65-43',
      status: 'pending',
      createdAt: '2024-01-16'
    }
  ])

  const createApplication = (applicationData) => {
    const newApplication = {
      id: Date.now(),
      ...applicationData,
      status: 'pending',
      createdAt: new Date().toISOString().split('T')[0]
    }
    applications.value.push(newApplication)
  }

  return {
    applications,
    createApplication
  }
})
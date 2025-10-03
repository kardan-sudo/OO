import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useBonusStore = defineStore('bonusStore', () => {
  const bonusList = [
    'Скидка в театр 50%',
    'Бесплатный кофе',
    'Пропуск на концерт',
    'Подарок-сюрприз',
    'Экскурсия в музей',
    'Подарочная карта'
  ]

  // Функция для получения массива бонусов (просто возвращаем массив)
  function getStrings() {
    return bonusList
  }

  function bonusText(level) {
    // Выбираем бонус исходя из уровня (каждые 10 уровней другой бонус)
    const idx = Math.floor(level / 10) % bonusList.length
    console.log(level)
    return bonusList[idx] || 'Сюрприз!'
  }

  // Если нужно добавить бонус в список — bonusList должен быть ref или reactive.
  // Сейчас bonusList — обычный массив, если хотите менять — меняйте структуру.

  return { bonusText, bonusList, getStrings }
})

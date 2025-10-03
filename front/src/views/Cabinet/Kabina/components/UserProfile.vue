<template>
  <div class="user-cabinet">
    <div class="cabinet-header">
      <h1>Личный кабинет пользователя</h1>
      <div class="user-status" :class="statusClass">
        {{ statusText }}
      </div>
    </div>

    <div class="FIO_DNK">
        <div class="user-info">
          <p><strong>ФИО:</strong> {{ user.fullName }}</p>
          <p><strong>Год рождения:</strong> {{ user.birthYear }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Статус:</strong> {{ statusText }}</p>
          <p><strong>Роль:</strong> {{ user.role === 'admin' ? 'Администратор' : 'Пользователь' }}</p>
        </div>

        <div class="DNK">
            <DNK/>
        </div>    
    </div>
    

    <div class="actions">
      <button @click="editProfile" class="btn btn-primary">
        Редактировать профиль
      </button>
      
      <button 
        v-if="!isOfficial" 
        @click="upgradeToOfficial" 
        class="btn btn-success"
      >
        Стать официальным представителем
      </button>

      <button @click="handleSwitchRole" class="btn btn-warning">
        Переключить роль (сейчас: {{ user.role }})
      </button>

      <router-link to="/admin" class="btn btn-info">
        Перейти в админку
      </router-link>
    </div>

    <!-- Модальное окно редактирования -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal">
        <h3>Редактирование профиля</h3>
        <form @submit.prevent="handleSaveProfile">
          <div class="form-group">
            <label>ФИО:</label>
            <input v-model="editForm.fullName" type="text" class="form-input" required>
          </div>
          <div class="form-group">
            <label>Год рождения:</label>
            <input v-model="editForm.birthYear" type="number" min="1900" max="2024" class="form-input" required>
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input v-model="editForm.email" type="email" class="form-input" required>
          </div>
          <div class="form-group">
            <label>Новый пароль:</label>
            <input v-model="editForm.password" type="password" class="form-input" placeholder="Оставьте пустым, если не меняется">
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-success">Сохранить</button>
            <button type="button" @click="closeModal" class="btn btn-secondary">Отмена</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Компоненты -->
    <div class="components-grid">
      <Achievements />
      <DailyBonus />
      <ApplicationForm v-if="isOfficial" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import Achievements from './Achievements.vue'
import DailyBonus from './DailyBonus.vue'
import ApplicationForm from './ApplicationForm.vue'
import DNK from './DNK.vue'

const authStore = useAuthStore()
const { user, isOfficial, updateProfile, updatePassword, upgradeToOfficial, switchRole } = authStore

const showEditModal = ref(false)
const editForm = ref({
  fullName: '',
  birthYear: '',
  email: '',
  password: ''
})

const statusText = computed(() => {
  return isOfficial ? 'Официальный представитель' : 'Обычный пользователь'
})

const statusClass = computed(() => {
  return isOfficial ? 'status-official' : 'status-ordinary'
})

// Функция открытия модального окна редактирования
const editProfile = () => {
  editForm.value = {
    fullName: user.value.fullName,
    birthYear: user.value.birthYear,
    email: user.value.email,
    password: ''
  }
  showEditModal.value = true
 
}

// Функция сохранения профиля
const handleSaveProfile = () => {
  try {
    // Создаем копию данных без пароля для обновления профиля
    const { password, ...profileData } = editForm.value
    
    // Обновляем профиль
    updateProfile(profileData)
    
    // Если указан пароль, обновляем его
    if (password && password.trim() !== '') {
      updatePassword(password)
    }
    
    closeModal()
    alert('Профиль успешно обновлен!')
    
  } catch (error) {
    console.error('Ошибка при обновлении профиля:', error)
    alert('Произошла ошибка при обновлении профиля')
  }
}

// Функция закрытия модального окна
const closeModal = () => {
  showEditModal.value = false
  // Сбрасываем форму
  editForm.value = {
    fullName: '',
    birthYear: '',
    email: '',
    password: ''
  }
}

// Функция переключения роли
const handleSwitchRole = () => {
  switchRole()
  alert(`Роль изменена на: ${user.value.role === 'admin' ? 'Администратор' : 'Пользователь'}`)
}

// Функция становления официальным представителем
const handleUpgradeToOfficial = () => {
  upgradeToOfficial()
  alert('Теперь вы официальный представитель!')
}

// Отслеживаем изменения пользователя для отладки
watch(() => user.value, (newUser) => {
  console.log('Данные пользователя обновлены:', newUser)
}, { deep: true })
</script>

<style scoped>
.FIO_DNK {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 30px;
    margin-bottom: 30px;
    min-height: 400px;
}

.user-info {
    flex: 0 0 600px;
    background: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 4px solid #007bff;
    display: flex;
    flex-direction: column;
}

.user-info p {
    margin: 12px 0;
    padding: 8px 0;
    border-bottom: 1px solid #f8f9fa;
    display: flex;
    justify-content: space-between;
}

.user-info p:last-child {
    border-bottom: none;
}

.DNK {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    height: 100%;
}

.cabinet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.user-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
}

.status-official {
  background: #d4edda;
  color: #155724;
}

.status-ordinary {
  background: #e2e3e5;
  color: #383d41;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  font-size: 14px;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

@media (max-width: 768px) {
  .cabinet-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .components-grid {
    grid-template-columns: 1fr;
  }
}
</style>
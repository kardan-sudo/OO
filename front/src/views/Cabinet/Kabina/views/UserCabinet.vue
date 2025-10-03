<template>
  <div class="user-cabinet">
    <!-- Заголовок с градиентом -->
    <div class="cabinet-header">
      <div class="header-content">
        <h1 class="cabinet-title">Личный кабинет</h1>
        <div class="user-status" :class="statusClass">
          <span class="status-icon">{{ getUser.is_representative ? '⭐' : '👤' }}</span>
          {{ statusText }}
        </div>
      </div>
      <div class="header-decoration">
        <div class="decoration-circle circle-1"></div>
        <div class="decoration-circle circle-2"></div>
        <div class="decoration-circle circle-3"></div>
      </div>
    </div>

    <!-- Основная информация пользователя и DNA -->
    <div  data-aos = "fade-right" class="FIO_DNK">
      <div class="user-info-card">
        <div class="card-header">
          <h3 class="card-title">👤 Персональные данные</h3>
          <div class="card-badge">ID: {{ getUser.id || '001' }}</div>
        </div>
        <div class="user-details">
          <div class="detail-item">
            <div class="detail-icon">📝</div>
            <div class="detail-content">
              <span class="detail-label">ФИО:</span>
              <span class="detail-value">{{ getUser.full_name }}</span>
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-icon">🎂</div>
            <div class="detail-content">
              <span class="detail-label">Год рождения:</span>
              <span class="detail-value">{{ getUser.date_of_birth }}</span>
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-icon">📧</div>
            <div class="detail-content">
              <span class="detail-label">Email:</span>
              <span class="detail-value">{{ getUser.email }}</span>
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-icon">🎯</div>
            <div class="detail-content">
              <span class="detail-label">Статус:</span>
              <span class="detail-value" :class="statusClass">{{ statusText }}</span>
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-icon">👑</div>
            <div class="detail-content">
              <span class="detail-label">Роль:</span>
              <span class="detail-value role-badge" :class="getUser.is_organizer === 'admin' ? 'role-admin' : 'role-user'">
                {{ getUser.is_organizer === 'admin' ? 'Администратор' : 'Пользователь' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div  data-aos = "fade-right" class="DNK-card">
        <div class="genetic-code-title">
            <h2>Культурный код</h2>
        </div>
        <div class="dna-wrapper">
          <div class="dna-animation-container">
            <DNK/>
          </div>
        </div>
      </div>
    </div>

    <!-- Действия -->
    <div  data-aos = "fade-right" class="actions-section">
      <h3 class="section-title">⚡ Быстрые действия</h3>
      <div class="actions-grid">
        <button @click="editProfile" class="action-btn primary">
          <span class="btn-icon">✏️</span>
          <span class="btn-text">Редактировать профиль</span>
        </button>

        <!-- Кнопка для открытия формы заявки -->
        <button 
          v-if="getUser.is_representative" 
          @click="showApplicationFormModal = true" 
          class="action-btn primary"
        >
          <span class="btn-icon">📋</span>
          <span class="btn-text">Создать заявку</span>
        </button>

        <router-link to="/admin" class="action-btn info" v-if="getUser.is_organizer === 'admin'">
          <span class="btn-icon">⚙️</span>
          <span class="btn-text">Панель администратора</span>
        </router-link>

        <button class="action-btn success"  @click="goParser">
          <span class="btn-icon">💳</span>
          <span class="btn-text">Орлиный глаз</span>
        </button>

        <button class="action-btn uslugi">
          <span class="btn-icon">🎼</span>
          <span class="btn-text">Подключить госуслуги</span>
        </button>
        <button class="action-btn ">
          <span class="btn-icon">💳</span>
          <span class="btn-text"><RouterLink to="/fav" class="action-btn info">Избранные мероприятия</RouterLink> </span>
        </button>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div  data-aos = "fade-right" v-if="showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">✏️ Редактирование профиля</h3>
          <button @click="closeModal" class="modal-close">×</button>
        </div>
        <form @submit.prevent="saveProfile" class="modal-form">
          <div class="form-group">
            <label class="form-label">ФИО</label>
            <input v-model="editForm.full_name" type="text" class="form-input" required placeholder="Введите ваше ФИО">
          </div>
          <div class="form-group">
            <label class="form-label">Год рождения</label>
            <input v-model="editForm.date_of_birth
" type="number" min="1900" max="2024" class="form-input" required placeholder="Год рождения">
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input v-model="editForm.email" type="email" class="form-input" required placeholder="your@email.com">
          </div>
          <div class="form-group">
            <label class="form-label">Новый пароль</label>
            <input v-model="editForm.password" type="password" class="form-input" placeholder="Введите новый пароль">
            <div class="form-hint">Оставьте пустым, если не меняется</div>
          </div>
          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn btn-secondary">Отмена</button>
            <button type="submit" class="btn btn-success">
              <span class="btn-loading" v-if="loading">⏳</span>
              Сохранить изменения
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Модальное окно формы заявки -->
    <div  data-aos = "fade-right" v-if="showApplicationFormModal" class="modal-overlay" @click.self="showApplicationFormModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">📋 Создать заявку на мероприятие</h3>
          <button @click="showApplicationFormModal = false" class="modal-close">×</button>
        </div>
        <ApplicationForm @submitted="showApplicationFormModal = false" />
      </div>
    </div>

    <!-- Компоненты -->
    <div class="components-section">
      <h3 class="section-title">🎯 Активности и достижения</h3>
      <div class="components-grid">
        <Achievements  data-aos = "fade-right" />
        <DailyBonus  data-aos = "fade-right" />
        <!-- ApplicationForm больше не отображается здесь постоянно -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import { useUserStore } from '@/stores/useUserStore'
import Achievements from '../components/Achievements.vue'
import DailyBonus from '../components/DailyBonus.vue'
import ApplicationForm from '../components/ApplicationForm.vue'
import DNK from '../components/DNK.vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const authStore = useAuthStore()
const { getUser } = storeToRefs(useUserStore())
const { updateProfile, updatePassword } = authStore

const showEditModal = ref(false)
const showApplicationFormModal = ref(false)
const loading = ref(false)
const editForm = ref({
  full_name: '',
  date_of_birth: '',
  email: '',
  password: ''
})
const goParser=()=>{
  router.push('/admin')
}
const statusText = computed(() => {
  return getUser.is_representative ? 'Официальный представитель' : 'Обычный пользователь'
})

const statusClass = computed(() => {
  return getUser.is_representative ? 'status-official' : 'status-ordinary'
})

const editProfile = () => {
  editForm.value = {
    full_name: getUser.value.full_name,
    date_of_birth
: getUser.value.date_of_birth
,
    email: getUser.value.email,
    password: ''
  }
  showEditModal.value = true
}

const saveProfile = async () => {
  try {
    loading.value = true
    const { password, ...profileData } = editForm.value
    
    // Обновляем профиль
    updateProfile(profileData)
    
    // Если указан пароль, обновляем его
    if (password && password.trim() !== '') {
      updatePassword(password)
    }
    
    // Имитация загрузки для лучшего UX
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    closeModal()
    alert('✅ Профиль успешно обновлен!')
    
  } catch (error) {
    console.error('Ошибка при обновлении профиля:', error)
    alert('❌ Произошла ошибка при обновлении профиля')
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  showEditModal.value = false
  editForm.value = {
    full_name: '',
    date_of_birth
: '',
    email: '',
    password: ''
  }
}
</script>

<style scoped>


.genetic-code-title {
  text-align: center;
  margin-bottom: 35px;
  width: 100%;
}

.genetic-code-title h2 {
  font-size: 28px;
  font-weight: bold;
  color: #1e3a8a;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 
    0 0 10px rgba(74, 144, 226, 0.7),
    0 0 20px rgba(74, 144, 226, 0.5),
    0 0 30px rgba(74, 144, 226, 0.3);
  background: linear-gradient(135deg, #1e3a8a, #4a90e2, #87ceeb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleGlow 3s ease-in-out infinite alternate;
  padding: 10px 20px;
  border-radius: 10px;
  position: relative;
}



.user-cabinet {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;

  min-height: 100vh;
}

/* Заголовок */
.cabinet-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cabinet-title {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.user-status {
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 600;
  font-size: 14px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-official {
  background: rgba(34, 197, 94, 0.2);
  color: #dcfce7;
}

.status-ordinary {
  background: rgba(100, 116, 139, 0.2);
  color: #f1f5f9;
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circle-1 {
  width: 100px;
  height: 100px;
  top: -30px;
  right: 10%;
}

.circle-2 {
  width: 150px;
  height: 150px;
  bottom: -50px;
  left: 5%;
}

.circle-3 {
  width: 80px;
  height: 80px;
  bottom: 20px;
  right: 20%;
}

/* Основной контент */
.FIO_DNK {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}

.user-info-card,
.DNK-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  min-height: 500px; /* Увеличиваем минимальную высоту */
  display: flex;
  flex-direction: column;
}

.user-info-card:hover,
.DNK-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f1f5f9;
  flex-shrink: 0; /* Запрещаем сжатие заголовка */
}

.card-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.card-badge {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 600;
  background: #f1f5f9;
  color: #64748b;
}

.card-badge.science {
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  color: white;
}

/* Детали пользователя */
.user-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex: 1; /* Занимает всё доступное пространство */
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  border-radius: 12px;
  transition: background 0.3s ease;
}

.detail-item:hover {
  background: #f8fafc;
}

.detail-icon {
  font-size: 1.2rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 10px;
}

.detail-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  color: #64748b;
  font-weight: 500;
}

.detail-value {
  color: #1e293b;
  font-weight: 600;
}

.role-badge {
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 600;
}

.role-admin {
  background: #fef3c7;
  color: #d97706;
}

.role-user {
  background: #dbeafe;
  color: #1d4ed8;
}

/* DNA контейнер */
.dna-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 400px; /* Увеличиваем минимальную высоту */
}

.dna-title-container {
  text-align: center;
  margin-bottom: 20px;
  padding: 15px;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  flex-shrink: 0; /* Запрещаем сжатие заголовка */
}

.dna-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  background: linear-gradient(135deg, #1e3a8a, #4a90e2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dna-animation-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 350px; /* Гарантируем достаточно места для анимации */
  position: relative;
}

/* Секция действий */
.actions-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border: none;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.action-btn:hover::before {
  left: 100%;
}

.action-btn.primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.action-btn.success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.action-btn.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.action-btn.info {
  background: linear-gradient(135deg, #ff0000, #520202);
  color: white;
}

.action-btn.uslugi {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  color: white;
}

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.btn-icon {
  font-size: 1.2rem;
}

.btn-text {
  flex: 1;
  text-align: left;
}

.btn-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 8px;
  border-radius: 10px;
  font-size: 12px;
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal {
  background: white;
  border-radius: 20px;
  width: 450px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 25px 0;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #64748b;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #ef4444;
}

.modal-form {
  padding: 0 25px 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-hint {
  font-size: 12px;
  color: #6b7280;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 25px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-loading {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Секция компонентов */
.components-section {
  margin-top: 40px;
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
}

/* Адаптивность */


@media (max-width: 1081px) {
  .FIO_DNK {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .user-info-card,
  .DNK-card {
    min-height: auto;
    padding: 20px;
  }
  
  .dna-wrapper {
    min-height: 350px;
  }
  
  .components-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}

@media (max-width: 960px) {
  .user-cabinet {
    padding: 10px;
  }
  
  .cabinet-header {
    padding: 20px 15px;
    border-radius: 15px;
  }
  
  .cabinet-title {
    font-size: 1.8rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .user-status {
    padding: 10px 20px;
    font-size: 13px;
  }
  
  .FIO_DNK {
    gap: 15px;
    margin-bottom: 25px;
  }
  
  .user-info-card,
  .DNK-card {
    padding: 15px;
    border-radius: 15px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .card-title {
    font-size: 1.2rem;
  }
  
  .user-details {
    gap: 12px;
  }
  
  .detail-item {
    padding: 10px;
    gap: 12px;
  }
  
  .detail-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .detail-label,
  .detail-value {
    font-size: 14px;
  }
  
  .genetic-code-title h2 {
    font-size: 1.4rem;
    padding: 8px 16px;
  }
  
  .dna-wrapper {
    min-height: 300px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .action-btn {
    padding: 16px;
    font-size: 13px;
  }
  
  .section-title {
    font-size: 1.3rem;
    margin-bottom: 15px;
  }
  
  .components-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .modal {
    width: 95vw;
    margin: 10px;
  }
  
  .modal-header {
    padding: 20px 20px 0;
  }
  
  .modal-form {
    padding: 0 20px 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    margin-bottom: 10px;
  }
}

@media (max-width: 480px) {
  .cabinet-title {
    font-size: 1.5rem;
  }
  
  .user-status {
    width: 100%;
    justify-content: center;
  }
  
  .genetic-code-title h2 {
    font-size: 1.2rem;
    padding: 6px 12px;
  }
  
  .card-title {
    font-size: 1.1rem;
  }
  
  .detail-icon {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }
  
  .action-btn {
    padding: 14px;
    min-height: 50px;
  }
  
  .btn-icon {
    font-size: 1.1rem;
  }
  
  .modal-title {
    font-size: 1.1rem;
  }
  
  .form-input {
    padding: 10px 12px;
    font-size: 16px; /* Убирает zoom на iOS */
  }
}

@media (max-width: 360px) {
  .cabinet-title {
    font-size: 1.3rem;
  }
  
  .user-info-card,
  .DNK-card {
    padding: 12px;
  }
  
  .detail-item {
    padding: 8px;
  }
  
  .action-btn {
    padding: 12px;
    font-size: 12px;
  }
  
  .genetic-code-title h2 {
    font-size: 1.1rem;
  }
}

/* Улучшения для touch devices */
@media (hover: none) and (pointer: coarse) {
  .action-btn:hover {
    transform: none;
  }
  
  .user-info-card:hover,
  .DNK-card:hover {
    transform: none;
  }
}

/* Предотвращение горизонтального скролла */
.user-cabinet {
  overflow-x: hidden;
}

</style>
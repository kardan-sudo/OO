<template>
  <div class="admin-panel">
    <!-- Заголовок с градиентом -->
    <div class="admin-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="admin-title">Панель администратора</h1>
        </div>
        <div class="admin-badge" :class="isAdmin ? 'badge-admin' : 'badge-user'">
          <span class="badge-icon">{{ isAdmin ? '👑' : '👤' }}</span>
          {{ isAdmin ? 'Администратор' : 'Пользователь' }}
        </div>
      </div>
      <div class="header-decoration">
        <div class="decoration-circle circle-1"></div>
        <div class="decoration-circle circle-2"></div>
        <div class="decoration-circle circle-3"></div>
      </div>
    </div>

    <!-- Информационная панель -->
    <div class="admin-info-card">
      <div class="info-content">
        <div class="info-icon">🚀</div>
        <div class="info-text">
          <h3>Добро пожаловать в панель администратора!</h3>
          <p>Управляйте системой, просматривайте статистику и контролируйте процессы</p>
        </div>
      </div>
      <div v-if="!isAdmin" class="warning-alert">
        <div class="alert-icon">⚠️</div>
        <div class="alert-content">
          <strong>Внимание:</strong> у вас нет прав администратора. Это демонстрационный режим.
        </div>
      </div>
    </div>

    <!-- Быстрые действия -->
    <div class="actions-section">
      <h3 class="section-title">⚡ Быстрые действия</h3>
      <div class="actions-grid">
        <router-link to="/user" class="action-btn primary">
          <span class="btn-icon">👤</span>
          <span class="btn-text">Вернуться в личный кабинет</span>
        </router-link>
      </div>
    </div>

    <!-- Основной контент администратора -->
    <div v-if="isAdmin" class="admin-content">
      <div class="content-header">
        <h3 class="content-title">🎯 Управление системой</h3>
        <div class="content-stats">
          <div class="stat-item">
            <div class="stat-value">24</div>
            <div class="stat-label">Активных пользователя</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">156</div>
            <div class="stat-label">Всего заявок</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">12</div>
            <div class="stat-label">На модерации</div>
          </div>
        </div>
      </div>
      
      <AdminApplications />
    </div>
    
    <!-- Сообщение о запрете доступа -->
    <div v-else class="no-access-card">
      <div class="no-access-icon">🚫</div>
      <h3 class="no-access-title">Доступ запрещен</h3>
      <p class="no-access-text">
        Для доступа к функциям администратора необходимо иметь соответствующие права.
        Обратитесь к системному администратору для получения доступа.
      </p>
      <router-link to="/profile" class="btn btn-primary">
        Вернуться в профиль
      </router-link>
    </div>

    <!-- Дополнительные инструменты -->
   
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import AdminApplications from '../components/AdminApplications.vue'

const authStore = useAuthStore()
const { user, isAdmin} = authStore


</script>

<style scoped>
.admin-panel {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
}

/* Заголовок */
.admin-header {
  background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex: 1;
}

.admin-title {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.profile-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  width: fit-content;
}

.profile-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.admin-badge {
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

.badge-admin {
  background: rgba(34, 197, 94, 0.2);
  color: #dcfce7;
}

.badge-user {
  background: rgba(100, 116, 139, 0.2);
  color: #f1f5f9;
}

.badge-icon {
  font-size: 1.1rem;
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
  width: 120px;
  height: 120px;
  top: -40px;
  right: 10%;
}

.circle-2 {
  width: 180px;
  height: 180px;
  bottom: -60px;
  left: 5%;
}

.circle-3 {
  width: 90px;
  height: 90px;
  bottom: 30px;
  right: 20%;
}

/* Информационная карточка */
.admin-info-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.info-content {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 20px;
}

.info-icon {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 15px;
  padding: 15px;
}

.info-text h3 {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.info-text p {
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.warning-alert {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 20px;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid #fcd34d;
  border-radius: 15px;
}

.alert-icon {
  font-size: 1.5rem;
}

.alert-content {
  flex: 1;
  color: #92400e;
}

.alert-content strong {
  font-weight: 600;
}

/* Секция действий */
.actions-section {
  margin-bottom: 30px;
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

/* Основной контент */
.admin-content {
  background: white;
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f1f5f9;
}

.content-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.content-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #dc2626;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

/* Сообщение о запрете доступа */
.no-access-card {
  background: white;
  border-radius: 20px;
  padding: 50px 40px;
  text-align: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  margin-bottom: 30px;
}

.no-access-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.no-access-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #dc2626;
  margin-bottom: 15px;
}

.no-access-text {
  color: #64748b;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 30px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

/* Секция инструментов */
.tools-section {
  margin-top: 40px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
}

.tool-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.tool-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.tool-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 10px;
}

.tool-description {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 20px;
}

.tool-btn {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tool-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
}

/* Кнопки */
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Адаптивность */
@media (max-width: 1024px) {
  .content-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .content-stats {
    justify-content: center;
  }
  
  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .admin-panel {
    padding: 15px;
  }
  
  .admin-header {
    padding: 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .header-left {
    align-items: center;
  }
  
  .admin-title {
    font-size: 2rem;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .content-stats {
    flex-direction: column;
    gap: 15px;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
  }
  
  .info-content {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .admin-title {
    font-size: 1.7rem;
  }
  
  .admin-badge {
    padding: 10px 20px;
    font-size: 12px;
  }
  
  .profile-btn {
    padding: 8px 16px;
    font-size: 12px;
  }
  
  .no-access-card {
    padding: 30px 20px;
  }
  
  .no-access-title {
    font-size: 1.5rem;
  }
}

/* Добавляем к существующим стилям */

@media (max-width: 768px) {
  .admin-panel {
    padding: 10px;
  }
  
  .admin-header {
    padding: 20px 15px;
    border-radius: 15px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .header-left {
    align-items: center;
  }
  
  .admin-title {
    font-size: 1.8rem;
  }
  
  .admin-badge {
    padding: 10px 20px;
  }
  
  .profile-btn {
    padding: 8px 16px;
  }
  
  .admin-info-card {
    padding: 20px 15px;
  }
  
  .info-content {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .info-icon {
    align-self: center;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .action-btn {
    padding: 16px;
    min-height: 50px;
  }
  
  .content-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .content-stats {
    flex-direction: column;
    gap: 15px;
  }
  
  .stat-value {
    font-size: 1.8rem;
  }
  
  .no-access-card {
    padding: 30px 20px;
  }
  
  .no-access-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .admin-title {
    font-size: 1.5rem;
  }
  
  .action-btn {
    padding: 14px;
    font-size: 13px;
  }
  
  .info-text h3 {
    font-size: 1.2rem;
  }
  
  .profile-btn .btn-text {
    display: none;
  }
  
  .profile-btn {
    padding: 10px;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    justify-content: center;
  }
}
</style>
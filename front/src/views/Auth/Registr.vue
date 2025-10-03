<!-- components/RegisterForm.vue -->
<template>
  <div class="auth-card">
    <div class="auth-header">
      <h2>Регистрация</h2>
      <p>Создайте аккаунт для доступа ко всем функциям</p>
    </div>

    <form @submit.prevent="handleSubmit" class="auth-form">
      <div class="form-group">
        <label for="reg-username">Логин</label>
        <div class="input-wrapper">
          <i class="pi pi-user"></i>
          <input
            id="reg-username"
            v-model="formData.username"
            type="text"
            placeholder="Ваш логин"
            :class="{ error: errors.username }"
            @blur="validateField('username')"
          />
        </div>
        <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
      </div>

      <div class="form-group">
        <label for="reg-email">Email</label>
        <div class="input-wrapper">
          <i class="pi pi-envelope"></i>
          <input
            id="reg-email"
            v-model="formData.email"
            type="email"
            placeholder="example@mail.ru"
            :class="{ error: errors.email }"
            @blur="validateField('email')"
          />
        </div>
        <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
      </div>

      <div class="form-group">
        <label for="reg-password">Пароль</label>
        <div class="input-wrapper">
          <i class="pi pi-lock"></i>
          <input
            id="reg-password"
            v-model="formData.password"
            type="password"
            placeholder="••••••••"
            :class="{ error: errors.password }"
            @blur="validateField('password')"
          />
        </div>
        <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
      </div>

      <div class="form-group">
        <label for="full_name">ФИО</label>
        <div class="input-wrapper">
          <i class="pi pi-id-card"></i>
          <input
            id="full_name"
            v-model="formData.full_name"
            type="text"
            placeholder="Иванов Иван Иванович"
            :class="{ error: errors.full_name }"
            @blur="validateField('full_name')"
          />
        </div>
        <span v-if="errors.full_name" class="error-message">{{ errors.full_name }}</span>
      </div>

      <div class="form-group">
        <label for="date_of_birth">Дата рождения</label>
        <div class="input-wrapper">
          <i class="pi pi-calendar"></i>
          <input
            id="date_of_birth"
            v-model="formData.date_of_birth"
            type="date"
            :class="{ error: errors.date_of_birth }"
            @blur="validateField('date_of_birth')"
          />
        </div>
        <span v-if="errors.date_of_birth" class="error-message">{{ errors.date_of_birth }}</span>
      </div>

      <button type="submit" class="submit-btn">
        Зарегистрироваться
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const auth = useAuthStore()

const formData = ref({
  username: '',
  email: '',       // ← добавлено
  password: '',
  full_name: '',
  date_of_birth: ''
})

const errors = ref({})

const validateField = (field) => {
  const value = formData.value[field]
  switch (field) {
    case 'username':
      if (!value.trim()) errors.value.username = 'Логин обязателен'
      else if (value.length < 3) errors.value.username = 'Не менее 3 символов'
      else errors.value.username = ''
      break
    case 'email': // ← добавлена валидация email
      if (!value.trim()) {
        errors.value.email = 'Email обязателен'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        errors.value.email = 'Некорректный email'
      } else {
        errors.value.email = ''
      }
      break
    case 'password':
      if (!value) errors.value.password = 'Пароль обязателен'
      else if (value.length < 6) errors.value.password = 'Не менее 6 символов'
      else errors.value.password = ''
      break
    case 'full_name':
      if (!value.trim()) errors.value.full_name = 'Укажите ФИО'
      else if (!/^[а-яА-ЯёЁ\s]+$/.test(value)) errors.value.full_name = 'Только кириллица и пробелы'
      else errors.value.full_name = ''
      break
    case 'date_of_birth':
      if (!value) errors.value.date_of_birth = 'Укажите дату рождения'
      else {
        const date_of_birth = new Date(value)
        const today = new Date()
        const age = today.getFullYear() - date_of_birth.getFullYear()
        if (age < 12) errors.value.date_of_birth = 'Минимум 12 лет'
        else if (age > 100) errors.value.date_of_birth = 'Некорректная дата'
        else errors.value.date_of_birth = ''
      }
      break
  }
}

const handleSubmit = () => {
  Object.keys(formData.value).forEach(validateField)
  if (Object.values(errors.value).every(e => !e)) {
    console.log('Регистрация:', formData.value)
    auth.registr(formData.value)
  }
}
</script>

<style scoped>
/* Стили такие же, как в usernameForm.vue — можно вынести в общий файл, но для примера дублируем */
.auth-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
  animation: fadeIn 0.4s ease;
}

.auth-header h2 {
  margin: 0 0 0.5rem;
  color: var(--text-primary);
  font-size: 1.75rem;
  font-weight: 700;
}

.auth-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.95rem;
}

.input-wrapper {
  position: relative;
}

.input-wrapper i {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 1.1rem;
}

.input-wrapper input {
  width: 100%;
  padding: 0.875rem 0.875rem 0.875rem 2.75rem;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 1rem;
  color: var(--text-primary);
  background: var(--bg-primary);
  transition: all var(--transition-fast);
}

/* Для input[type="date"] — убираем стандартный стиль */
.input-wrapper input[type="date"] {
  padding-left: 2.75rem;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.input-wrapper input.error {
  border-color: #f5576c;
}

.error-message {
  display: block;
  color: #f5576c;
  font-size: 0.875rem;
  margin-top: 0.375rem;
  font-weight: 500;
}

.submit-btn {
  width: 100%;
  padding: 0.875rem;
  background: var(--primary-gradient);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-md);
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
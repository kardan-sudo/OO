<!-- components/LoginForm.vue -->
<template>
  <div  class="auth-card">
    <div class="auth-header">
      <h2>Вход в аккаунт</h2>
      <p>Введите свои данные для входа</p>
    </div>

    <form @submit.prevent="handleSubmit" class="auth-form">
      <div class="form-group">
        <label for="username">Логин</label>
        <div class="input-wrapper">
          <i class="pi pi-user"></i>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Ваш логин"
            :class="{ error: errors.username }"
            @blur="validateLogin"
          />
        </div>
        <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
      </div>

      <div class="form-group">
        <label for="password">Пароль</label>
        <div class="input-wrapper">
          <i class="pi pi-lock"></i>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="••••••••"
            :class="{ error: errors.password }"
            @blur="validatePassword"
          />
        </div>
        <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
      </div>

      <button type="submit" class="submit-btn">
        Войти
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const errors = ref({})

const validateLogin = () => {
  if (!username.value.trim()) {
    errors.value.username = 'Логин обязателен'
  } else if (username.value.length < 3) {
    errors.value.username = 'Логин должен быть не короче 3 символов'
  } else {
    errors.value.username = ''
  }
}

const validatePassword = () => {
  if (!password.value) {
    errors.value.password = 'Пароль обязателен'
  } else if (password.value.length < 6) {
    errors.value.password = 'Пароль должен быть не короче 6 символов'
  } else {
    errors.value.password = ''
  }
}

const handleSubmit = () => {
  validateLogin()
  validatePassword()
  if (!errors.value.username && !errors.value.password) {
   
   auth.login({username:username.value, password: password.value})
  }
}
</script>

<style scoped>
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
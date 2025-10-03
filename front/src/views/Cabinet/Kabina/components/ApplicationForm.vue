<template>
  <div class="application-form">
    <form @submit.prevent="submitApplication">
      <div class="form-row">
        <div class="form-group">
          <label>Название мероприятия *</label>
          <input v-model="form.eventName" type="text" placeholder="Введите название" required>
        </div>
        <div class="form-group">
          <label>Тип мероприятия *</label>
          <select v-model="form.eventType" required>
            <option value="">Выберите тип</option>
            <option value="Концерты">Концерты</option>
            <option value="Выставки">Выставки</option>
            <option value="Праздники">Праздники</option>
            <option value="Спектакли">Спектакли</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Дата начала *</label>
          <input v-model="form.startDate" type="date" required>
        </div>
        <div class="form-group">
          <label>Дата окончания *</label>
          <input v-model="form.endDate" type="date" required>
        </div>
      </div>

      <div class="form-group">
        <label>Адрес *</label>
        <input v-model="form.address" type="text" placeholder="Введите адрес" required>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Координата X</label>
          <input v-model="form.coordinateX" type="number" step="any" placeholder="Введите координату X">
        </div>
        <div class="form-group">
          <label>Координата Y</label>
          <input v-model="form.coordinateY" type="number" step="any" placeholder="Введите координату Y">
        </div>
      </div>

      <div class="form-group">
        <label>Организатор *</label>
        <input v-model="form.organizer" type="text" placeholder="Введите организатора" required>
      </div>

      <div class="form-group">
        <label>Описание *</label>
        <textarea v-model="form.description" placeholder="Подробное описание мероприятия" rows="4" required></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Веб-сайт</label>
          <input v-model="form.website" type="url" placeholder="https://example.com">
        </div>
        <div class="form-group">
          <label>Телефон</label>
          <input v-model="form.phone" type="tel" placeholder="+7 (XXX) XXX-XX-XX">
        </div>
      </div>

      <button type="submit" class="submit-btn">📨 Отправить заявку</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useApplicationsStore } from '../stores/applications'

const applicationsStore = useApplicationsStore()
const { createApplication } = applicationsStore

const emit = defineEmits(['submitted'])

const form = ref({
  eventName: '',
  eventType: '',
  startDate: '',
  endDate: '',
  address: '',
  coordinateX: null,
  coordinateY: null,
  organizer: '',
  description: '',
  website: '',
  phone: ''
})

const submitApplication = () => {
  createApplication(form.value)
  form.value = {
    eventName: '',
    eventType: '',
    startDate: '',
    endDate: '',
    address: '',
    coordinateX: null,
    coordinateY: null,
    organizer: '',
    description: '',
    website: '',
    phone: ''
  }
  alert('Заявка успешно отправлена! 📨')
  emit('submitted')
}
</script>

<style scoped>
.application-form {
  padding: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.submit-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
}

@media (max-width: 768px) {
  .application-form {
    padding: 15px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .form-group input,
  .form-group select,
  .form-group textarea {
    padding: 14px;
    font-size: 16px;
  }
  
  .submit-btn {
    padding: 16px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .application-form {
    padding: 12px;
  }
}
</style>
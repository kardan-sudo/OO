
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useUserStore } from "./useUserStore";
import { useRouter } from "vue-router";
import axios from "axios";
import { apiClient } from "@/main";
export const useAuthStore = defineStore("auth", () => {
  const loading = ref(false)
 const router = useRouter()
  const userStore = useUserStore();
  function logout() {
    userStore.removeUser();
  }


async function login(user) {
  loading.value = true;
  console.log('Загрузка началась:', loading.value);

  try {
    // Выполняем запрос и ждём минимум 1 секунду
    const [response] = await Promise.all([
      apiClient.post('/user/login', user),
      new Promise(resolve => setTimeout(resolve, 1500)) // ← гарантирует 1 сек минимум
    ]);

    console.log('Успешно:', response.data);
    userStore.setUser(response.data);
    console.log('Пользователь:', userStore.getUser);
    console.log('Авторизован:', userStore.getAuth);

    router.push('/');
  } catch (err) {
    console.log('Ошибка входа:', err);
    router.push('/auth');
  } finally {
    loading.value = false;
    console.log('Загрузка завершена:', loading.value);
  }
}

async function registr(user) {
  loading.value = true;
  console.log('Регистрация началась...');

  try {
    // Тоже ждём минимум 1 секунду
    const [response] = await Promise.all([
      apiClient.post('/user/register', user),
      new Promise(resolve => setTimeout(resolve, 1000))
    ]);

    console.log('Успешно создан пользователь:', response.data);
    userStore.setUser(response.data);
    console.log('Пользователь:', userStore.getUser);
    console.log('Авторизован:', userStore.getAuth);

    router.push('/');
  } catch (error) {
    console.error('Ошибка при регистрации:', error.response?.data || error.message);
    router.push('/auth');
  } finally {
    loading.value = false;
  }
}
  const getIsAuth = computed(()=>isAuth.value)
  const getLoading = computed(()=>loading.value)
  return {
    login,
    logout,
    getIsAuth,
    registr,
    getLoading
  };
});

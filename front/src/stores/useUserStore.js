import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", () => {
  const userData = localStorage.getItem("user");
  const user = ref(null);
  
  const isauth = ref(false);
  try {
    if (userData) {
      user.value = JSON.parse(userData); // Только если данные есть
      isauth.value = true
    }
  } catch (e) {
    localStorage.removeItem("user"); // Очищаем битые данные
    isauth.value = false
  }
  function setUser(newUser) {
    user.value = newUser;
    isauth.value = true; // ✅
    localStorage.setItem("user", JSON.stringify(newUser));
  }
  function removeUser() {
    user.value = null;
    isauth.value = false; // ✅
    console.log('sss')
    localStorage.removeItem("user");
  }
  function updateUser(updatedFields) {
    if (user.value && typeof updatedFields === "object") {
      user.value = { ...user.value, ...updatedFields };
      localStorage.setItem("user", JSON.stringify(user.value));
    }
  }
  const getUser = computed(() => user.value);
  const getAuth = computed(()=>isauth.value);
  return {
    setUser,
    getUser,
    removeUser,
    updateUser,
    getAuth
  };
});
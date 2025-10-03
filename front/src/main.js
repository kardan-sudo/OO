import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import { createYmaps } from 'vue-yandex-maps';
import Menubar from 'primevue/menubar'
import AOS from "aos";
import "aos/dist/aos.css";
import axios from 'axios';
export const apiClient = axios.create({
  baseURL: 'http://192.168.3.116:8000', 
});
const app = createApp(App)
const pinia = createPinia()
app.use(pinia) // Убрали дублирующий вызов createPinia()
app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
})
app.use(createYmaps({
  apikey: '6515b0e7-ea7d-49ba-9ef0-084b8bda31dd',
  importModules: ['@yandex/ymaps3-controls@0.0.1'],
}));
AOS.init({
  duration: 800,
  once: false,
});
app.component('Menubar', Menubar)

app.mount('#app')
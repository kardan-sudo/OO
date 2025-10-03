import { createRouter, createWebHistory } from 'vue-router'
import Merop from '@/views/Mer/Merop.vue'
import Peopl from '@/views/Peopl/Peopl.vue'
import Ratin from '@/views/Rating/Ratin.vue'
import Root from '@/views/Rot/Root.vue'
import Victorint from '@/views/Vict/Victorint.vue'
import Home from '@/views/Home.vue'
import Profil from '@/views/profile/Profil.vue'
import AuthForm from '@/views/Auth/AuthForm.vue'
import Cabinet from '@/views/Cabinet/Cabinet.vue'
import MyFavor from '@/views/fav/MyFavor.vue'
import Mybonus from '@/views/Bonuss/Mybonus.vue'
import MyParser from '@/views/Parser/MyParser.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/mer',
      name: 'mer',
      component: Merop,
    },
    {
      path: '/rot',
      name: 'rot',
      component: Root,
    },
    {
      path: '/rating',
      name: 'rating',
      component: Ratin,
    },
    {
      path: '/vict',
      name: 'vict',
      component: Victorint,
    },
    {
      path: '/peopl',
      name: 'peopl',
      component: Peopl,
    },
    {
      path: '/profil',
      name: 'profil',
      component: Profil,
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthForm,
    },
    {
      path: '/profile',
      name: 'profile',
      component: Cabinet,
    },
    {
      path: '/fav',
      name: 'fav',
      component: MyFavor,
    },
     {
      path: '/bonus',
      name: 'bonus',
      component: Mybonus,
    },
    {
      path: '/admin',
      name: 'admin',
      component: MyParser,
    },
  ],
})

export default router

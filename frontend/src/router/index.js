import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import RecommendView from '@/views/RecommendView.vue'
import MyPageView from '@/views/MyPageView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/mypage', name: 'mypage', component: MyPageView, meta: { requiresAuth: true } },
  { path: '/recommend', name: 'recommend', component: RecommendView, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

import HomeView from '@/views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import RecommendView from '@/views/RecommendView.vue'
import MyPageView from '@/views/MyPageView.vue'

import MapView from '@/views/MapView.vue'
import CompareView from '@/views/CompareView.vue'
import PricesView from '@/views/PricesView.vue'
import CommunityView from '@/views/CommunityView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/mypage', name: 'mypage', component: MyPageView, meta: { requiresAuth: true } },
  { path: '/recommend', name: 'recommend', component: RecommendView, meta: { requiresAuth: true } },

  // 🆕 공개 접근 가능 뷰
  { path: '/map', name: 'map', component: MapView },
  { path: '/compare', name: 'compare', component: CompareView },
  { path: '/prices', name: 'prices', component: PricesView },
  { path: '/community', name: 'community', component: CommunityView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const store = useUserStore()
  if (to.meta.requiresAuth && !store.token) {
    alert('로그인이 필요합니다.')
    next('/login')
  } else {
    next()
  }
})

export default router

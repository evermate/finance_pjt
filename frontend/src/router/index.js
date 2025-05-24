// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'  

import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/SignUp.vue'
import LoginView from '@/views/LoginView.vue'
import RecommendView from '@/views/RecommendView.vue'
import MyPageView from '@/views/MyPageView.vue'
import MapView from '@/views/MapView.vue'
import CompareView from '@/views/CompareView.vue'
import PricesView from '@/views/PricesView.vue'
import SearchView from '@/views/SearchView.vue'
import MyPageEdit from '@/views/MyPageEdit.vue'
import CommunityListView from '@/views/community/CommunityListView.vue'
import CommunityDetailView from '@/views/community/CommunityDetailView.vue'
import CommunityFormView from '@/views/community/CommunityFormView.vue'


const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/signup', name: 'signup', component: SignUpView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/mypage', name: 'mypage', component: MyPageView, meta: { requiresAuth: true } },
  { path: '/mypage/edit', name: 'mypage-edit', component: MyPageEdit },
  { path: '/recommend', name: 'recommend', component: RecommendView, meta: { requiresAuth: true } },
  { path: '/map', name: 'map', component: MapView },
  { path: '/compare', name: 'compare', component: CompareView },
  { path: '/prices', name: 'prices', component: PricesView },
  { path: '/search', name: 'search', component: SearchView },
  { path: '/community', name: 'community', component: CommunityListView },
  { path: '/community/write', name: 'community-write', component: CommunityFormView },
  { path: '/community/:id', name: 'community-detail', component: CommunityDetailView },
  { path: '/community/:id/edit', name: 'community-edit', component: CommunityFormView },
  { path: '/profile/:username', name: 'user-profile', component: () => import('@/views/community/UserProfileView.vue')},
  { path: '/search', name: 'search', component: SearchView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const store = useAccountStore()
  if (to.meta.requiresAuth && !store.user) {
    alert('로그인이 필요합니다.')
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})


export default router

// src/main.js
import axios from 'axios'

// ① 백엔드 Django 서버 주소를 기본 URL로 설정
axios.defaults.baseURL = 'http://localhost:8000'

// (세션 인증 쓰실 거면 아래 줄도 활성화)
// axios.defaults.withCredentials = true

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(Toast, {
  // 옵션 예시
  position: 'top-right',
  timeout: 2000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  hideProgressBar: false,
})

app.component('LoadingSpinner', LoadingSpinner)
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)
app.mount('#app')

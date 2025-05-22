<template>
  <header class="nav">
    <RouterLink to="/">🏠 Home</RouterLink>
    <RouterLink v-if="!user" to="/login">🔐 로그인</RouterLink>
    <RouterLink v-if="!user" to="/register">📝 회원가입</RouterLink>
    <RouterLink v-if="user" to="/mypage">👤 마이페이지</RouterLink>
    <RouterLink v-if="user" to="/recommend">💡 추천받기</RouterLink>
    <button v-if="user" @click="logout">🚪 로그아웃</button>
  </header>
</template>

<script setup>
import { useRouter, RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const user = userStore.user

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #ccc;
}
</style>

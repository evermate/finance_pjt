<template>
  <header class="nav">
    <RouterLink to="/">Home</RouterLink>

    <div class="nav-right">
      <RouterLink v-if="!user" to="/login">로그인</RouterLink>
      <RouterLink v-if="!user" to="/register">회원가입</RouterLink>
      <RouterLink v-if="user" to="/mypage">마이페이지</RouterLink>
      <RouterLink v-if="user" to="/recommend">추천받기</RouterLink>
      <button v-if="user" @click="logout" class="logout-button">로그아웃</button>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
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
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #ccc;
  background-color: #f9f9f9;
}

.nav-right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* 밑줄 제거 및 색상 조정 */
.nav a {
  text-decoration: none;
  color: inherit;
  font-weight: 500;
}

.logout-button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
}

.logout-button:hover {
  text-decoration: underline;
}

</style>

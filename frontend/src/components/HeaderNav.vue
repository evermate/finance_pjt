<template>
  <header class="nav">
    <div class="container nav-content">
      <div class="nav-left">
        <RouterLink :to="{ name: 'home' }">
          <img src="/image/image.png" alt="Bank Logo" class="logo" />
        </RouterLink>
      </div>
      <div class="nav-right">
        <nav class="nav-menu">
          <!-- <RouterLink :to="{ name: 'compare' }" class="menu-btn">예적금 금리 비교</RouterLink> -->
          <!-- 예·적금 금리 비교 -->
         <RouterLink :to="{ name: 'compare' }" class="menu-btn">예·적금 금리 비교</RouterLink>
         <!-- 현물 상품(금/은) 시세 비교 -->
         <RouterLink :to="{ name: 'prices' }" class="menu-btn">현물 상품 비교</RouterLink>
         <!-- 금융 상품 추천 -->
         <RouterLink :to="{ name: 'recommend' }" class="menu-btn">금융 상품 추천</RouterLink>
         <!-- 은행 검색 (카카오 API) -->
         <RouterLink :to="{ name: 'map' }" class="menu-btn">은행 검색</RouterLink>
         <!-- 관심 종목(유튜브) 검색 -->
         <RouterLink :to="{ name: 'search' }" class="menu-btn">관심 종목 검색</RouterLink>
         <!-- 은퇴 자산 시뮬레이션 -->
         <RouterLink :to="{ name: 'simulation' }" class="menu-btn">은퇴 자산 시뮬레이션</RouterLink>
         <!-- 커뮤니티 -->
         <RouterLink :to="{ name: 'community' }" class="menu-btn">게시판</RouterLink>
        </nav>
        <RouterLink v-if="!user" :to="{ name: 'login' }" class="btn-outline">로그인</RouterLink>
        <RouterLink v-if="!user" :to="{ name: 'signup' }" class="btn">회원가입</RouterLink>
        <RouterLink v-if="user" :to="{ name: 'mypage' }"><img src="/image/User.png" alt="User Logo" class="user-icon">
          <span class="user-name"> {{ user.username }} 님</span></RouterLink>
        <!-- <RouterLink v-if="user" :to="{ name: 'recommend' }">추천받기</RouterLink> -->
        <button v-if="user" @click="logout" class="logout-button">Logout</button>
      </div>
    </div>
  </header>
</template>


<script setup>
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { computed } from 'vue'

const userStore = useAccountStore()
const router = useRouter()

const user = computed(() => userStore.user)

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>


<style scoped>
.nav {
  background-color: #ffffff;
  border-bottom: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 30px;
}

.nav-menu {
  display: flex;
  gap: 0.75rem;
  margin-left: 2rem;
}

.menu-btn {
  background-color: #f3f3f3;
  padding: 6px 14px;
  border-radius: 12px;
  font-weight: 500;
  text-decoration: none;
  color: #222;
  font-size: 14px;
}

.nav-right {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.btn {
  padding: 6px 14px;
  border-radius: 12px;
  background-color: #111;
  color: white;
  border: none;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
}

.btn-outline {
  padding: 6px 14px;
  border-radius: 12px;
  background-color: #fff;
  color: #111;
  border: 1px solid #bbb;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
}

.logout-button {
  background: none;
  border: none;
  color: #2f80ed;
  cursor: pointer;
  font-size: 14px;
  padding: 0;
}

.logout-button:hover {
  text-decoration: underline;
}
.user-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 6px;
}

.user-icon {
  width: 28px;
  height: 28px;
}

.user-name {
  font-weight: 500;
  color: #333;
}
</style>

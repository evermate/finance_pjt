<template>
  <header class="nav fixed-nav">
    <div class="nav-wrapper">
      <!-- 좌측: 로고 -->
      <div class="nav-left">
        <RouterLink :to="{ name: 'home' }" class="logo-link">
          <img src="/image/MainLogo.png" alt="Bank Logo" class="logo" />
        </RouterLink>
      </div>

      <!-- 중앙: 메뉴 -->
      <nav class="nav-center">
        <RouterLink :to="{ name: 'compare' }" class="menu-btn">예·적금 금리 비교</RouterLink>
        <RouterLink :to="{ name: 'recommend' }" class="menu-btn">금융 상품 추천</RouterLink>
        <RouterLink :to="{ name: 'simulation' }" class="menu-btn">은퇴 자산 시뮬레이션</RouterLink>
        <RouterLink :to="{ name: 'map' }" class="menu-btn">은행 검색</RouterLink>
        <RouterLink :to="{ name: 'prices' }" class="menu-btn">현물 상품 비교</RouterLink>
        <RouterLink :to="{ name: 'search' }" class="menu-btn">관심 종목 검색</RouterLink>
        <RouterLink :to="{ name: 'community' }" class="menu-btn">게시판</RouterLink>
      </nav>

      <!-- 우측: 유저 영역 -->
      <div class="nav-right">
        <RouterLink v-if="!user" :to="{ name: 'login' }" class="btn-outline">로그인</RouterLink>
        <RouterLink v-if="!user" :to="{ name: 'signup' }" class="btn">회원가입</RouterLink>

        <div v-if="user" class="user-area">
          <RouterLink :to="{ name: 'mypage' }" class="user-link">
            <img src="/image/User.png" alt="User Icon" class="user-icon" />
            <span class="user-name">{{ user.username }} 님</span>
          </RouterLink>
          <button @click="logout" class="logout-button">로그아웃</button>
        </div>
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
/* 헤더 기본 */
.fixed-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  z-index: 1000;
}

.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 2rem;
  max-width: 1280px;
  margin: 0 auto;
}

/* 좌측: 로고 */
.logo {
  height: 40px;
}
.logo-link {
  display: flex;
  align-items: center;
}

/* 중앙 메뉴 */
.nav-center {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
}

.menu-btn {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 14px;
  background-color: white;
  color: #333;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
}
.menu-btn:hover {
  background-color: #f4f7ff;
  color: #1f4fd4;
}

/* 우측: 유저 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn, .btn-outline {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
}

.btn {
  background-color: #2c3e50;
  color: white;
  border: none;
}
.btn:hover {
  background-color: #1f2f3f;
}

.btn-outline {
  background-color: white;
  border: 1px solid #aaa;
  color: #333;
}
.btn-outline:hover {
  background-color: #f3f3f3;
}

/* 유저 정보 */
.user-area {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  color: #222;
  font-size: 14px;
}

.logout-button {
  background: none;
  border: none;
  color: black;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
}
.logout-button:hover {
  text-decoration: underline;
  color: red;
}
</style>

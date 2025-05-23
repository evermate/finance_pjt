<template>
  <div class="mypage-container">
    <h1>마이페이지</h1>

    <div v-if="user" class="mypage-box">
      <!-- ✅ 프로필 이미지 -->
      <div class="profile-image">
        <img
          v-if="user.profile_image"
          :src="`${API_BASE_URL}${user.profile_image}`"
          alt="프로필 이미지"
        />
        <p v-else class="no-image">[프로필 이미지 없음]</p>
      </div>

      <!-- ✅ 정보 박스 (폼 레이아웃처럼) -->
      <div class="info-group">
        <label>아이디</label>
        <div class="info">{{ user.username }}</div>

        <label>이메일</label>
        <div class="info">{{ user.email }}</div>

        <label>나이</label>
        <div class="info">{{ user.age ?? '미입력' }}</div>

        <label>연락처</label>
        <div class="info">{{ user.phone_number || '미입력' }}</div>

        <label>생년월일</label>
        <div class="info">{{ user.birth_date || '미입력' }}</div>

        <label>성별</label>
        <div class="info">
          <template v-if="user.gender === 'M'">남성</template>
          <template v-else-if="user.gender === 'F'">여성</template>
          <template v-else-if="user.gender === 'O'">기타</template>
          <template v-else>미입력</template>
        </div>

        <label>월 수입대</label>
        <div class="info">{{ user.monthly_income_range || '미입력' }}</div>

        <label>주거래 은행</label>
        <div class="info">{{ user.main_bank?.kor_co_nm || '미입력' }}</div>
      </div>

      <router-link to="/mypage/edit">
        <button class="edit-btn">회원정보 수정</button>
      </router-link>
    </div>

    <div v-else>
      <p>유저 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { API_BASE_URL } from '@/constants'
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

watch(() => route.fullPath, () => {
  userStore.fetchUser()
})

const userStore = useAccountStore()
const user = userStore.user

onMounted(() => {
  if (!user) {
    userStore.fetchUser()
  }
})
</script>

<style scoped>
.mypage-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
}

.mypage-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image {
  margin-bottom: 1.5rem;
}

.profile-image img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ddd;
}

.no-image {
  font-style: italic;
  color: #999;
}

.info-group {
  width: 100%;
}

.info-group label {
  display: block;
  font-weight: bold;
  margin-top: 1rem;
  margin-bottom: 0.2rem;
}

.info {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.5rem;
  background-color: #f9f9f9;
}

.edit-btn {
  margin-top: 2rem;
  padding: 0.6rem 1.2rem;
  border: 1px solid #888;
  background-color: white;
  cursor: pointer;
}
</style>

<template>
  <div class="mypage-container">
    <!-- 상단 카드: 제목만 -->
    <div class="card header-card">
      <h1 style="text-align: center;">마이페이지</h1>
    

      <!-- 하단 상세 정보 카드 -->
      <div class="card detail-card">
        <div class="top-section">
          <!-- 프로필 이미지 -->
          <div class="profile-image">
            <img
              v-if="user.profile_image"
              :src="`${API_BASE_URL}${user.profile_image}`"
              alt="프로필 이미지"
            />
            <p v-else class="no-image">[프로필 이미지 없음]</p>
          </div>

          <!-- 아이디, 이메일, 나이 -->
          <div class="basic-info">
            <label>아이디</label>
            <div class="info-box">{{ user.username }}</div>

            <label>이메일</label>
            <div class="info-box">{{ user.email }}</div>

            <label>나이</label>
            <div class="info-box">{{ user.age ?? '미입력' }}</div>
          </div>
        </div>

        <div class="info-group">
          <label>연락처</label>
          <div class="info-box">{{ user.phone_number || '미입력' }}</div>

          <label>생년월일</label>
          <div class="info-box">{{ user.birth_date || '미입력' }}</div>

          <label>성별</label>
          <div class="info-box">
            <template v-if="user.gender === 'M'">남성</template>
            <template v-else-if="user.gender === 'F'">여성</template>
            <template v-else-if="user.gender === 'O'">기타</template>
            <template v-else>미입력</template>
          </div>

          <label>월 수입대</label>
          <div class="info-box">{{ user.monthly_income_range || '미입력' }}</div>

          <label>주거래 은행</label>
          <div class="info-box">{{ user.main_bank?.kor_co_nm || '미입력' }}</div>
        </div>

        <router-link to="/mypage/edit">
          <button class="submit-btn">회원정보 수정</button>
        </router-link>
      </div>
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
const userStore = useAccountStore()
const user = userStore.user

watch(() => route.fullPath, () => {
  userStore.fetchUser()
})

onMounted(() => {
  if (!user) {
    userStore.fetchUser()
  }
})
</script>

<style scoped>
.mypage-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background-color: #f5f7fb;
  font-family: 'Pretendard', sans-serif;
}

.card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  padding: 2rem;
  margin-bottom: 2rem;
}

.header-card {
  background: linear-gradient(to right, #e9f0ff, #f4f9ff);
  /* text-align: center; */
}
.profile-image {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.top-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-image img {
  width: 130px;
  height: 130px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ccc;
}

.no-image {
  width: 130px;
  height: 130px;
  background: #eee;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-style: italic;
  color: #999;
  border: 2px solid #ccc;
}

.basic-info {
  flex: 1;
}

.info-group label,
.basic-info label {
  display: block;
  font-weight: bold;
  margin-top: 1rem;
  margin-bottom: 0.3rem;
}

.info-box {
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  background-color: #fcfcfc;
}

.edit-btn {
  margin-top: 2rem;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  background-color: #2f80ed;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s;
}

.edit-btn:hover {
  background-color: #256fd1;
}
.submit-btn {
  /* 기존 스타일 유지 */
  margin-top: 1rem;
  padding: 0.6rem 1.5rem;
  font-weight: 600;
  border: none;
  background-color: #2f80ed;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: block;
  margin-left: auto;
  margin-right: auto;

  /* 🔴 밑줄 제거 */
  text-decoration: none;
}
</style>

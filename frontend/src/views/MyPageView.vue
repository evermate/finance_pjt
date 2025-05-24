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

        <!-- <router-link to="/mypage/edit">
          <button class="submit-btn" >회원정보 수정</button>
        </router-link> -->
        <!-- 회원정보 수정 버튼 -->
        <button class="submit-btn" @click="openPasswordModal">회원정보 수정</button>

        <!-- 비밀번호 확인 모달 -->
        <div v-if="showModal" class="modal-backdrop">
          <div class="modal-content">
            <h2>개인정보 확인</h2>
            <label>비밀번호 입력</label>
            <input v-model="password" type="password" placeholder="비밀번호 입력" />
            <div class="modal-buttons">
              <button class="confirm-btn" @click="verifyPassword">확인</button>
              <button class="cancel-btn" @click="showModal = false">닫기</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { API_BASE_URL } from '@/constants'
import { watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const userStore = useAccountStore()
const user = userStore.user

const showModal = ref(false)
const password = ref('')
const openPasswordModal = () => {
  showModal.value = true
}


watch(() => route.fullPath, () => {
  userStore.fetchUser()
})

onMounted(() => {
  if (!user) {
    userStore.fetchUser()
  }
})

const verifyPassword = async () => {
  try {
    await axios.post(`${API_BASE_URL}/accounts/verify-password/`, {
      username: user.username,
      password: password.value,
    })
    router.push('/mypage/edit')
  } catch (error) {
    alert('비밀번호가 일치하지 않습니다.')
  }
}
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
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 320px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.modal-content input {
  width: 90%;
  padding: 0.5rem;
  margin: 1rem 0;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.confirm-btn {
  background-color: #0055ff;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #f0f0f0;
  padding: 0.5rem 1rem;
  border: 1px solid #aaa;
  border-radius: 6px;
  cursor: pointer;
}

</style>

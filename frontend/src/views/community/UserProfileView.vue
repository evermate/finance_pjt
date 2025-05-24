<template>
  <div class="user-profile-container" v-if="user">
    <h1>{{ user.username }}님의 프로필</h1>

    <div class="profile-section">
      <img
        v-if="user.profile_image"
        :src="`${API_BASE_URL}${user.profile_image}`"
        alt="프로필 이미지"
        class="profile-img"
      />
      <p v-else class="no-img">[프로필 이미지 없음]</p>

      <ul class="info-list">
        <li><strong>이메일:</strong> {{ user.email }}</li>
        <li><strong>나이:</strong> {{ user.age }}세</li>
        <li><strong>성별:</strong> {{ user.gender || '미입력' }}</li>
        <li><strong>주거래은행:</strong> {{ user.main_bank?.kor_co_nm || '미지정' }}</li>
        <li><strong>월 소득 구간:</strong> {{ user.monthly_income_range || '미입력' }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '@/constants'

const route = useRoute()
const user = ref(null)

onMounted(async () => {
  const username = route.params.username
  try {
    const res = await axios.get(`${API_BASE_URL}/accounts/profile/${username}/`)
    user.value = res.data
  } catch (err) {
    console.error('유저 프로필 불러오기 실패:', err)
    alert('존재하지 않는 사용자입니다.')
  }
})
</script>

<style scoped>
.user-profile-container {
  padding: 1rem;
}
.profile-section {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}
.profile-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
}
.info-list {
  list-style: none;
  padding: 0;
}
.no-img {
  font-style: italic;
  color: #999;
}
</style>

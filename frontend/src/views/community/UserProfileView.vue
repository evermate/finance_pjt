<template>
  <div class="outer-card" v-if="user">
    <!-- 상단 제목 영역 -->
    <h1 class="profile-title">{{ user.username }}님의 프로필</h1>

    <!-- 안쪽 카드: 프로필 정보 -->
    <div class="inner-card">
      <div class="profile-section">
        <div class="profile-image-box">
          <img
            v-if="user.profile_image"
            :src="`${API_BASE_URL}${user.profile_image}`"
            alt="프로필 이미지"
            class="profile-img"
          />
          <div v-else class="no-img">[프로필 이미지 없음]</div>
        </div>

        <ul class="info-list">
          <li><strong>이메일:</strong> {{ user.email }}</li>
          <li><strong>나이:</strong> {{ user.age }}세</li>
          <li><strong>성별:</strong> {{ user.gender || '미입력' }}</li>
          <li><strong>주거래은행:</strong> {{ user.main_bank?.kor_co_nm || '미지정' }}</li>
          <li><strong>월 소득 구간:</strong> {{ user.monthly_income_range || '미입력' }}</li>
        </ul>
      </div>
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
.outer-card {
  max-width: 780px;
  margin: 3rem auto;
  padding: 2.5rem;
  border-radius: 20px;
  background-color: #eef4ff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Pretendard', sans-serif;
}

.profile-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #222;
}

.inner-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.profile-section {
  display: flex;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.profile-image-box {
  flex-shrink: 0;
}

.profile-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #e1e1e1;
  background-color: #fafafa;
}

.no-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px solid #ccc;
  background-color: #f0f0f0;
  font-style: italic;
  color: #888;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 0.85rem;
  padding: 0.5rem;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}

.info-list li {
  margin-bottom: 0.7rem;
  font-size: 1.05rem;
  color: #444;
}

.info-list strong {
  display: inline-block;
  width: 110px;
  color: #222;
}

</style>

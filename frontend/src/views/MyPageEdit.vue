<template>
  <div class="signup-container">
    <h1>회원정보 수정</h1>
    <form @submit.prevent="submitForm" class="signup-form" enctype="multipart/form-data">
      <!-- ✅ 프로필 이미지 미리보기 -->
      <div class="form-group">
        <label>프로필 이미지</label>
        <div class="profile-preview">
          <img
            v-if="previewImage"
            :src="previewImage"
            alt="프로필 미리보기"
          />
          <p v-else class="no-image">[프로필 이미지 없음]</p>
        </div>
        <input type="file" @change="handleFileChange" />
      </div>

      <!-- 읽기 전용 필드들 -->
      <div class="form-group">
        <label>아이디</label>
        <input :value="user?.username" disabled />
      </div>

      <div class="form-group">
        <label>이메일</label>
        <input :value="user?.email" disabled />
      </div>

      <div class="form-group">
        <label>나이</label>
        <input :value="user?.age ?? '미입력'" disabled />
      </div>

      <!-- 수정 가능한 필드 -->
      <div class="form-group">
        <label>연락처</label>
        <input v-model="form.phone_number" />
      </div>

      <div class="form-group">
        <label>생년월일</label>
        <input type="date" v-model="form.birth_date" />
      </div>

      <div class="form-group">
        <label>성별</label>
        <select v-model="form.gender">
          <option value="">선택</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
          <option value="O">기타</option>
        </select>
      </div>

      <div class="form-group">
        <label>월 수입대</label>
        <input v-model="form.monthly_income_range" />
      </div>

      <button type="submit">수정 완료</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { API_BASE_URL } from '@/constants'

const router = useRouter()
const userStore = useAccountStore()
const token = userStore.token
const user = userStore.user

const form = ref({
  phone_number: '',
  birth_date: '',
  gender: '',
  monthly_income_range: ''
})

const imageFile = ref(null)
const previewImage = ref(null)

onMounted(() => {
  if (user) {
    form.value = {
      phone_number: user.phone_number || '',
      birth_date: user.birth_date || '',
      gender: user.gender || '',
      monthly_income_range: user.monthly_income_range || ''
    }
    if (user.profile_image) {
      previewImage.value = `${API_BASE_URL}${user.profile_image}`
    }
  }
})

const handleFileChange = (event) => {
  const file = event.target.files[0]
  imageFile.value = file
  if (file) {
    previewImage.value = URL.createObjectURL(file)
  }
}

const submitForm = async () => {
  const formData = new FormData()
  for (const key in form.value) {
    formData.append(key, form.value[key])
  }
  if (imageFile.value) {
    formData.append('profile_image', imageFile.value)
  }

  try {
    await axios.patch(`${API_BASE_URL}/accounts/mypage/update/`, formData, {
      headers: {
        Authorization: `Token ${token}`,
        'Content-Type': 'multipart/form-data',
      }
    })
    alert('수정 완료!')
    await userStore.fetchUser()  // ✅ 최신 정보 fetch

    // ✅ 새로고침 유도 방식 1: 강제 리로드
    router.push({ name: 'mypage' }).then(() => router.go())

    // ✅ 대안 방식 2: 쿼리 파라미터로 재마운트 유도 (선택사항)
    // router.push({ name: 'mypage', query: { updated: Date.now() } })

  } catch (err) {
    console.error('수정 실패:', err)
    alert('수정 실패')
  }
}
</script>


<style scoped>
.signup-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1rem;
}

.signup-form .form-group {
  margin-bottom: 1.2rem;
}

.signup-form label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

.signup-form input,
.signup-form select {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

.profile-preview {
  text-align: center;
  margin-bottom: 1rem;
}

.profile-preview img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid #ccc;
}

.no-image {
  font-style: italic;
  color: #999;
}
</style>

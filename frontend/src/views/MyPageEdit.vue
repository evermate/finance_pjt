<template>
  <div class="hero-section">
    <div class="container">
      <h1>회원정보 수정</h1>
      <h2>회원정보를 관리하세요.</h2>
    </div>
  </div>
  <div class="edit-container">
    <div class="card header-card">
      <h1 style="text-align: center;">회원정보 수정</h1>
      <div class="card detail-card">
        <form @submit.prevent="submitForm" enctype="multipart/form-data" class="edit-form">
          <div class="top-section">
            <!-- 프로필 이미지 -->
            <div class="image-box">
              <img
                v-if="previewImage"
                :src="previewImage"
                alt="프로필 이미지"
              />
              <p v-else class="no-image">[프로필 이미지 없음]</p>

              <!-- 파일 선택 -->
              <input type="file" @change="handleFileChange" class="file-input" />
            </div>

            <!-- 읽기 전용 항목 -->
            <div class="readonly-info">
              <label>아이디</label>
              <div class="readonly-box">{{ user?.username }}</div>

              <label>이메일</label>
              <div class="readonly-box">{{ user?.email }}</div>

              <label>나이</label>
              <div class="readonly-box">{{ user?.age ?? '미입력' }}</div>
            </div>
          </div>

          <!-- 수정 가능한 항목 -->
          <div class="form-group">
            <label>연락처</label>
            <input v-model="form.phone_number" class="editable-input" />
          </div>

          <div class="form-group">
            <label>생년월일</label>
            <input type="date" v-model="form.birth_date" class="editable-input" />
          </div>

          <div class="form-group">
            <label>성별</label>
            <select v-model="form.gender" class="editable-input">
              <option value="">선택</option>
              <option value="M">남성</option>
              <option value="F">여성</option>
            </select>
          </div>

          <div class="form-group">
            <label>월 수입대</label>
            <input v-model="form.monthly_income_range" class="editable-input" />
          </div>

          <button type="submit" class="submit-btn">수정 완료</button>
        </form>
      </div>
    </div>
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
.edit-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Pretendard', sans-serif;
  background-color: #f8f9fc;
}

.edit-form {
  background-color: #fff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
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
.top-section {
  display: flex;
  gap: 2rem;
  align-items: center;
  margin-bottom: 2rem;
}

.image-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-box img {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ccc;
}

.image-box input[type="file"] {
  margin-top: 1rem;
}

.no-image {
  width: 140px;
  height: 140px;
  background-color: #eee;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-style: italic;
  border: 2px solid #ccc;
}

.readonly-info {
  flex: 1;
}

.readonly-info label {
  font-weight: 600;
  margin-bottom: 0.3rem;
  display: block;
}

.readonly-box {
  background-color: #f3f6fa;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  font-weight: 600;
  display: block;
  margin-bottom: 0.4rem;
}

.editable-input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-sizing: border-box;
  background-color: #fff;
}

.submit-btn {
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
}

.submit-btn:hover {
  background-color: #256fd1;
}

.hero-section {
  background-image: url('/image/notebook.jpg'); /* ← 여기에 넣고 싶은 이미지 경로 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  height: 300px; /* 필요에 따라 조정 */
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white; /* 이미지 위 텍스트를 흰색으로 */
}

.container h1 {
  font-size: 2.5rem;
  font-weight: bold;
}

.container h2 {
  font-size: 1.2rem;
  margin-top: 0.5rem;
}

</style>

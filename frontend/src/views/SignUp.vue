<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="onSignUp" class="signup-form">
      <div class="form-group">
        <label for="username">사용자명</label>
        <div class="input-with-button">
          <input id="username" v-model="username" placeholder="사용자명" />
          <button type="button" @click="checkUsername">중복 확인</button>
        </div>
        <p v-if="errors.username" class="error-msg">{{ errors.username }}</p>
        <p v-else-if="usernameStatus === 'taken'" class="error-msg">❌ 이미 사용 중인 아이디입니다.</p>
        <p v-else-if="usernameStatus === 'available'" class="valid-msg">✔ 사용 가능한 아이디입니다.</p>

      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input id="email" v-model="email" type="email" placeholder="이메일" />
        <p v-if="errors.email" class="error-msg">{{ errors.email }}</p>
      </div>

      <!-- 비밀번호 -->
      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input id="password1" v-model="password1" type="password" placeholder="비밀번호" />
        <p v-if="passwordError" class="error-msg">{{ passwordError }}</p>
        <p v-else-if="password1.length >= 8" class="valid-msg">✔ 사용 가능한 비밀번호입니다.</p>
      </div>

      <!-- 비밀번호 확인 -->
      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input id="password2" v-model="password2" type="password" placeholder="비밀번호 확인" />
        <p v-if="passwordConfirmError" class="error-msg">{{ passwordConfirmError }}</p>
        <p v-else-if="password2 && password2 === password1" class="valid-msg">✔ 비밀번호가 일치합니다.</p>
      </div>


      <!-- ✅ 생년월일 select 입력 -->
      <div class="form-group">
        <label>생년월일</label>
        <div class="birth-selects">
          <select v-model="birthYear">
            <option value="">년도</option>
            <option v-for="y in years" :key="y" :value="y">{{ y }}년</option>
          </select>
          <select v-model="birthMonth">
            <option value="">월</option>
            <option v-for="m in 12" :key="m" :value="String(m).padStart(2, '0')">{{ m }}월</option>
          </select>
          <select v-model="birthDay">
            <option value="">일</option>
            <option v-for="d in 31" :key="d" :value="String(d).padStart(2, '0')">{{ d }}일</option>
          </select>
        </div>
      </div>
      <p v-if="errors.birth_date" class="error-msg">{{ errors.birth_date }}</p>

      <button type="submit">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'
import axios from 'axios'

const accountStore = useAccountStore()
const errors = ref({})
const usernameStatus = ref(null)
const passwordError = ref('')
const passwordConfirmError = ref('')


const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')

// 생년월일 관련
const birthYear = ref('')
const birthMonth = ref('')
const birthDay = ref('')
const years = Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - i)

const birth_date = computed(() => {
  if (birthYear.value && birthMonth.value && birthDay.value) {
    return `${birthYear.value}-${birthMonth.value}-${birthDay.value}`
  }
  return ''
})

const onSignUp = async () => {
  errors.value = {}
  passwordError.value = ''
  passwordConfirmError.value = ''

  // ✅ 아이디 중복 확인 여부 검사
  if (usernameStatus.value !== 'available') {
    errors.value.username = '아이디 중복 확인이 필요합니다.'
    return
  }

  // ✅ 비밀번호 유효성 검사
  if (password1.value.length < 8) {
    passwordError.value = '비밀번호는 최소 8자 이상이어야 합니다.'
    return
  }

  if (password1.value !== password2.value) {
    passwordConfirmError.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  const userInfo = {
    username: username.value,
    birth_date: birth_date.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value
  }

  try {
    await accountStore.signUp(userInfo)
  } catch (err) {
    const resErrors = err.response?.data
    if (resErrors) {
      errors.value = Object.fromEntries(
        Object.entries(resErrors).map(([key, val]) => [key, Array.isArray(val) ? val[0] : val])
      )

      // 서버에서 중복된 username 에러가 다시 올 수도 있으므로 상태 리셋
      if (resErrors.username) {
        usernameStatus.value = 'taken'
      }
    }
  }
}


const checkUsername = async () => {
  usernameStatus.value = null
  errors.value.username = ''

  if (!username.value.trim()) {
    errors.value.username = '아이디를 입력해주세요.'
    return
  }

  try {
    const res = await axios.get('/accounts/check-username/', {
      params: { username: username.value }
    })

    usernameStatus.value = res.data.available ? 'available' : 'taken'

    // if (!res.data.available) {
    //   errors.value.username = '이미 사용 중인 아이디입니다.'
    // }
  } catch (err) {
    console.error('아이디 중복 확인 실패:', err)
    errors.value.username = '중복 확인 중 오류가 발생했습니다.'
  }
}

watch(username, () => {
  usernameStatus.value = null
})

watch(password1, (val) => {
  if (val.length < 8) {
    passwordError.value = '비밀번호는 최소 8자 이상이어야 합니다.'
  } else {
    passwordError.value = ''
  }

  // 비밀번호 확인과도 비교
  if (password2.value && password2.value !== val) {
    passwordConfirmError.value = '비밀번호가 일치하지 않습니다.'
  } else {
    passwordConfirmError.value = ''
  }
})

watch(password2, (val) => {
  if (val !== password1.value) {
    passwordConfirmError.value = '비밀번호가 일치하지 않습니다.'
  } else {
    passwordConfirmError.value = ''
  }
})

</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1rem;
}

.signup-form .form-group {
  margin-bottom: 1rem;
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

.birth-selects {
  display: flex;
  gap: 0.5rem;
}

.error-msg {
  color: #e03131;
  font-size: 0.85rem;
  margin-top: 0.2rem;
}

.input-with-button {
  display: flex;
  gap: 0.5rem;
}

.input-with-button input {
  flex: 1;
}

.input-with-button button {
  padding: 0.4rem 0.8rem;
  background-color: #ddd;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.input-with-button button:hover {
  background-color: #ccc;
}

.valid-msg {
  color: #2f9e44;
  font-size: 0.85rem;
  margin-top: 0.2rem;
}

/* 추가 및 수정된 스타일 */
.signup-container {
  max-width: 360px;
  margin: 60px auto;
  padding: 2rem;
  background-color: #f9fbfd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.signup-container h1 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
}

.signup-form .form-group {
  margin-bottom: 1.2rem;
}

.signup-form label {
  display: block;
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.3rem;
}

.signup-form input,
.signup-form select {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
}

.input-with-button button {
  padding: 0.55rem 0.9rem;
  background-color: #eee;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.9rem;
}

.input-with-button button:hover {
  background-color: #ddd;
}

.birth-selects {
  display: flex;
  gap: 0.5rem;
}

button[type="submit"] {
  width: 100%;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.7rem;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background-color 0.3s;
}

button[type="submit"]:hover {
  background-color: #0066d9;
}

.error-msg {
  color: #e03131;
  font-size: 0.85rem;
  margin-top: 0.3rem;
}

.valid-msg {
  color: #2f9e44;
  font-size: 0.85rem;
  margin-top: 0.3rem;
}

</style>

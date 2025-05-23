<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="onSignUp" class="signup-form">
      <div class="form-group">
        <label for="username">사용자명</label>
        <input id="username" v-model="username" placeholder="사용자명" />
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input id="email" v-model="email" type="email" placeholder="이메일" />
      </div>

      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input id="password1" v-model="password1" type="password" placeholder="비밀번호" />
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input id="password2" v-model="password2" type="password" placeholder="비밀번호 확인" />
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

      <button type="submit">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'

const accountStore = useAccountStore()

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

const onSignUp = function () {
  const userInfo = {
    username: username.value,
    birth_date: birth_date.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value
  }
  accountStore.signUp(userInfo)
}
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
</style>

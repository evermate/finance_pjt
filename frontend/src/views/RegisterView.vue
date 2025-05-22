<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="submit" class="signup-form">
      <div class="form-group">
        <label for="username">사용자명</label>
        <input id="username" v-model="form.username" placeholder="사용자명" />
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input id="email" v-model="form.email" type="email" placeholder="이메일" />
      </div>

      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input id="password1" v-model="form.password1" type="password" placeholder="비밀번호" />
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input id="password2" v-model="form.password2" type="password" placeholder="비밀번호 확인" />
      </div>

      <div class="form-group">
        <label for="age">나이 (선택)</label>
        <input id="age" v-model="form.age" type="number" placeholder="나이" />
      </div>

      <button type="submit">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const form = ref({
  username: '',
  email: '',
  password1: '',
  password2: '',
  age: null,
})

const submit = async () => {
  try {
    await userStore.register(form.value)
    alert('회원가입 완료')
  } catch (err) {
    const errorData = err.response?.data || { error: '알 수 없는 오류 발생' }
    alert('회원가입 실패: ' + JSON.stringify(errorData))
    console.error('회원가입 실패 디버그:', err)
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
  margin-bottom: 1rem;
}

.signup-form label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

.signup-form input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>

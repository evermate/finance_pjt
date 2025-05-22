<template>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="submit" class="login-form">
      <div class="form-group">
        <label for="username">사용자명</label>
        <input id="username" v-model="form.username" placeholder="사용자명" />
      </div>

      <div class="form-group">
        <label for="password">비밀번호</label>
        <input id="password" v-model="form.password" type="password" placeholder="비밀번호" />
      </div>

      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const form = ref({ username: '', password: '' })

const submit = async () => {
  try {
    await userStore.login(form.value)
    alert('로그인 성공')
  } catch (err) {
    alert('로그인 실패: ' + JSON.stringify(err.response?.data || { error: '알 수 없는 오류' }))
    console.error('로그인 에러:', err)
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1rem;
}

.login-form .form-group {
  margin-bottom: 1rem;
}

.login-form label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

.login-form input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>

<!-- LoginView.vue -->
<template>
  <div class="login-container">
    <form @submit.prevent="onLogIn" class="login-form">
      <label for="username">아이디</label>
      <div class="form-input">
        <input id="username" v-model="username" placeholder="아이디" type="text" />
      </div>

      <label for="password">비밀번호</label>
      <div class="form-input">
        <input id="password" v-model="password" placeholder="비밀번호" type="password" />
      </div>
      <br>

      <button type="submit" class="login-btn">로그인</button>
      <hr class="custom-hr" />
      <RouterLink to="/signup" class="register-btn">회원가입</RouterLink>
    </form>
    


  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
import { useToast } from 'vue-toastification'


const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const username = ref('')
const password = ref('')

const toast = useToast()

const onLogIn = async () => {
  const userInfo = {
    username: username.value,
    password: password.value
  }
  try {
    await accountStore.logIn(userInfo)
    toast.success(`${username.value}님, 환영합니다!`)
    router.push(route.query.redirect || '/')
  } catch (err) {
    toast.error('로그인에 실패했습니다. 아이디 또는 비밀번호를 확인하세요.')
  }
}

</script>

<style scoped>
.login-container {
  max-width: 360px;
  margin: 60px auto;
  padding: 2rem;
  background-color: #f9fbfd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  font-family: sans-serif;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

label {
  font-weight: 600;
  margin-bottom: 0.3rem;
  font-size: 0.95rem;
}

input {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
  background-color: #fff;
}

.login-btn {
  width: 100%;
  background-color: #0074ff;
  color: white;
  border: none;
  padding: 0.7rem;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #0066d9;
}

.register-btn {
  display: block;
  width: 100%;
  text-align: center;
  border: 1px solid #ccc;
  background-color: white;
  color: #333;
  padding: 0.7rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.2s;
}

.register-btn:hover {
  background-color: #f2f2f2;
}

.custom-hr {
  border: none;
  height: 1px;
  background-color: #ccc;
  margin: 1.5rem 0;
}

.login-btn,
.register-btn {
  width: 100%;
  padding: 0.7rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  box-sizing: border-box; /* ✅ 중요: 내부 패딩 포함 너비 계산 */
}

.login-btn {
  background-color: #0074ff;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #0066d9;
}

.register-btn {
  display: block;
  text-align: center;
  border: 1px solid #ccc;
  background-color: white;
  color: #333;
  text-decoration: none;
  transition: background-color 0.2s;
}

.register-btn:hover {
  background-color: #f2f2f2;
}

</style>

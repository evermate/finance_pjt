<!-- LoginView.vue -->
<template>
  <div class="login-container">
    <form @submit.prevent="onLogIn" class="login-form">
      <label for="username">아이디</label>
      <div class="form-input">
        <input
          id="username"
          v-model="username"
          placeholder="아이디"
          type="text"
        />
      </div>

      <label for="password">비밀번호</label>
      <div class="form-input">
        <input
          id="password"
          v-model="password"
          placeholder="비밀번호"
          type="password"
        />
      </div>

      <button type="submit" class="login-btn">로그인</button>
   </form>
      <hr class="custom-hr" />
      <RouterLink to="/signup" class="register-btn">회원가입</RouterLink>
 
    
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts.js'

  const accountStore = useAccountStore()

  const username = ref('')
  const password = ref('')
  const onLogIn = function () {
    const userInfo = {
      username: username.value,
      password: password.value
    }
    accountStore.logIn(userInfo)
  }
</script>

<style scoped>
.login-container {
  max-width: 360px;
  margin: 60px auto 30px;
  padding: 1rem;
  font-family: sans-serif;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-input {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  background-color: #fafafa;
}

input {
  border: none;
  outline: none;
  width: 100%;
  background: transparent;
  font-size: 14px;
}

.login-btn {
  background-color: #0074ff;
  color: white;
  border: none;
  padding: 12px 0;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  font-size: 16px;
}

.register-btn {
  display: block;
  text-align: center;
  border: 1px solid #ccc;
  background-color: white;
  color: #333;
  padding: 12px 0;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
}

.footer {
  text-align: center;
  font-size: 12px;
  color: #999;
  margin-top: 1.5rem;
}

.custom-hr {
  border: none;
  height: 1px;
  background-color: #ccc;
  margin: 20px 0;
}
</style>

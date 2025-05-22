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

      <div class="form-group">
        <label for="age">나이 (선택)</label>
        <input id="age" v-model="age" type="number" placeholder="나이" />
      </div>

      <button type="submit">가입하기</button>
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts.js'
  
  const accountStore = useAccountStore()

  const username = ref('')
  const age = ref('')
  const email = ref('')
  const password1 = ref('')
  const password2 = ref('')

  const onSignUp = function () {
    const userInfo = {
      username: username.value,
      age: age.value,
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

.signup-form input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}
</style>

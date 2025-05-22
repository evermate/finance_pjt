<template>
  <div>
    <h1>로그인</h1>
    <form @submit.prevent="submit">
      <input v-model="form.username" placeholder="사용자명" />
      <input v-model="form.password" type="password" placeholder="비밀번호" />
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
    alert('로그인 실패: ' + JSON.stringify(err.response.data))
  }
}
</script>

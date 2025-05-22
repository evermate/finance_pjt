<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="submit">
      <input v-model="form.username" placeholder="사용자명" />
      <input v-model="form.email" type="email" placeholder="이메일" />
      <input v-model="form.password1" type="password" placeholder="비밀번호" />
      <input v-model="form.password2" type="password" placeholder="비밀번호 확인" />
      <input v-model="form.age" type="number" placeholder="나이 (선택)" />
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

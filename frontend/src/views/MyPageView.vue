<!-- src/views/MyPageView.vue -->
<template>
  <div>
    <h1>마이페이지</h1>
    <div v-if="user">
      <p><strong>아이디:</strong> {{ user.username }}</p>
      <p><strong>이메일:</strong> {{ user.email }}</p>
      <p v-if="user.age !== null"><strong>나이:</strong> {{ user.age }}</p>
    </div>
    <div v-else>
      <p>유저 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'  // ✅ store import 수정

const userStore = useAccountStore()
const user = userStore.user

onMounted(() => {
  if (!user) {
    userStore.fetchUser()  // ✅ fetchUser 메서드 호출
  }
})
</script>


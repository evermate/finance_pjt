<template>
  <div>
    <LoadingSpinner v-if="isLoading" />
    <div v-else>
      <h1>추천 결과입니다!</h1>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const isLoading = ref(true)

onMounted(() => {
  // 💡 API 없이 테스트용 딜레이 (3초)
  setTimeout(() => {
    isLoading.value = false
  }, 3000)
})
</script>

<style scoped>
</style>

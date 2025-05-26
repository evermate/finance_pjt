<template>
  <div class="loading-container">
    <p>{{ message }}</p>
    <img :src="currentImage" alt="로딩 이미지" class="loading-image" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  message: {
    type: String,
    default: '결과 생성 중입니다.'
  }
})

const images = [
  new URL('@/assets/loading1.png', import.meta.url).href,
  new URL('@/assets/loading2.png', import.meta.url).href,
]
const currentImage = ref(images[0])
let index = 0
let intervalId = null

onMounted(() => {
  intervalId = setInterval(() => {
    index = (index + 1) % images.length
    currentImage.value = images[index]
  }, 1000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
}

.loading-image {
  width: 400px; /* ⬅️ 기존 100px → 150px (또는 200px 등으로 확대) */
  height: auto;
  margin-top: 1rem;
  animation: fadeIn 0.5s ease-in-out;
}


@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

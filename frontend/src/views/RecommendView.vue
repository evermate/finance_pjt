<!-- src/views/RecommendView.vue -->
<template>
  <section class="p-6">
    <h1 class="text-2xl font-semibold mb-4">맞춤 예금/적금 상품 추천</h1>

    <!-- 1) 자산 선택 폼 -->
    <form @submit.prevent="onSubmit" class="space-y-4 mb-6">
      <label class="block font-medium">자산 (원 단위 숫자로 입력)</label>
      <input
        v-model.number="asset"
        type="number"
        min="0"
        placeholder="예) 100000000"
        class="border rounded p-2 w-full"
      />

      <button
        type="submit"
        class="bg-blue-600 text-white px-4 py-2 rounded"
        :disabled="recommendStore.loading"
      >
        {{ recommendStore.loading ? '로딩 중...' : '추천 받기' }}
      </button>
    </form>

    <!-- 2) 에러 메시지 -->
    <p v-if="recommendStore.error" class="text-red-500 mb-4">
      오류가 발생했습니다: {{ recommendStore.error.message }}
    </p>

    <!-- 3) 로딩 스피너 -->
    <LoadingSpinner v-if="recommendStore.loading" class="mx-auto mb-4" />

    <!-- 4) 추천 결과 카드 그리드 -->
    <div v-if="recommendStore.recommendations.length" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <ProductCard
        v-for="rec in recommendStore.recommendations"
        :key="rec.option_id"
        :product="rec"
      />
    </div>

    <!-- 5) 결과 없을 때 안내 -->
    <p v-else-if="!recommendStore.loading">아직 추천을 받지 않았습니다.</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ProductCard from '@/components/ProductCard.vue'
import { useRecommendStore } from '@/stores/recommend.js'

// 1) Pinia 스토어
const recommendStore = useRecommendStore()

// 2) 자산 입력값 (숫자)
const asset = ref(0)

// 3) 폼 제출 핸들러
function onSubmit() {
  recommendStore.fetchByProfile(asset.value, 10)
}
</script>

<style scoped>
/* 필요 시 추가 스타일 */
</style>

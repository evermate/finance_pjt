<!-- src/views/RecommendView.vue -->
<template>
  <section class="p-6">
    <!-- 제목 -->
    <h1 class="text-2xl font-semibold mb-4">맞춤 예금/적금 상품 추천</h1>

    <!-- 자산 입력 폼 + 버튼 -->
    <div class="flex items-center mb-6 space-x-4">
      <!-- 기존 추천 폼 -->
      <form @submit.prevent="onSubmit" class="flex items-center space-x-2">
        <label class="font-medium">자산 (원 단위)</label>
        <input
          v-model.number="asset"
          type="number"
          min="0"
          placeholder="예) 100000000"
          class="border rounded p-2 w-40"
        />
        <button
          type="submit"
          class="bg-blue-600 text-white px-4 py-2 rounded"
          :disabled="recommendStore.loading"
        >
          {{ recommendStore.loading ? '로딩 중…' : '추천 받기' }}
        </button>
      </form>

      <!-- AI 고도화된 추천 버튼 -->
      <button
        @click="onAiRecommend"
        class="bg-green-600 text-white px-4 py-2 rounded"
        :disabled="aiLoading"
      >
        {{ aiLoading ? 'AI 추천 중...' : 'AI를 활용한 고도화된 추천' }}
      </button>
    </div>

    <!-- AI 분석 리포트 (3개 카드) -->
    <AiReport v-if="aiRecs.length" :recs="aiRecs" />

    <!-- 기존 추천 에러 -->
    <p v-if="recommendStore.error" class="text-red-500 mb-4">
      오류 발생: {{ recommendStore.error.message }}
    </p>

    <!-- 기존 추천 로딩 스피너 -->
    <LoadingSpinner v-if="recommendStore.loading" class="mx-auto my-4" />

    <!-- 기존 추천 10개 결과 (세로 나열 카드) -->
    <div v-if="recommendStore.recommendations.length && !recommendStore.loading">
      <ProductCard
        v-for="rec in recommendStore.recommendations"
        :key="rec.option_id"
        :product="rec"
      />
    </div>

    <!-- AI 추천 에러 -->
    <p v-else-if="aiError" class="text-red-500">
      AI 추천 실패: {{ aiError.message }}
    </p>

    <!-- 추천 결과가 아직 없을 때 안내 -->
    <p
      v-else-if="!recommendStore.recommendations.length && !recommendStore.loading && !aiLoading"
      class="text-gray-500 mt-4"
    >
      아직 추천을 받지 않았습니다.
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ProductCard    from '@/components/ProductCard.vue'
import AiReport       from '@/components/AiReport.vue'
import { useRecommendStore } from '@/stores/recommend.js'

// 1) 기존 추천 스토어
const recommendStore = useRecommendStore()

// 2) 자산 입력값
const asset = ref(0)

// 3) AI 추천용 상태
const aiRecs    = ref([])   // AI가 골라준 3개 상품
const aiLoading = ref(false)
const aiError   = ref(null)

// 4) 기존 추천 함수
function onSubmit() {
  recommendStore.fetchByProfile(asset.value, 10)
}

// 5) AI 추천 함수
async function onAiRecommend() {
  aiLoading.value = true
  aiError.value   = null
  try {
    const res = await axios.get('/api/products/ai-recommend/', {
      params: { asset: asset.value }
    })
    aiRecs.value = res.data
  } catch (err) {
    aiError.value = err
  } finally {
    aiLoading.value = false
  }
}
</script>

<style scoped>
/* 필요에 따라 추가 스타일링 */
</style>

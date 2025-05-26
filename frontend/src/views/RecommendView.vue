<template>
  <section class="recommend-wrapper">
    <div class="hero-section">
      <div class="overlay"></div>
      <div class="container">
        <h1>금융 상품 추천받기</h1>
        <h2>고객님을 위한 추천 시스템</h2>
      </div>
    </div>

    <div class="recommend-card">
      <h1 class="title">평가되는 패널과 카드 아이콘을 골라요</h1>
      <p class="subtitle">협업 금융 AI를 활용해 고객에게 차례적인 상품을 제시합니다.</p>

      <div class="action-area">
        <form @submit.prevent="onSubmit" class="input-area">
          <label>자산</label>
          <input v-model.number="asset" type="number" min="0" placeholder="예) 1000000" />
          <button :disabled="recommendStore.loading">
            {{ recommendStore.loading ? '로딩 중...' : '일반 추천' }}
          </button>
        </form>

        <button @click="onAiRecommend" class="ai-button" :disabled="recommendStore.aiLoading">
          {{ recommendStore.aiLoading ? 'AI 추천 중...' : 'AI 다양도 고도화 추천' }}
        </button>

        <!-- ✅ 리셋 버튼 -->
        <button @click="onReset" class="reset-button">
          리셋
        </button>
      </div>
    </div>

    <!-- AI 추천 결과 -->
    <AiReport v-if="recommendStore.aiRecs.length && !recommendStore.aiLoading" :recs="recommendStore.aiRecs" />
    <LoadingSpinner v-else-if="recommendStore.aiLoading" message="AI 추천을 생성 중입니다..." />
    <p v-else-if="recommendStore.aiError" class="error-msg">AI 추천 실패: {{ recommendStore.aiError.message }}</p>

    <!-- 일반 추천 결과 -->
    <LoadingSpinner v-if="recommendStore.loading" class="mx-auto my-4" />
    <div v-if="recommendStore.recommendations.length && !recommendStore.loading">
      <ProductCard v-for="rec in recommendStore.recommendations" :key="rec.option_id" :product="rec" />
    </div>
    <p v-else-if="!recommendStore.recommendations.length && !recommendStore.loading && !recommendStore.aiLoading"
      class="no-result">
      아직 추천 결과가 없습니다.
    </p>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useRecommendStore } from '@/stores/recommend.js'
import ProductCard from '@/components/ProductCard.vue'
import AiReport from '@/components/AiReport.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const recommendStore = useRecommendStore()

// ✅ 스토어와 연결된 반응형 자산 입력
const asset = computed({
  get: () => recommendStore.aiAsset,
  set: (val) => (recommendStore.aiAsset = val),
})

function onSubmit() {
  recommendStore.fetchByProfile(asset.value, 10)
}

function onAiRecommend() {
  recommendStore.fetchAiRecommend()
}

function onReset() {
  recommendStore.resetAll()
}
</script>


<style scoped>
.recommend-wrapper {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Pretendard', sans-serif;
}

.recommend-card {
  background-color: #f9fbff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  text-align: center;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a237e;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #555;
  margin-bottom: 1.5rem;
}

.action-area {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  align-items: center;
}

.input-area {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.input-area input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 160px;
}

.input-area button,
.ai-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  background-color: #1e88e5;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.input-area button:hover,
.ai-button:hover {
  background-color: #1565c0;
}

.ai-button {
  background-color: #43a047;
}

.ai-button:hover {
  background-color: #2e7d32;
}

.error-msg {
  color: #c00;
  text-align: center;
  margin: 1rem 0;
}

.no-result {
  text-align: center;
  color: #777;
  margin-top: 2rem;
  font-style: italic;
}

.hero-section {
  position: relative;
  background-image: url('/image/4.jpg');
  /* ← 여기에 넣고 싶은 이미지 경로 */
  background-size: cover;
  background-position: center;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
}

.container {
  color: white;
  font-size: 1.8rem;
  font-weight: bold;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.7);
}

.hero-section .overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  /* ✅ 어두운 반투명 오버레이 */
  z-index: 1;
}

.hero-section .container {
  position: relative;
  z-index: 2;
}

.hero-section h1,
.hero-section h2 {
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.7);
  /* ✅ 추가 가독성 */
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  min-height: 300px;
  /* 카드 영역 크기 비슷하게 */
  margin-top: 1rem;
}

.loading-image {
  width: 240px;
  /* 카드 가로 크기와 비슷하게 */
  height: auto;
  margin-top: 1rem;
  animation: fadeIn 0.5s ease-in-out;
}

.reset-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  background-color: #ff5858;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reset-button:hover {
  background-color: #ff0000;
}

</style>

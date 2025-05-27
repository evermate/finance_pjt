<template>
  <!-- ✅ 상단 배너 추가 -->
  <div class="banner-section">
    <img src="/image/recommend.jpg" alt="시뮬레이션" class="banner-img" />
    <div class="banner-text">
      <h2>금융 상품 추천받기</h2>
      <p>자산과 AI 분석 기반으로 맞춤형 금융 상품을 추천 받으세요</p>
    </div>
  </div>
  <section class="recommend-wrapper">
    <div class="recommend-card">
      <h1 class="title">내 자산에 맞는 금융 상품 추천</h1>
      <p class="subtitle">AI 분석으로 나에게 맞는 금융 상품을 찾아드립니다</p>

      <div class="action-area">
        <form @submit.prevent="onSubmit" class="input-area">
          <label>자산</label>
          <input v-model.number="asset" type="number" min="0" placeholder="예) 1000000" />
          <button :disabled="recommendStore.loading">
            {{ recommendStore.loading ? '로딩 중...' : '일반 추천' }}
          </button>
        </form>

        <button @click="onAiRecommend" class="ai-button" :disabled="recommendStore.aiLoading">
          {{ recommendStore.aiLoading ? 'AI 추천 중...' : 'AI 분석 추천' }}
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

    <h5 class="report-title">&nbsp; 자산 기반 상품 추천</h5>
    <!-- 일반 추천 결과 -->
    <LoadingSpinner v-if="recommendStore.loading" class="mx-auto my-4" />
    <div v-if="recommendStore.recommendations.length && !recommendStore.loading" class="product-list">
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
  background-color: #ffffff;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  margin-bottom: 2.5rem;
  text-align: center;
}

.title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #1a237e;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #444;
  font-size: 1rem;
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
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  width: 180px;
  font-size: 0.95rem;
}

.input-area button,
.ai-button,
.reset-button {
  padding: 0.55rem 1.4rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 2px 5px rgba(0,0,0,0.06);
}

/* 일반 추천: 토스 블루 계열 */
.input-area button {
  background-color: #3182f6;  /* 연한 하늘색 계열 */
  color: #fff;
}
.input-area button:hover {
  background-color: #1a73e8;
}

/* AI 추천: 토스 그린 계열 */
.ai-button {
  background-color: #2dd7a4;  /* 연한 민트 */
  color: #fff;
}
.ai-button:hover {
  background-color: #1ac89a;
}

/* 리셋: 연그레이 + 진회색 텍스트 */
.reset-button {
  background-color: #f3f4f6;
  color: #374151;
  text-align: right;
}
.reset-button:hover {
  background-color: #e5e7eb;
}

.product-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.4rem; /* ✅ 간격 줄이기 (기존 1.25rem → 0.75rem) */
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

.banner-section {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 2.5rem;
}

.banner-img {
  width: 100%;
  height: 250%;
  object-fit: cover;
  object-position: bottom;
  filter: brightness(0.6);
}

.banner-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 2;
}

.banner-text h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.banner-text p {
  font-size: 1.1rem;
  font-weight: 400;
}

.report-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #1e293b;
}

</style>

<template>
  <div class="prod-card mb-4">
    <!-- 은행 로고 -->
    <img
      :src="getBankLogo(product.bank.fin_co_no)"
      alt="은행 로고"
      class="prod-card-thumb mb-2"
    />
    <div class="prod-card-body">
      <h3 class="prod-card-title">{{ product.fin_prdt_nm }}</h3>
      <p class="prod-card-meta">은행: {{ product.bank.kor_co_nm }}</p>
      <p class="prod-card-meta">기간: {{ product.save_trm }}개월 | 금리: {{ product.intr_rate }}%</p>
      <!-- AI 추천인 경우 reason이 있을 수 있으니 조건부로 렌더 -->
      <p v-if="product.reason" class="prod-card-desc mt-2">{{ product.reason }}</p>
      <!-- 가입 버튼 -->
      <button class="prod-card-btn mt-4">상품 가입</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

// fin_co_no 기반 은행 로고 경로 생성
function getBankLogo(finCoNo) {
  return `/images/banks/${finCoNo}.png`
}
</script>

<style scoped>
.prod-card {
  display: flex;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  padding: 1rem;
  align-items: center;
}
.prod-card-thumb {
  width: 64px;
  height: 64px;
  object-fit: contain;
  margin-right: 1rem;
}
.prod-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.prod-card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}
.prod-card-meta {
  font-size: 0.9rem;
  color: #555;
}
.prod-card-desc {
  font-size: 0.9rem;
  color: #666;
}
.prod-card-btn {
  align-self: flex-start;
  margin-top: auto;
  padding: 0.5rem 1rem;
  background-color: #0074ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color .2s;
}
.prod-card-btn:hover {
  background-color: #005ecc;
}
</style>

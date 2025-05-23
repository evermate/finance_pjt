<!-- src/components/ProductCard.vue -->
<template>
  <div class="border rounded p-4 shadow">
    <!-- 상품명 -->
    <h2 class="text-lg font-bold mb-1">{{ product.fin_prdt_nm }}</h2>
    <!-- 은행명 -->
    <p class="text-sm mb-1">은행: {{ product.bank.kor_co_nm }}</p>
    <!-- 기간, 금리 -->
    <p class="text-sm">
      기간: {{ product.save_trm }}개월
      &nbsp;|&nbsp;
      금리: {{ product.intr_rate }}%
    </p>
  </div>
</template>

<script setup>
// props 선언
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
/* 필요하면 스타일 조절 */
</style>

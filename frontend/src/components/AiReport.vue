<!-- src/components/AiReport.vue -->
<template>
  <section class="ai-report mb-8">
    <h2 class="text-xl font-semibold mb-4">AI 분석 리포트</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        v-for="rec in recs"
        :key="rec.fin_prdt_cd"
        class="border p-4 rounded shadow"
      >
        <h3 class="font-bold mb-2">{{ rec.fin_prdt_nm }}</h3>
        <p>은행: {{ rec.bank.kor_co_nm }}</p>
        <p>기간: {{ rec.save_trm }}개월 | 금리: {{ rec.intr_rate }}%</p>
        <p class="mt-2 text-sm text-gray-700">이유: {{ rec.reason }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  recs: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.ai-report {
  /* 필요하면 스타일 추가 */
}
</style>

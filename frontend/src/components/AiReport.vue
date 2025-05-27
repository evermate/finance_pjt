<!-- AiReport.vue -->
<template>
  <section class="ai-report mb-8">
    <h2 class="text-xl font-semibold mb-4">AI 분석 리포트</h2>
    <div class="video-grid">
      <div v-for="rec in recs" :key="rec.fin_prdt_cd" class="prod-card">
        <!-- ✅ 은행 이름 기반 로고 적용 -->
        <img :src="getBankLongIcon(rec.bank.kor_co_nm)" alt="은행 로고" class="prod-card-thumb" />

        <div class="prod-card-body">
          <router-link class="prod-name-link" :to="`/product/${rec.product_type || 'saving'}/${rec.fin_prdt_cd}`"
            :title="rec.fin_prdt_nm">
            {{ rec.fin_prdt_nm }}
          </router-link>
          <p class="prod-card-meta">은행: {{ rec.bank.kor_co_nm }}</p>
          <p class="prod-card-meta">기간: {{ rec.save_trm }}개월</p>
          <p class="prod-card-meta">금리: {{ rec.intr_rate }}%</p>
          <p class="prod-card-desc">{{ rec.reason }}</p>
          <button class="prod-card-btn" :class="{ joined: isJoined(rec.fin_prdt_cd, rec.option_id) }"
            @click="toggleProduct(rec.fin_prdt_cd, rec.option_id, rec.fin_prdt_nm)">
            {{ isJoined(rec.fin_prdt_cd, rec.option_id) ? '가입취소' : '가입하기기' }}
          </button>

        </div>
      </div>
    </div>
  </section>
  <br>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { getBankLongIcon } from '@/utils/bankIconMap'

const props = defineProps({
  recs: {
    type: Array,
    required: true
  }
})

const accountStore = useAccountStore()

const joinedIds = computed(() =>
  accountStore.user?.joined_products?.map(p => p.fin_prdt_cd) || []
)

const isJoined = (productId, optionId) => {
  return accountStore.user?.joined_products?.some(p =>
    p.option?.product === productId && p.option?.id === optionId
  )
}

const toggleProduct = async (productId, optionId, productName) => {
  if (isJoined(productId, optionId)) {
    await accountStore.leaveProduct(productId, optionId, productName)
  } else {
    await accountStore.joinProduct(productId, optionId, productName)
  }
}
</script>


<style scoped>
/* SearchView.vue 의 .video-grid 재사용 */
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}

/* 동영상 카드 스타일을 금융상품 카드로 재정의 */
.prod-card {
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  /* ✅ 여백을 카드 자체에 줍니다 */
}

/* 카드 상단 썸네일(로고) */
.prod-card-thumb {
  width: 100%;
  height: auto;
  aspect-ratio: auto;
  object-fit: contain;
  background: #f7f7f7;
  display: block;
  margin: 0 auto;
  max-height: 120px;
}

/* 카드 내용 */
.prod-card-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.prod-card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.prod-card-meta {
  font-size: 0.85rem;
  color: #555;
  margin-bottom: 0.25rem;
}

.prod-card-desc {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.75rem;
  flex: 1;
  overflow: hidden;
}

.prod-card-btn {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #0074ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.prod-card-btn:hover {
  background-color: #005ecc;
}

.prod-card-btn.joined {
  background-color: #aaa;
}

.prod-card-btn.joined:hover {
  background-color: #797979;
}

.prod-name-link {
  margin-top: 10px;
  font-size: 1.2rem;
  color: #333;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
  max-width: 100%;
  cursor: pointer;
}

.prod-name-link:hover {
  color: #007bff;
  text-decoration: underline;
}

</style>

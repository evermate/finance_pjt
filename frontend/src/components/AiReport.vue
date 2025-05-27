<!-- AiReport.vue -->
<template>
  <section class="ai-report">
    <h2 class="report-title">AI 분석 리포트</h2>
    <div class="report-grid">
      <div v-for="rec in recs" :key="rec.fin_prdt_cd" class="outer-card">
        <div class="product-card">
          <!-- 상단 로고 -->
          <div class="logo-area">
            <img :src="getBankLongIcon(rec.bank.kor_co_nm)" alt="은행 로고" class="bank-logo" />
          </div>

          <!-- 내용 영역 -->
          <div class="info-area">
            <h3 class="product-name">
              <RouterLink :to="`/product/saving/${rec.fin_prdt_cd}`" class="product-link">
                {{ rec.fin_prdt_nm }}
              </RouterLink>
            </h3>
            <p class="product-submeta">{{ rec.bank.kor_co_nm }} · {{ rec.save_trm }}개월 · {{ rec.intr_rate }}%</p>
            <p class="product-desc">{{ rec.reason }}</p>
          </div>

          <!-- 버튼 -->
          <button class="join-btn" :class="{ joined: isJoined(rec.fin_prdt_cd, rec.option_id) }"
            @click="toggleProduct(rec.fin_prdt_cd, rec.option_id, rec.fin_prdt_nm)">
            {{ isJoined(rec.fin_prdt_cd, rec.option_id) ? '가입 취소' : '상품 가입' }}
          </button>
        </div>
      </div>
    </div>
  </section>
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
.ai-report {
  padding: 2rem 1rem;
}

.report-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #000000;
}

.report-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.outer-card {
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  padding: 1rem;
  border-radius: 1.25rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.outer-card:hover {
  transform: translateY(-3px);
}

.product-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* 버튼을 아래로 밀기 */
  height: 100%;
  /* outer-card 전체를 채움 */
  background-color: #ffffff;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.logo-area {
  background-color: #f3f4f6;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  width: 100%;
  border-bottom: 1px solid #e5e7eb;
}

.bank-logo {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.info-area {
  padding: 1rem;
  flex-grow: 1;
  /* 설명 영역이 남는 공간을 채우도록 */
}

.product-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.25rem;
}

.product-submeta {
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.product-desc {
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.45;
}

.join-btn {
  margin: 1rem;
  margin-top: auto;
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
  background-color: #2b66f6;
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.join-btn:hover {
  background-color: #1f4fd4;
}

.join-btn.joined {
  background-color: #ff5858;
}

.join-btn.joined:hover {
  background-color: #e63946;
}

.product-link {
  color: #111827;
  text-decoration: none;
}
.product-link:hover {
  color: #2b66f6;
  text-decoration: underline;
}

</style>

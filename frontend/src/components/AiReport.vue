<template>
  <section class="ai-report mb-10">
    <h2 class="report-title">AI 분석 리포트</h2>
    <div class="card-grid">
      <div v-for="rec in recs" :key="rec.fin_prdt_cd" class="product-card">
        <div class="logo-wrapper">
          <img :src="getBankLongIcon(rec.bank.kor_co_nm)" alt="은행 로고" class="bank-logo" />
        </div>
        <div class="card-body">
          <router-link class="product-name" :to="`/product/${rec.product_type || 'saving'}/${rec.fin_prdt_cd}`"
            :title="rec.fin_prdt_nm">
            {{ rec.fin_prdt_nm }}
          </router-link>
          <ul class="product-meta">
            <li>{{ rec.bank.kor_co_nm }}</li>
            <li>{{ rec.save_trm }}개월</li>
            <li>{{ rec.intr_rate }}%</li>
          </ul>
          <p class="product-desc">{{ rec.reason }}</p>
          <button class="product-button" :class="{ joined: isJoined(rec.fin_prdt_cd, rec.option_id) }"
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
.ai-report {
  padding: 1rem;
}

.report-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #1e293b;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background-color: #fff;
  border-radius: 1.25rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.1);
}

.logo-wrapper {
  width: 100%;
  height: 90px; /* 원하는 높이로 조정 가능 */
  background-color: #f9fafb;
  display: flex;
  justify-content: center;
  align-items: center;
  border-top-left-radius: 1.25rem;
  border-top-right-radius: 1.25rem;
  overflow: hidden;
  margin: -1.5rem -1.5rem 1rem; /* 카드 패딩 상쇄해서 꽉 차게 */
}

.bank-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
}


.card-body {
  flex: 1;
}

.product-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  text-decoration: none;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.product-name:hover {
  color: #2563eb;
}

.product-meta {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 1rem;
  font-size: 0.9rem;
  color: #64748b;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}


.prod-card-btn {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #2b66f6;
  
.product-desc {
  font-size: 0.9rem;
  color: #334155;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.product-button {
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.prod-card-btn:hover {
  background-color: #1f4fd4;
}

.prod-card-btn.joined {
  background-color: #ff5858;
}

.prod-card-btn.joined:hover {
  background-color: #e63946;

.product-button:hover {
  background-color: #1d4ed8;
}

.product-button.joined {
  background-color: #94a3b8;
}

.product-button.joined:hover {
  background-color: #64748b;

}
</style>

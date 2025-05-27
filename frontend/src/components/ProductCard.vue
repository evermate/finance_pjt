<template>
  <div class="prod-card mb-2">
    <img :src="getBankIcon(product.bank.kor_co_nm)" alt="은행 로고" class="prod-logo" />
    <router-link class="prod-name-link" :to="`/product/${product.product_type || 'saving'}/${product.fin_prdt_cd}`"
      :title="product.fin_prdt_nm">
      {{ product.fin_prdt_nm }}
    </router-link>
    <span class="prod-bank">{{ product.bank.kor_co_nm }}</span>
    <span class="prod-term">{{ product.save_trm }}개월</span>
    <span class="prod-rate">{{ product.intr_rate }}%</span>

    <!-- 가입 버튼 -->
    <button class="prod-btn" :class="{ joined: isJoined(product.fin_prdt_cd, product.option_id) }"
      @click="toggleProduct(product.fin_prdt_cd, product.option_id, product.fin_prdt_nm)">
      {{ isJoined(product.fin_prdt_cd, product.option_id) ? '가입 완료' : '상품 가입' }}
    </button>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { getBankIcon } from '@/utils/bankIconMap'

const props = defineProps({
  product: {
    type: Object,
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
.prod-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
  transition: box-shadow 0.2s, transform 0.2s;
}

.prod-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background-color: #f9fafb;
  transform: translateY(-2px);
}

.prod-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  flex-shrink: 0;
}

.prod-bank,
.prod-term,
.prod-rate {
  flex: 1;
  color: #444;
  text-align: center;
}

.prod-btn {
  flex-shrink: 0;
  padding: 0.4rem 0.85rem;
  font-size: 0.85rem;
  border: none;
  background-color: #3182f6;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.prod-btn:hover {
  background-color: #1a73e8;
}

.prod-btn.joined {
  background-color: #cbd5e1;
  color: #374151;
}

.prod-btn.joined:hover {
  background-color: #94a3b8;
}

.prod-name-link {
  color: #1e293b;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
  max-width: 100%;
  flex: 1.5;
}

.prod-name-link:hover {
  color: #2563eb;
  text-decoration: underline;
}


</style>

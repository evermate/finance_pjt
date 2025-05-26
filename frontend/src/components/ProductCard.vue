<!-- ProductCard.vue -->
<template>
  <div class="prod-card mb-2">
    <img :src="getBankIcon(product.bank.kor_co_nm)" alt="은행 로고" class="prod-logo" />
    <span class="prod-name" :title="product.fin_prdt_nm">
      {{ product.fin_prdt_nm }}
    </span>
    <span class="prod-bank">{{ product.bank.kor_co_nm }}</span>
    <span class="prod-term">{{ product.save_trm }}개월</span>
    <span class="prod-rate">{{ product.intr_rate }}%</span>
    <!-- 가입 버튼 -->
    <button class="prod-btn" :class="{ joined: isJoined(product.fin_prdt_cd) }"
      @click="toggleProduct(product.fin_prdt_cd, product.fin_prdt_nm)">
      {{ isJoined(product.fin_prdt_cd) ? '가입 완료' : '상품 가입' }}
    </button>
  </div>
</template>


<script setup>
import { defineProps } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { getBankIcon } from '@/utils/bankIconMap'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const isJoined = (id) => {
  return accountStore.user?.joined_products?.some(p => p.fin_prdt_cd === id)
}

const toggleProduct = async (id, name) => {
  if (isJoined(id)) {
    await accountStore.leaveProduct(id, name)
  } else {
    await accountStore.joinProduct(id, name)
  }
}

const accountStore = useAccountStore()
</script>


<style scoped>
.prod-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.prod-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.prod-name {
  flex: 1.5;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: default;
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
  padding: 0.4rem 0.75rem;
  font-size: 0.85rem;
  border: none;
  background-color: #0074ff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.prod-btn:hover {
  background-color: #005ecc;
}

.prod-btn.joined {
  background-color: #aaa;
  cursor: default;
}
</style>

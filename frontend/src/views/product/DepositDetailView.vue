<template>
  <div v-if="product" class="product-detail">
    <div class="back-button">
      <button @click="goBack">← 목록으로 돌아가기</button>
    </div>

    <h1 class="title">{{ typeLabel }} 상세</h1>

    <div class="info-card">
      <div class="info-grid">
        <div class="label">공시 제출월</div>
        <div class="value">{{ product.dcls_strt_day }}</div>

        <div class="label">금융회사명</div>
        <div class="value">{{ product.bank_name }}</div>

        <div class="label">상품명</div>
        <div class="value">{{ product.fin_prdt_nm }}</div>

        <div class="label">가입 대상</div>
        <div class="value">{{ product.join_member }}</div>

        <div class="label">가입 방법</div>
        <div class="value">{{ product.join_way }}</div>

        <div class="label">우대 조건</div>
        <div class="value">{{ product.spcl_cnd }}</div>
      </div>
    </div>

    <div class="options-card">
      <h2>금리 옵션</h2>
      <table class="options-table">
        <thead>
          <tr>
            <th>기간</th>
            <th>기본금리</th>
            <th>최고금리</th>
            <th>이율유형</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="opt in product.options" :key="opt.id">
            <td>{{ opt.save_trm }}개월</td>
            <td>{{ opt.intr_rate }}%</td>
            <td>{{ opt.intr_rate2 }}%</td>
            <td>{{ opt.intr_rate_type_nm }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="action-section">
      <button
        class="join-btn"
        :class="{ joined: isJoined }"
        @click="toggleJoin"
        :disabled="!isLoggedIn"
      >
        {{ isJoined ? '가입완료' : '가입하기' }}
      </button>
    </div>
  </div>

  <div v-else class="loading">
    <p>상품 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const type = route.params.type
const id = route.params.id
const product = ref(null)

const accountStore = useAccountStore()
const isLoggedIn = computed(() => !!accountStore.user)

const goBack = () => {
  // 브라우저 뒤로가기가 없으면 기본값으로 /compare 이동
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push({ name: 'compare' })
  }
}

const typeLabel = computed(() => {
  return type === 'saving' ? '정기적금' : '정기예금'
})

const isJoined = computed(() => {
  return accountStore.user?.joined_products?.some(p => p.fin_prdt_cd === id)
})

onMounted(async () => {
  try {
    const res = await axios.get(`/api/products/deposits/${id}/`)
    product.value = res.data
  } catch (err) {
    console.error('상품 정보를 불러오지 못했습니다:', err)
  }
})

const toggleJoin = async () => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    if (isJoined.value) {
      await accountStore.leaveProduct(id)
    } else {
      await accountStore.joinProduct(id)
    }
  } catch (err) {
    console.error('가입 상태 변경 실패:', err)
  }
}
</script>

<style scoped>
.product-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.info-card,
.options-card {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.info-grid {
  display: grid;
  grid-template-columns: 150px 1fr;
  row-gap: 1rem;
  column-gap: 1rem;
}

.label {
  font-weight: bold;
  color: #333;
}

.value {
  color: #444;
}

.options-table {
  width: 100%;
  border-collapse: collapse;
}

.options-table th,
.options-table td {
  padding: 0.6rem;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

.options-table th {
  background-color: #f0f4f8;
  font-weight: 600;
}

.action-section {
  text-align: right;
}

.join-btn {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  color: white;
  background-color: #007bff;
}

.join-btn.joined {
  background-color: #aaa;
  cursor: pointer;
}

.join-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.back-button {
  margin-bottom: 1rem;
}

.back-button button {
  background: none;
  border: none;
  color: #007bff;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 500;
  padding: 0;
  transition: color 0.2s;
}

.back-button button:hover {
  text-decoration: underline;
  color: #0056b3;
}

</style>

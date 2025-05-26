<template>
  <div v-if="product" class="product-detail">
    <div class="back-button">
      <button @click="goBack" class="back-link">
        <i class="fas fa-arrow-left"></i>
        <span>이전 페이지로 돌아가기</span>
      </button>
    </div>

    <div class="product-header">
      <h1 class="title">{{ product.fin_prdt_nm }}</h1>
      <p class="subtitle">{{ product.bank_name }} | {{ typeLabel }}</p>
    </div>

    <div class="card detail-card">
      <div class="detail-item" v-for="(value, label) in summaryMap" :key="label">
        <span class="item-label">{{ label }}</span>
        <span class="item-value" v-html="formatValue(label, value)"></span>
      </div>
    </div>

    <div class="card option-card">
      <h2 class="section-title">금리 옵션</h2>
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

    <div class="action-wrapper">
      <button class="join-btn" :class="{ joined: isJoined }" @click="toggleJoin" :disabled="!isLoggedIn">
        {{ isJoined ? '가입완료' : '가입하기' }}
      </button>
      <span v-if="!isLoggedIn" class="tooltip">로그인이 필요합니다</span>
    </div>
  </div>

  <div v-else class="loading">
    <p>상품 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const product = ref(null)
const accountStore = useAccountStore()
const isLoggedIn = computed(() => !!accountStore.user)

const typeLabel = computed(() =>
  route.params.type === 'saving' ? '정기적금' : '정기예금'
)

const isJoined = computed(() =>
  accountStore.user?.joined_products?.some(p => p.fin_prdt_cd === route.params.id)
)

const summaryMap = computed(() => ({
  '공시 제출월': product.value?.dcls_strt_day,
  '금융회사명': product.value?.bank_name,
  '가입 대상': product.value?.join_member,
  '가입 방법': product.value?.join_way,
  '우대 조건': product.value?.spcl_cnd,
}))

const goBack = () => {
  if (window.history.length > 1) router.back()
  else router.push({ name: 'compare' })
}

const fetchProductDetail = async (id) => {
  try {
    const res = await axios.get(`/api/products/deposits/${id}/`)
    product.value = res.data
  } catch (err) {
    console.error('상품 정보를 불러오지 못했습니다:', err)
  }
}

onMounted(() => fetchProductDetail(route.params.id))

watch(() => route.params.id, (newId, oldId) => {
  if (newId !== oldId) fetchProductDetail(newId)
})

const toggleJoin = async () => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const optionId = product.value.options[0]?.id
    const productId = route.params.id
    const productName = product.value.fin_prdt_nm

    if (isJoined.value) {
      await accountStore.leaveProduct(productId, optionId, productName)
    } else {
      await accountStore.joinProduct(productId, optionId, productName)
    }
  } catch (err) {
    console.error('가입 상태 변경 실패:', err)
  }
}

const formatValue = (label, value) => {
  if (label === '우대 조건') {
    const bolded = value.replace(/(\d+\)?[^\n]+)/g, '<strong>$1</strong>')
    return bolded.replace(/\n/g, '<br>')
  }
  return value
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.product-detail {
  max-width: 768px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Noto Sans KR', sans-serif;
}

.back-button {
  margin-bottom: 1.5rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  color: #2b66f6;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: color 0.2s;
}

.back-link:hover {
  color: #1a4dcc;
  text-decoration: underline;
}

.back-link i {
  font-size: 1rem;
}

.product-header {
  margin-bottom: 1.5rem;
}

.title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #212529;
}

.subtitle {
  font-size: 0.95rem;
  color: #868e96;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f1f3f5;
  font-size: 0.95rem;
}

.item-label {
  font-weight: 400;
  color: #495057;
  white-space: nowrap;
}

.item-value {
  text-align: right;
  color: #343a40;
  max-width: 70%;
  font-weight: 600;
  line-height: 1.6;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #212529;
}

.options-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.options-table th,
.options-table td {
  text-align: center;
  padding: 0.6rem;
  border-bottom: 1px solid #dee2e6;
}

.options-table th {
  background-color: #f8f9fa;
  color: #495057;
  font-weight: 600;
}

.action-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}

.join-btn {
  background-color: #2b66f6;
  color: white;
  padding: 0.6rem 1.4rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.join-btn:hover {
  background-color: #1f4fd4;
}

.join-btn.joined {
  background-color: #adb5bd;
  cursor: default;
}

.tooltip {
  font-size: 0.8rem;
  color: #868e96;
}
</style>

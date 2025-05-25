<template>
  <section class="compare-container">
    <!-- 헤더 및 탭 -->
    <div class="compare-header">
      <h1>{{ selectedType === 'saving' ? '정기적금' : '정기예금' }} 비교</h1>
      <div class="type-tabs">
        <button :class="{ active: selectedType === 'saving' }" @click="changeType('saving')">정기적금</button>
        <button :class="{ active: selectedType === 'deposit' }" @click="changeType('deposit')">정기예금</button>
      </div>
    </div>

    <!-- 📌 필터 + 테이블을 나란히 배치 -->
    <div class="compare-body">
      <!-- 왼쪽: 필터 -->
      <div class="filter-section">
        <h4>금융회사</h4>
        <select v-model="selectedBank" class="bank-select">
          <option value="전체">전체</option>
          <option v-for="bank in bankList" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
        <h4>기간</h4>
        <select v-model="selectedTerm" class="term-select" @change="fetchSortedProducts(selectedTerm)">
          <option v-for="term in ['6', '12', '24', '36']" :key="term" :value="term">
            {{ term }}개월
          </option>
        </select>


        <!-- 가입한 상품 목록 -->
        <!-- 이부분은 MyProductsPanel 버튼이 대체하였습니다 -->
        <!-- <div class="joined-products" v-if="isLoggedIn && accountStore.user?.joined_products?.length">
          <h4>가입한 상품</h4>
          <div class="joined-grid">
            <div class="joined-card" v-for="item in accountStore.user.joined_products" :key="item.fin_prdt_cd">
              <div class="card-title">{{ item.fin_prdt_nm }}</div>
              <div class="card-subtitle">{{ item.bank_name }}</div>
              <button class="leave-icon" @click="leaveProduct(item.fin_prdt_cd)">✕</button>
            </div>
          </div>
        </div> -->

      </div>
      <!-- 필터 섹션 끝 -->



      <!-- 오른쪽: 테이블 -->
      <div class="table-wrapper">
        <table class="rate-table">
          <thead>
            <tr>
              <th>공시월</th>
              <th>금융회사</th>
              <th>상품명</th>
              <th v-for="term in ['6', '12', '24', '36']" :key="term" @click="fetchSortedProducts(term)"
                :class="{ clickable: true, active: selectedTerm === term }">
                {{ term }}개월
                <span class="sort-icon">
                  <template v-if="selectedTerm === term">▼</template>
                  <template v-else>▽</template>
                </span>
              </th>
              <!-- ✅ 버튼 칼럼 헤더 -->
              <th>가입</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd"
              :class="{ 'joined-row': isJoined(product.fin_prdt_cd) }">
              <td>{{ product.dcls_strt_day }}</td>
              <td>{{ product.bank_name }}</td>

              <td :title="product.fin_prdt_nm">
                <router-link class="product-link" :to="`/product/${selectedType}/${product.fin_prdt_cd}`">
                  {{ product.fin_prdt_nm }}
                </router-link>
              </td>


              <td v-for="(term, idx) in termList" :key="term" :class="getCellClass(idx)">
                {{ getRate(product.options, term) }}
              </td>
              <!-- 가입 버튼 열 -->
              <td>
                <template v-if="isLoggedIn">
                  <button @click="toggleProduct(product.fin_prdt_cd)"
                    :class="['join-btn', { joined: isJoined(product.fin_prdt_cd) }]">
                    {{ isJoined(product.fin_prdt_cd) ? '가입완료' : '가입하기' }}
                  </button>

                </template>
                <template v-else>
                  <span class="login-required">로그인 필요</span>
                </template>
              </td>

              <!-- <td :class="getCellClass('6')">{{ getRate(product.options, '6') }}</td>
              <td :class="getCellClass('12')">{{ getRate(product.options, '12') }}</td>
              <td :class="getCellClass('24')">{{ getRate(product.options, '24') }}</td>
              <td :class="getCellClass('36')">{{ getRate(product.options, '36') }}</td> -->
            </tr>
          </tbody>

        </table>
      </div>
    </div>
  </section>


</template>


<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const API_BASE_URL = 'http://127.0.0.1:8000/api/products/deposits/sorted/'
const products = ref([])
const selectedTerm = ref('6')
const selectedType = ref(route.query.type || 'saving')
const selectedBank = ref('전체')
const termList = ['6', '12', '24', '36']


// 상품 가입
const accountStore = useAccountStore()
const isLoggedIn = computed(() => !!accountStore.user)

// 유저가 가입한 상품 목록
const joinedIds = computed(() => {
  return accountStore.user?.joined_products?.map(p => p.fin_prdt_cd) || []
})

const joinProduct = (id) => {
  accountStore.joinProduct(id)
}

const isJoined = (id) => joinedIds.value.includes(id)

const leaveProduct = async (id) => {
  await accountStore.leaveProduct(id)
}

const toggleProduct = async (id) => {
  if (isJoined(id)) {
    await accountStore.leaveProduct(id)
  } else {
    await accountStore.joinProduct(id)
  }
}

const fetchSortedProducts = async (term = selectedTerm.value) => {
  selectedTerm.value = term
  try {
    const params = new URLSearchParams({
      type: selectedType.value,
      term: term
    })
    const res = await axios.get(`${API_BASE_URL}?${params.toString()}`)
    products.value = res.data ?? []
  } catch (err) {
    console.error('불러오기 실패:', err)
    products.value = []
  }
}

const changeType = async (type) => {
  selectedType.value = type
  await fetchSortedProducts(selectedTerm.value)
  selectedBank.value = '전체'

  // ✅ URL 쿼리 업데이트 (뒤로가기/새로고침 대응)
  router.replace({
    query: {
      ...route.query,
      type,
    },
  })
}


onMounted(() => {
  fetchSortedProducts()
})

const getRate = (options, term) => {
  if (!Array.isArray(options)) return '-'
  const opt = options.find(o => o.save_trm === term)
  return opt?.intr_rate !== null && opt?.intr_rate !== undefined ? `${opt.intr_rate}%` : '-'
}

const bankList = computed(() => {
  const banks = products.value.map(p => p.bank_name)
  return [...new Set(banks)]
})

const filteredProducts = computed(() => {
  if (selectedBank.value === '전체') return products.value
  return products.value.filter(p => p.bank_name === selectedBank.value)
})

const getCellClass = (idx) => {
  return idx === selectedTermIndex.value ? 'highlighted' : 'dimmed'
}

const selectedTermIndex = computed(() => termList.indexOf(selectedTerm.value))

watch(joinedIds, (val) => {
  console.log('🔄 joinedIds 변경됨:', val)
})
</script>

<style scoped>
.compare-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
}

.left-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bank-select {
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 200px;
}

.term-select {
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 200px;
}

.type-tabs {
  display: flex;
  gap: 0.5rem;
}

.type-tabs button {
  padding: 0.3rem 0.8rem;
  border: 1px solid #ccc;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.type-tabs button.active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.rate-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  table-layout: fixed;
  margin-top: 1rem;
}

.rate-table th,
.rate-table td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rate-table th:nth-child(1),
.rate-table td:nth-child(1) {
  width: 100px;
}

.rate-table th:nth-child(2),
.rate-table td:nth-child(2) {
  width: 150px;
}

.rate-table th:nth-child(3),
.rate-table td:nth-child(3) {
  width: 250px;
}

.rate-table th:nth-child(n+4),
.rate-table td:nth-child(n+4) {
  width: 80px;
}

.rate-table th {
  background-color: #f2f6fa;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #ddd;
  transition: background-color 0.3s, color 0.3s;
  font-size: 0.95rem;
}

.rate-table th.clickable {
  cursor: pointer;
}

.rate-table th.active {
  background-color: #007bff;
  color: white;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.compare-body {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
}

.filter-section {
  width: 250px;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filter-section h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.3rem;
}

.bank-select,
.term-select {
  padding: 0.6rem 0.8rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  background-color: #f9fafb;
  width: 100%;
  transition: border-color 0.3s ease;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.bank-select:focus,
.term-select:focus {
  outline: none;
  border-color: #007bff;
  background-color: #ffffff;
}

.table-wrapper {
  flex: 1;
  overflow-x: auto;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  padding: 1rem;
}

.rate-table td {
  font-size: 0.95rem;
  color: #222;
}

.rate-table td:empty::before {
  content: '-';
  color: #aaa;
}

.rate-table td {
  font-weight: 500;
}

.rate-table td:nth-child(n+4) {
  font-size: 1.05rem;
  font-weight: bold;
  color: #007bff;
}

.rate-table tbody tr:hover {
  background-color: #f0f8ff;
  transition: background-color 0.2s;
}

/* 연한 색상 (선택 안 된 기간용) */
.rate-table td.dimmed {
  color: #bbb;
  font-weight: normal;
}

/* 강조 색상 (선택된 기간용) */
.rate-table td.highlighted {
  color: #df2e5a;
  font-weight: bold;
  border-left: 2px solid #007bff;
  border-right: 2px solid #007bff;
  background-color: #fffafc;
  box-shadow: inset 2px 0 0 #007bff, inset -2px 0 0 #007bff;
}

/* 선택된 열의 테두리 강조 */
.rate-table td.highlighted {
  border-left: 2px solid #007bff;
  border-right: 2px solid #007bff;
  background-color: #fffdfd;
}

.join-btn {
  padding: 0.3rem 0.6rem;
  background-color: #007bff;
  color: white;
  font-size: 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.join-btn.joined {
  background-color: #aaa;
  color: #fff;
}

.join-btn:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

/* 가입 완료된 행 강조 */
.joined-row {
  background-color: #f5f8fb;
}

/* 로그인 안내 텍스트 */
.login-required {
  font-size: 0.8rem;
  color: #999;
}

.joined-products {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.joined-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.joined-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.4rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.joined-name {
  font-size: 0.9rem;
  color: #333;
}

.leave-btn {
  background: none;
  border: none;
  color: #dc3545;
  font-size: 1rem;
  cursor: pointer;
}

.joined-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.joined-card {
  position: relative;
  background: #f9f9f9;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s;
}

.joined-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.card-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 0.4rem;
  font-size: 0.95rem;
}

.card-subtitle {
  font-size: 0.85rem;
  color: #666;
}

.leave-icon {
  position: absolute;
  top: 8px;
  right: 10px;
  background: none;
  border: none;
  color: #dc3545;
  font-size: 1rem;
  cursor: pointer;
}

.product-link {
  color: #333;             /* 일반 텍스트 색상 */
  text-decoration: none;   /* 밑줄 제거 */
  font-weight: 500;
  transition: color 0.2s;
}

.product-link:hover {
  color: #007bff;          /* 마우스 호버 시 파란색 강조 */
  text-decoration: underline; /* 선택적으로 호버시만 밑줄 */
}

</style>

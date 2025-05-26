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
        <button class="reset-btn" @click="resetFilters">카테고리 초기화</button>
        <h4>금융회사</h4>
        <select v-model="selectedBank" class="bank-select" @change="updateQuery">
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
                  <!-- 가입 버튼 -->
                  <button @click="toggleProduct(product.fin_prdt_cd, product.fin_prdt_nm, product.options)"
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
const selectedType = ref(route.query.type || 'saving')
const selectedBank = ref(route.query.bank || '전체')
const selectedTerm = ref(route.query.term || '6')
const termList = ['6', '12', '24', '36']


// 상품 가입
const accountStore = useAccountStore()
const isLoggedIn = computed(() => !!accountStore.user)

// 유저가 가입한 상품 목록
const joinedIds = computed(() => {
  return accountStore.user?.joined_products?.map(p => p.option.product) || []
})


const joinProduct = (id, name) => {
  accountStore.joinProduct(id, name)
}

const isJoined = (id) => joinedIds.value.includes(id)

const leaveProduct = async (id, name) => {
  await accountStore.leaveProduct(id, name)
}

const toggleProduct = async (productId, productName, options) => {
  const term = selectedTerm.value
  const matchedOption = options.find(opt => opt.save_trm === term)
  if (!matchedOption) {
    alert(`${term}개월 옵션이 존재하지 않습니다.`)
    return
  }

  const optionId = matchedOption.id

  if (isJoined(productId)) {
    await accountStore.leaveProduct(productId, optionId, productName)  // ✅ productId + optionId
  } else {
    await accountStore.joinProduct(productId, optionId, productName)
  }
}

const fetchSortedProducts = async (term = selectedTerm.value) => {
  selectedTerm.value = term

  try {
    const params = new URLSearchParams({
      type: selectedType.value,
      term,
    })

    const res = await axios.get(`${API_BASE_URL}?${params.toString()}`)
    products.value = res.data ?? []

    // ✅ URL 쿼리 반영
    router.replace({
      query: {
        ...route.query,
        type: selectedType.value,
        bank: selectedBank.value,
        term: term,
      }
    })
  } catch (err) {
    console.error('불러오기 실패:', err)
    products.value = []
  }
}

const changeType = async (type) => {
  selectedType.value = type
  selectedBank.value = '전체'  // 탭 바꾸면 은행 필터 초기화
  await fetchSortedProducts(selectedTerm.value)

  router.replace({
    query: {
      ...route.query,
      type,
      bank: selectedBank.value,
      term: selectedTerm.value,
    },
  })
}

const updateQuery = () => {
  router.replace({
    query: {
      ...route.query,
      type: selectedType.value,
      bank: selectedBank.value,
      term: selectedTerm.value,
    }
  })
}

const resetFilters = async () => {
  selectedType.value = 'saving'
  selectedBank.value = '전체'
  selectedTerm.value = '6'
  await fetchSortedProducts('6')

  router.replace({
    query: {
      type: 'saving',
      bank: '전체',
      term: '6'
    }
  })
}

onMounted(() => {
  fetchSortedProducts()
})

const getRate = (options, term) => {
  if (!Array.isArray(options)) return '-'
  const opt = options.find(o => o.save_trm === term)
  return opt?.intr_rate2 !== null && opt?.intr_rate2 !== undefined ? `${opt.intr_rate2}%` : '-'
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
  flex-direction: column;
  align-items: flex-start;
  gap: 0.8rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.compare-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #212529;
  letter-spacing: -0.02em;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.compare-header h1::before {
  content: "💰";
  font-size: 1.6rem;
  line-height: 1;
}

.type-tabs {
  display: flex;
  gap: 0.5rem;
}

.type-tabs button {
  padding: 0.5rem 1.2rem;
  font-size: 0.95rem;
  font-weight: 500;
  border: 1px solid #d0d7de;
  border-radius: 9999px; /* pill 형태 */
  background-color: #ffffff;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
}


.type-tabs button.active {
  background-color: #007bff;
  color: #ffffff;
  border: 1px solid #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25); /* 포커스 느낌 */
  font-weight: 600;
}
.type-tabs button:hover {
  background-color: #f1f3f5;
  color: #212529;
}
.type-tabs button.active:hover {
  background-color: #0069d9;
  border-color: #0062cc;
}
.type-tabs button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.35);
}
.type-tabs button:disabled {
  background-color: #e9ecef;
  color: #adb5bd;
  cursor: not-allowed;
  border-color: #dee2e6;
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

/* 📊 테이블 전체 */
.rate-table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0 0.75rem;
  table-layout: fixed;
  font-size: 0.95rem;
}

/* 📌 헤더 셀 */
.rate-table thead th {
  background-color: #f8f9fa;
  color: #343a40;
  font-weight: 600;
  padding: 0.9rem 0.5rem;
  text-align: center;
  border-bottom: 2px solid #dee2e6;
  font-size: 0.95rem;
  white-space: nowrap;
}
/* 📄 행 */
.rate-table tbody tr {
  background-color: #ffffff;
  border-radius: 12px;
  border-bottom: 1px solid #e9ecef;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  transition: background-color 0.2s ease;
}

/* 🖱️ 행 hover 효과 */
.rate-table tbody tr:hover {
  background-color: #f8f9fa;
}

/* 🔢 셀 */
.rate-table td {
  padding: 0.75rem;
  text-align: center;
  font-size: 0.95rem;
  color: #212529;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
  font-size: 0.95rem;
  color: #495057;
  margin-bottom: 0.4rem;
  font-weight: 600;
  letter-spacing: -0.3px;
}


.bank-select,
.term-select {
  width: 100%;
  appearance: none;
  padding: 0.65rem 0.8rem;
  font-size: 0.95rem;
  border-radius: 10px;
  border: 1px solid #ced4da;
  background-color: #f8f9fa;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: border-color 0.3s ease, background-color 0.3s ease;
  background-image: url('data:image/svg+xml;charset=UTF-8,<svg fill="gray" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414L10 13.414l-4.707-4.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>');
  background-repeat: no-repeat;
  background-position: right 0.8rem center;
  background-size: 1rem;
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

/* 🔢 셀 */
.rate-table td {
  padding: 0.75rem;
  text-align: center;
  font-size: 0.95rem;
  color: #212529;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rate-table td:empty::before {
  content: '-';
  color: #ccc;
}

.rate-table td {
  font-weight: 500;
}

/* 📈 금리 강조 셀 */
.rate-table td:nth-child(n+4):not(:last-child) {
  font-size: 1.05rem;
  font-weight: 600;
  color: #2b66f6;
}

.rate-table tbody tr:hover {
  background-color: #f0f8ff;
  transition: background-color 0.2s;
}

/* 연한 색상 (선택 안 된 기간용) */
.rate-table td.dimmed {
  color: #adb5bd;
  font-weight: normal;
}
/* 📌 선택된 열 강조 */
.rate-table td.highlighted {
  background-color: #ffe0e0;  /* ✅ 더 진한 분홍/다홍색 */
  color: #c92a2a;
  font-weight: 700;
  border-left: 2px solid #fa5252;
  border-right: 2px solid #fa5252;
}


/* 선택된 열의 테두리 강조 */
.rate-table td.highlighted {
  border-left: 0.5px solid #007bff;
  border-right: 0.5px solid #007bff;
  background-color: #fff1f0;
}
.rate-table tbody tr:last-child td.highlighted {
  border-bottom: 0.5px solid #007bff;
}

/* ✅ 가입 버튼 */
.join-btn {
  display: inline-block;
  padding: 0.45rem 1rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: white;
  background-color: #2b66f6;
  border: none;
  border-radius: 6px;
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.join-btn:hover {
  background-color: #1f4fd4;
}

.join-btn.joined {
  background-color: #adb5bd;
  color: white;
  cursor: default;
}

.join-btn:disabled {
  background-color: #dee2e6;
  color: #adb5bd;
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
  color: #333;
  /* 일반 텍스트 색상 */
  text-decoration: none;
  /* 밑줄 제거 */
  font-weight: 500;
  transition: color 0.2s;
}

.product-link:hover {
  color: #007bff;
  /* 마우스 호버 시 파란색 강조 */
  text-decoration: underline;
  /* 선택적으로 호버시만 밑줄 */
}

.reset-btn {
  width: 100%;  /* ✅ 셀렉트 박스와 통일 */
  padding: 0.65rem 1rem;
  background-color: #f1f3f5;
  border: 1px solid #ced4da;
  color: #495057;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}


.reset-btn:hover {
  background-color: #e9ecef;
  color: #212529;
  border-color: #adb5bd;
}

</style>

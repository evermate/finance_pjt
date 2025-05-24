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
          <option
            v-for="bank in bankList"
            :key="bank"
            :value="bank"
          >
            {{ bank }}
          </option>
        </select>
      </div>

      <!-- 오른쪽: 테이블 -->
      <div class="table-wrapper">
        <table class="rate-table">
          <thead>
            <tr>
              <th>공시월</th>
              <th>금융회사</th>
              <th>상품명</th>
              <th
                v-for="term in ['6', '12', '24', '36']"
                :key="term"
                @click="fetchSortedProducts(term)"
                :class="{ clickable: true, active: selectedTerm === term }"
              >
                {{ term }}개월
                <span class="sort-icon">
                  <template v-if="selectedTerm === term">▼</template>
                  <template v-else>▽</template>
                </span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd">
              <td>{{ product.dcls_strt_day }}</td>
              <td>{{ product.bank_name }}</td>
              <td :title="product.fin_prdt_nm">{{ product.fin_prdt_nm }}</td>
              <td>{{ getRate(product.options, '6') }}</td>
              <td>{{ getRate(product.options, '12') }}</td>
              <td>{{ getRate(product.options, '24') }}</td>
              <td>{{ getRate(product.options, '36') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api/products/deposits/sorted/'
const products = ref([])
const selectedTerm = ref('6')
const selectedType = ref('saving')
const selectedBank = ref('전체')

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
  background-color: #f3f3f3;
  user-select: none;
}

.rate-table th.clickable {
  cursor: pointer;
}

.rate-table th.active {
  background-color: #007bff;
  color: white;
}
.compare-body {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
}

.filter-section {
  min-width: 200px;
}

.table-wrapper {
  flex: 1;
  overflow-x: auto;
}

</style>

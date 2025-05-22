<template>
  <section>
    <div class="compare-header">
      <h1>{{ selectedType === 'saving' ? '정기적금' : '정기예금' }} 비교</h1>
      <div class="type-tabs">
        <button
          :class="{ active: selectedType === 'saving' }"
          @click="changeType('saving')"
        >정기적금</button>
        <button
          :class="{ active: selectedType === 'deposit' }"
          @click="changeType('deposit')"
        >정기예금</button>
      </div>
    </div>

    <div class="term-buttons">
      <button
        v-for="term in ['6', '12', '24', '36']"
        :key="term"
        :class="{ active: selectedTerm === term }"
        @click="fetchSortedProducts(term)"
      >
        {{ term }}개월
      </button>
    </div>

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
        <tr v-for="product in products" :key="product.fin_prdt_cd">
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
  </section>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api/products/deposits/sorted/'
const products = ref([])
const selectedTerm = ref('6')
const selectedType = ref('saving')  // 'saving' | 'deposit'

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
}

onMounted(() => {
  fetchSortedProducts()
})

const getRate = (options, term) => {
  if (!Array.isArray(options)) return '-'
  const opt = options.find(o => o.save_trm === term)
  return opt?.intr_rate !== null && opt?.intr_rate !== undefined ? `${opt.intr_rate}%` : '-'
}
</script>

<style scoped>
.compare-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
}

.type-tabs button.active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.term-buttons {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
}

.term-buttons button {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ccc;
  background: white;
  cursor: pointer;
}

.term-buttons button.active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.rate-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  table-layout: fixed;
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

</style>

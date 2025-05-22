<template>
  <section>
    <h1>정기적금 비교</h1>

    <!-- 🔹 정렬 버튼 -->
    <div class="term-buttons">
      <button
        v-for="term in ['6', '12', '24', '36']"
        :key="term"
        :class="{ active: selectedTerm === term }"
        @click="selectedTerm = term"
      >
        {{ term }}개월
      </button>
    </div>

    <!-- 🔹 금리 비교 테이블 -->
    <table class="rate-table">
      <thead>
        <tr>
          <th>공시월</th>
          <th>금융회사</th>
          <th>상품명</th>
          <th
            v-for="term in ['6', '12', '24', '36']"
            :key="term"
            @click="selectedTerm = term"
            :class="{ clickable: true, active: selectedTerm === term }"
          >
            {{ term }}개월
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in sortedProducts" :key="product.fin_prdt_cd">
          <td>{{ product.dcls_strt_day }}</td>
          <td>{{ product.bank.kor_co_nm }}</td>
          <td>{{ product.fin_prdt_nm }}</td>
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
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/products/deposits/'
const products = ref([])
const selectedTerm = ref('6')  // 초기 정렬 기준

onMounted(async () => {
  try {
    const res = await axios.get(API_URL)
    products.value = res.data
  } catch (err) {
    console.error('불러오기 실패:', err)
  }
})

const getRate = (options, term) => {
  const opt = options.find(o => o.save_trm === term)
  return opt?.intr_rate !== null && opt?.intr_rate !== undefined ? `${opt.intr_rate}%` : '-'
}

const sortedProducts = computed(() => {
  const term = selectedTerm.value
  return [...products.value]
    .filter(p => p.options.some(opt => opt.save_trm === term && opt.intr_rate !== null))
    .sort((a, b) => {
      const aRate = a.options.find(opt => opt.save_trm === term)?.intr_rate || 0
      const bRate = b.options.find(opt => opt.save_trm === term)?.intr_rate || 0
      return bRate - aRate
    })
})
</script>

<style scoped>
.term-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
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
}

.rate-table th,
.rate-table td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: center;
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

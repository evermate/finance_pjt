<template>
  <div class="page">
    <!-- ✅ 상단 배너 추가 -->
    <div class="banner-section">
      <img src="/image/goldbar.jpg" alt="골드바" class="banner-img" />
      <div class="banner-text">
        <h2>현물 상품 시세 비교</h2>
        <p>금과 은의 시세를 날짜별로 확인해보세요</p>
      </div>
    </div>

    <div class="container">
      <section class="summary-card">
        <div class="summary-box">
          <h3>{{ selectedMetal === 'gold' ? '금' : '은' }} 가격</h3>
          <p class="price" :style="priceColorStyle">
            ${{ latestPrice }}
            <span class="date">({{ latestDate }})</span>
          </p>
        </div>
      </section>
      <div class="controls">
        <button @click="selectMetal('gold')" :class="['gold', { active: selectedMetal === 'gold' }]">금</button>
        <button @click="selectMetal('silver')" :class="['silver', { active: selectedMetal === 'silver' }]">은</button>
        <input type="date" v-model="startDate" /> ~
        <input type="date" v-model="endDate" />
      </div>
      <canvas
        v-if="filteredData.length > 0"
        :key="chartKey"
        id="priceChart">
      </canvas>
      <div v-else class="no-data">
        <img src="/image/no-data.jpg" alt="데이터 없음" class="no-data-img" />
        <p>선택한 조건에 해당하는 데이터가 없습니다.</p>
      </div>

      <!-- 데이터 요약 테이블 -->
      <div class="table-summary" v-if="filteredData.length">
        <table>
          <tbody>
            <!-- <tr><th>전일 종가</th><td>{{ filteredData[0]['Close/Last'] }}</td></tr> -->
            <tr><th>최신 가격</th><td>{{ filteredData.at(-1)['Close/Last'] }}</td></tr>
            <tr><th>최고가</th><td>{{ maxPrice }}</td></tr>
            <tr><th>최저가</th><td>{{ minPrice }}</td></tr>
            <tr><th>데이터 개수</th><td>{{ filteredData.length }}</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import goldData from '@/excel/Gold_prices.json'
import silverData from '@/excel/Silver_prices.json'

const selectedMetal = ref('gold')
const startDate = ref('2023-01-01')
const today = new Date().toISOString().split('T')[0]
const endDate = ref(today)
const chartKey= ref(0)
let chartInstance = null

const priceColorStyle = computed(() => ({
  color: selectedMetal.value === 'gold' ? '#DAA520' : '#6e7d88'
}))

const getFilteredData = (data) => {
  const start = new Date(startDate.value)
  const end = new Date(endDate.value)
  return data.filter(item => {
    const itemDate = new Date(item.date)
    return itemDate >= start && itemDate <= end
  })
}

const drawChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }
  const data = selectedMetal.value === 'gold' ? goldData : silverData
  const ctx = document.getElementById('priceChart')
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: filteredData.value.map(item => `${item.date.slice(0, 4)}${item.date.slice(4, 6)}${item.date.slice(6)}`),
      datasets: [{
        label: selectedMetal.value === 'gold' ? '금 시세' : '은 시세',
        data: filteredData.value.map(item => Number(item["Close/Last"].replace(',', ''))),
        borderColor: selectedMetal.value === 'gold' ? '#FFD700' : '#C0C0C0',
        backgroundColor: selectedMetal.value === 'gold' ? 'rgba(255, 215, 0, 0.2)' : 'rgba(192, 192, 192, 0.2)',
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: { title: { display: true, text: '날짜' }, ticks: { maxRotation: 45, minRotation: 45 } },
        y: { title: { display: true, text: '가격 (USD/oz)' }, beginAtZero: false }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: context => `가격: $${context.parsed.y}`
          }
        }
      }
    }
  })
}

const selectMetal = (type) => {
  selectedMetal.value = type
}

const filteredData = computed(() => {
  const data = selectedMetal.value === 'gold' ? goldData : silverData
  return getFilteredData(data)
})

const latestPrice = computed(() => {
  const last = filteredData.value.at(-1)
  return last ? last["Close/Last"] : '-'
})

const latestDate = computed(() => {
  const last = filteredData.value.at(-1)
  return last ? `${last.date.slice(0, 4)}${last.date.slice(4, 6)}${last.date.slice(6)}` : '-'
})

const maxPrice = computed(() => {
  return Math.max(...filteredData.value.map(item => Number(item["Close/Last"].replace(',', '')))).toFixed(2)
})

const minPrice = computed(() => {
  return Math.min(...filteredData.value.map(item => Number(item["Close/Last"].replace(',', '')))).toFixed(2)
})

watch([selectedMetal, startDate, endDate], () => {
  chartKey.value++
  nextTick(() => {
    if (filteredData.value.length > 0) {
      drawChart()
    }
  })
})
onMounted(drawChart)
</script>

<style scoped>
.page {
  background-color: #f8f9fc;
  font-family: 'Pretendard', sans-serif;
}

.hero {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(to right, #2f80ed, #56ccf2);
  color: white;
}

.hero h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.hero p {
  font-size: 1.1rem;
  font-weight: 300;
}

.summary-card {
  max-width: 960px;
  margin: 2rem auto 1rem;
  padding: 1.5rem 2rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.summary-box h3 {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.6rem;
  color: #111;
}

.summary-box .price {
  font-size: 2.5rem;
  font-weight: 700;
}

.summary-box .date {
  font-size: 1rem;
  font-weight: 400;
  color: #888888;
  margin-left: 0.6rem;
}

.container {
  max-width: 960px;
  margin: 2rem auto;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.controls button {
  padding: 0.5rem 1.2rem;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s;
}

.controls button.active.gold {
  background-color: #ffd700;
  color: white;
  border-color: #ffd700;
}

.controls button.active.silver {
  background-color: #c0c0c0;
  color: white;
  border-color: #c0c0c0;
}

.controls input[type="date"] {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.9rem;
}

.table-summary {
  margin-top: 2rem;
}

.table-summary table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.table-summary th, .table-summary td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
}
.title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
}
.subtitle {
  font-size: 0.95rem;
  color: #f0eeee;
  margin-bottom: 2rem;
}
canvas {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1rem;
}
.no-data {
  text-align: center;
  padding: 3rem 1rem;
  font-size: 1.1rem;
  color: #666;
  animation: fadeIn 0.5s ease-in-out;
}
.no-data-img {
  width: 360px;
  margin-bottom: 1rem;
  opacity: 0.8;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.banner-section {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.banner-img {
  width: 100%;
  height: 350%;
  object-fit: cover;
  filter: brightness(0.6);
}

.banner-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 2;
}

.banner-text h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.banner-text p {
  font-size: 1.1rem;
  font-weight: 400;
}
</style>

<!-- src/views/SimulationView.vue -->
<template>
  <section class="simulation">
    <!-- 헤더 배너 -->
    <div class="simulation-header">
      <h1>은퇴 자산 시뮬레이션</h1>
      <p>나만의 은퇴 계획을 미리 확인해보세요</p>
    </div>

    <!-- 입력 폼 카드 -->
    <div class="simulation-form-card">
      <h2>시뮬레이션 파라미터 입력</h2>
      <SimulationForm />
    </div>

    <!-- 10년 단위 예상 자산 카드 그리드 -->
    <div v-if="decadeSummary.length" class="cards">
      <div
        v-for="item in decadeSummary"
        :key="item.age"
        class="card"
      >
        <div class="badge">{{ item.age }}세</div>
        <p class="amount">{{ formatNumber(item.asset) }}원</p>
        <p class="unit">{{ toKoreanUnit(item.asset) }}</p>
      </div>
    </div>

    <!-- 차트 -->
    <div v-if="store.data" class="chart-wrapper">
      <SimulationChart :results="store.data" />
    </div>

    <!-- 에러 -->
    <p v-if="store.error" class="error">{{ store.error.message }}</p>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import SimulationForm  from '@/components/SimulationForm.vue'
import SimulationChart from '@/components/SimulationChart.vue'
import { useSimulationStore } from '@/stores/simulation.js'

const store = useSimulationStore()

// 10년 단위 요약 계산
const decadeSummary = computed(() => {
  if (!store.data) return []
  const { age, median_assets } = store.data
  const firstDecade = Math.ceil(age[0] / 10) * 10
  return age
    .map((a, i) => ({ age: a, asset: median_assets[i] }))
    .filter(item => item.age >= firstDecade && item.age % 10 === 0)
})

// 숫자 천 단위 콤마
function formatNumber(x) {
  return x.toLocaleString('ko-KR', { maximumFractionDigits: 0 })
}

// 억/조/경/만 단위 변환 (띄어쓰기 포함)
function toKoreanUnit(x) {
  const val = BigInt(Math.floor(x))
  const GYEONG = 10n ** 16n
  const JO     = 10n ** 12n
  const EOK    = 10n ** 8n
  const MAN    = 10n ** 4n

  let rest = val
  const gyeong    = rest / GYEONG; rest %= GYEONG
  const jo        = rest / JO;     rest %= JO
  const eok       = rest / EOK;    rest %= EOK
  const man       = rest / MAN;    rest %= MAN
  const remainder = rest

  const parts = []
  if (gyeong   > 0n) parts.push(`${gyeong}경`)
  if (jo       > 0n) parts.push(`${jo}조`)
  if (eok      > 0n) parts.push(`${eok}억`)
  if (man      > 0n) parts.push(`${man}만`)
  if (remainder> 0n) parts.push(`${remainder}`)

  return parts.join(' ') + '원'
}
</script>

<style scoped>
/* 전체 섹션 배경 & 패딩 */
.simulation {
  background: #f0f4f8;
  padding: 2rem 1rem;
}

/* 헤더 배너 */
.simulation-header {
  max-width: 600px;
  margin: 0 auto 2rem;
  text-align: center;
}
.simulation-header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1e3a8a;
  letter-spacing: 0.5px;
}
.simulation-header p {
  margin-top: 0.5rem;
  color: #475569;
  font-size: 1.125rem;
}

/* 입력 폼 카드 */
.simulation-form-card {
  max-width: 720px;
  margin: 0 auto 3rem;
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.simulation-form-card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 1rem;
}

/* 카드 그리드 */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

/* 카드 기본 스타일 */
.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: box-shadow .2s, transform .2s;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

/* 나이 배지 */
.badge {
  display: inline-block;
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

/* 금액 텍스트 */
.amount {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0.5rem 0;
}

/* 한글 단위 텍스트 */
.unit {
  color: #64748b;
  font-size: 0.875rem;
}

/* 차트 래퍼 (가로 중앙 & 적당한 여백) */
.chart-wrapper {
  max-width: 800px;
  margin: 0 auto 2rem;
  background: #ffffff;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* 에러 텍스트 */
.error {
  max-width: 600px;
  margin: 1rem auto;
  color: #dc2626;
  text-align: center;
  font-weight: 500;
}
</style>

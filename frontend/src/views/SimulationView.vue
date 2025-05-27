<template>
  <section class="simulation-page">
    <!-- ✅ 상단 배너 추가 -->
    <div class="banner-section">
      <img src="/image/simulation.jpg" alt="시뮬레이션" class="banner-img" />
      <div class="banner-text">
        <h2>데이터 기반 은퇴 자산 시뮬레이션</h2>
        <p>예상 수익률과 지출을 바탕으로 노후 자산을 시각적으로 확인해보세요</p>
      </div>
    </div>
    <!-- <h1 class="page-title">은퇴 자산 시뮬레이션</h1> -->

    <div class="layout">
      <!-- 좌측 -->
      <div class="left-panel">
        <div class="panel">
          <SimulationForm />
        </div>
        <div v-if="store.data" class="panel chart-panel">
          <SimulationChart :results="store.data" />
        </div>
      </div>

      <!-- 우측 -->
      <div class="right-panel">
        <h2 class="section-title">10년 단위 예상 자산</h2>
        <div class="card-list">
          <div
            v-for="item in decadeSummary"
            :key="item.age"
            class="card"
            :class="{ 'zero-asset': item.asset === 0 }"
          >
            <span class="badge">{{ item.age }}세</span>
            <p class="amount">{{ formatNumber(item.asset) }}원</p>
            <p class="unit">{{ item.asset === 0 ? '0원' : toKoreanUnit(item.asset) }}</p>
          </div>
        </div>
      </div>
    </div>

    <p v-if="store.error" class="error">
      에러 발생: {{ store.error.message }}
    </p>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import SimulationForm from '@/components/SimulationForm.vue'
import SimulationChart from '@/components/SimulationChart.vue'
import { useSimulationStore } from '@/stores/simulation.js'

const store = useSimulationStore()

const decadeSummary = computed(() => {
  if (!store.data) return []
  const { age, median_assets } = store.data
  const firstDecade = Math.ceil(age[0] / 10) * 10
  return age
    .map((a, i) => ({ age: a, asset: median_assets[i] }))
    .filter(item => item.age >= firstDecade && item.age % 10 === 0)
})

function formatNumber(x) {
  return x.toLocaleString('ko-KR', { maximumFractionDigits: 0 })
}

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

  return parts.length > 0 ? parts.join(' ') + '원' : '원'
}
</script>

<style scoped>
.simulation-page {
  padding: 1.5rem;
  background-color: #f7f9fc;
  min-height: 100vh;
  box-sizing: border-box;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 800;
  margin-bottom: 2rem;
  text-align: center;
}

.layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  justify-content: center;
  align-items: center;
}

@media (min-width: 1024px) {
  .layout {
    flex-direction: row;
    align-items: flex-start;
    justify-content: center;
    max-width: 1400px;
    margin: 0 auto;
  }
}

.left-panel {
  flex: 0 0 66%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.panel {
  background: #ffffff;
  padding: 2rem;
  border-radius: 1.5rem;
  box-shadow: 0 10px 15px rgba(0,0,0,0.08);
}

.right-panel {
  flex: 0 0 25%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  min-height: fit-content;
}


.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-align: center;
  color: #111827;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.5rem;
}


.card-list {
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 1rem;
}

.card {
  background: #ffffff;
  padding: 1.25rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
  margin-bottom: 1rem; /* 카드 간 간격 확보 */
  min-height: unset; /* 줄바꿈 방지용 */
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15); /* hover 시 그림자 강조 */
  background-color: #f9fafb;
}

.amount {
  font-size: 1.25rem; /* ✅ 기존보다 더 축소 */
  font-weight: 700;   /* ✅ bold는 유지하되 너무 두껍지 않게 */
  color: #111827;
  margin: 0.25rem 0;
  word-break: keep-all;   /* ✅ 원 단위 끊김 방지 */
  white-space: nowrap;    /* ✅ 줄바꿈 방지 */
  overflow: hidden;
  text-overflow: ellipsis;
}


.unit {
  font-size: 0.8125rem; /* 살짝 더 작게 */
  color: #6b7280;
  margin-top: 0.5rem;
}

.badge {
  display: inline-block;
  background-color: #3b82f6;
  color: #ffffff;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.amount {
  font-size: 1.875rem;
  font-weight: 800;
  color: #111827;
  margin: 0.25rem 0;
}

.unit {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.error {
  color: #dc2626;
  margin-top: 1.5rem;
  text-align: center;
}
.banner-section {
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.banner-img {
  width: 100%;
  height: 100%;
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

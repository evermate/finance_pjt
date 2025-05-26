<template>
  <section class="simulation-page">
    <!-- 페이지 타이틀 -->
    <h1 class="page-title">은퇴 자산 시뮬레이션</h1>

    <!-- flex 레이아웃: 좌측(폼+차트) / 우측(카드 리스트) -->
    <div class="layout">
      <!-- 좌측 -->
      <div class="left-panel">
        <div class="panel">
          <SimulationForm />
        </div>
        <div v-if="store.data" class="panel">
          <SimulationChart :results="store.data" />
        </div>
      </div>

      <!-- 우측 -->
      <div class="right-panel">
        <h2 class="section-title">10년 단위 예상 자산</h2>
        <div class="card-list">
          <div v-for="item in decadeSummary" :key="item.age" class="card">
            <span class="badge">{{ item.age }}세</span>
            <p class="amount">{{ formatNumber(item.asset) }}원</p>
            <p class="unit">{{ toKoreanUnit(item.asset) }}</p>
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

  return parts.join(' ') + '원'
}
</script>

<style scoped>
/* ─── 페이지 전체 ─── */
.simulation-page {
  padding: 1.5rem;
  background-color: #f7f9fc;
  min-height: 100vh;
  box-sizing: border-box;
}

/* ─── 타이틀 ─── */
.page-title {
  font-size: 1.875rem;   /* 30px */
  font-weight: 800;
  margin-bottom: 2rem;
  text-align: center;
}

/* ─── 레이아웃 ─── */
.layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
@media (min-width: 1024px) {
  .layout {
    flex-direction: row;
  }
}

/* ─── 좌측 패널 ─── */
.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
/* 공통 패널 스타일 (폼/차트 박스) */
.panel {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 10px 15px rgba(0,0,0,0.1);
}

/* ─── 우측 패널 ─── */
.right-panel {
  width: 100%;
}
@media (min-width: 1024px) {
  .right-panel {
    width: 33.3333%;
  }
}

.section-title {
  font-size: 1.875rem;  /* 30px */
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}

/* ─── 카드 리스트 ─── */
.card-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ─── 개별 카드 ─── */
.card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: box-shadow .2s;
}
.card:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

/* ─── 나이 배지 ─── */
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

/* ─── 금액 텍스트 ─── */
.amount {
  font-size: 2.25rem;  /* 36px */
  font-weight: 800;
  color: #111827;
  margin: 0.5rem 0;
}

/* ─── 한글 단위 텍스트 ─── */
.unit {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
}

/* ─── 에러 메시지 ─── */
.error {
  color: #dc2626;
  margin-top: 1.5rem;
  text-align: center;
}
</style>

<!-- src/components/Eda/InfographicSection.vue -->
<template>
  <section class="infographic-section">
    <h2>금융 인포그래픽</h2>
    <div class="cards">
      <div
        class="card"
        v-for="item in items"
        :key="item.id"
      >
        <h3 class="card-title">{{ item.title }}</h3>

        <!-- 차트를 감싸는 래퍼 -->
        <div class="chart-wrapper">
         <!-- chartType 이 'text' 가 아니면 차트 렌더 -->
         <MiniChart
           v-if="item.chartType !== 'text'"
           :chartType="item.chartType"
           :labels="item.labels"
           :data="item.data"
         />
         <!-- chartType === 'text' 면 숫자 전용 뷰 -->
         <div
           v-else
           class="value-only"
         >
           <!-- item.value 를 억/만 단위로 포맷하거나 원 단위를 붙여서 표시 -->
           {{ formatNumber(item.value) }}
         </div>
       </div>

        <p class="card-desc">{{ item.description }}</p>
      </div>
    </div>
  </section>
</template>

 <!-- src/components/Eda/InfographicSection.vue -->
 <script setup>
 import { infographicItems } from '@/data/infographicData.js'
 import MiniChart from './MiniChart.vue'

 // 1) 데이터
 const items = infographicItems

 // 2) 숫자 포맷 헬퍼
 function formatNumber(val) {
   const v = Number(val)
   if (isNaN(v)) return val
   if (v >= 1e8) return (v / 1e8).toFixed(2) + '억'
   if (v >= 1e4) return (v / 1e4).toFixed(2) + '만'
   return v.toLocaleString() + '원'
 }
 </script>

<style scoped>
.infographic-section { padding:2rem 1rem; }
.infographic-section .cards {
  display:grid;
  grid-template-columns:repeat(auto-fill, minmax(300px,1fr));
  gap:1rem;
}

/* 3등분 그리드 → 최소 300px, 최대 1fr */
.card {
  max-width:320px;       /* 카드 너비 고정 상한 */
  display:flex;
  flex-direction:column;
  padding:1rem;
  box-sizing:border-box;
}

/* 카드 박스 */
.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  padding: 1rem;
  display: flex;
  flex-direction: column;

  /* 카드 너비 최소 300px, 최대 1fr */
  width: 100%;
  max-width: 320px;

  /* 카드 높이: 제목(약 1.2em) + 차트(140px) + 설명(약 2em) + 패딩 */
  height: auto;
  box-sizing: border-box;
}

/* 제목 */
.card-title {
  font-size: 1rem;
  margin: 0 0 0.5rem;
  text-align: center;
}

.chart-wrapper {
  display: flex;               /* 1) 플렉스 컨테이너로 전환 */
  align-items: center;         /* 수직 중앙 정렬 */
  justify-content: center;     /* 수평 중앙 정렬 */
  width: 100%;
  height: 140px;               /* 카드 안에 들어갈 높이 */
  overflow: hidden;            /* 차트가 튀어나오지 않도록 자르기 */
  box-sizing: border-box;
}

.chart-wrapper canvas {
  /* 2) 부모 비율에 맞춰 최대 크기 제한 */
  max-width: 80%;              /* 카드 너비의 80% */
  max-height: 100%;            /* 카드 높이의 100% */
}

/* 설명 */
.card-desc {
  font-size: 0.85rem;
  color: #555;
  text-align: center;
  line-height: 1.2em;
  /* 두 줄 넘지 않게 */
  max-height: 2.4em;
  overflow: hidden;
}
</style>
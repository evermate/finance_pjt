<!-- src/components/Eda/MiniChart.vue -->
<template>
  <div class="chart-with-legend">
    <div class="chart-wrapper">
      <canvas ref="canvas"></canvas>
    </div>
    <!-- bar 차트에만 레전드 표시 -->
    <div v-if="props.chartType === 'bar'" class="legend">
      <span
        v-for="(label, i) in props.labels"
        :key="i"
        class="legend-item"
      >
        {{ label }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  chartType: { type: String, required: true },
  labels:    { type: Array,  required: false, default: () => [] },
  data:      { type: Array,  required: false, default: () => [] },
})

const canvas = ref(null)
let chartInstance = null

function renderChart() {
  if (!canvas.value) return
  if (chartInstance) chartInstance.destroy()
  const ctx = canvas.value.getContext('2d')

  chartInstance = new Chart(ctx, {
    type: props.chartType,
    data: {
      labels: props.labels,
      datasets: [{
        data: props.data,
        backgroundColor:  'rgba(59,130,246,0.6)',
        borderColor:      'rgba(59,130,246,1)',
        borderWidth:      1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      },
      scales: {
        x: {
          display: false  // HTML 레전드를 쓰므로 axis 레이블은 숨김
        },
        y: {
          display: false
        }
      }
    }
  })
}

onMounted(renderChart)
watch(
  () => [props.chartType, props.labels, props.data],
  renderChart,
  { deep: true }
)
onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<style scoped>
.chart-with-legend {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  /* 카드 안쪽 여백을 더 줘서 legend가 잘리지 않도록 */
  padding-bottom: 0.5rem;
}

.chart-wrapper {
  width: 100%;
  /* 기존 140px → 레전드를 위한 공간 확보 차원에서 120px로 줄임 */
  height: 120px;
  overflow: hidden;
  margin-bottom: 0; /* legend가 바로 붙도록 */
}

canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}

/* HTML 레전드 */
.legend {
  display: flex;
  justify-content: space-around;
  /* 차트 아래로 더 내려주기 */
  margin-top: 0.5rem;
}

.legend-item {
  font-size: 0.75rem;
  color: #666;
  white-space: nowrap;
  /* 텍스트도 살짝 아래로 */
  transform: translateY(2px);
}
</style>

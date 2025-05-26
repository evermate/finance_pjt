<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  results: {
    type: Object,
    required: true
  }
})

const chartCanvas = ref(null)
let chartInstance = null

const renderChart = () => {
  const { age, median_assets, p10_assets, p90_assets } = props.results

  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels: age,
      datasets: [
        { label: '중앙값', data: median_assets, tension: .4 },
        { label: '10백분위', data: p10_assets, tension: .4 },
        { label: '90백분위', data: p90_assets, tension: .4 }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { title: { display: true, text: '나이' } },
        y: { title: { display: true, text: '자산 (원)' } }
      }
    }
  })
}

onMounted(renderChart)
watch(() => props.results, renderChart)
</script>

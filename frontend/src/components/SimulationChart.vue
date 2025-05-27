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
        {
          label: '중앙값',
          data: median_assets,
          tension: 0.4,
          borderWidth: 3,
          borderColor: '#3b82f6',
          pointRadius: 2
        },
        {
          label: '10백분위',
          data: p10_assets,
          tension: 0.4,
          borderWidth: 3,
          borderColor: '#f472b6',
          pointRadius: 2
        },
        {
          label: '90백분위',
          data: p90_assets,
          tension: 0.4,
          borderWidth: 3,
          borderColor: '#fbbf24',
          pointRadius: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          top: 20,
          bottom: 20,
          left: 10,
          right: 10
        }
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: '나이',
            font: {
              size: 16
            }
          },
          ticks: {
            font: {
              size: 12
            }
          }
        },
        y: {
          title: {
            display: true,
            text: '자산 (원)',
            font: {
              size: 16
            }
          },
          ticks: {
            font: {
              size: 12
            }
          }
        }
      }
    }
  })
}

onMounted(renderChart)
watch(() => props.results, renderChart)
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: 400px !important;
  max-width: 100%;
  display: block;
  margin: 0 auto;
}
</style>

<template>
    <div>
        <!-- 가입한 상품 리스트 -->
        <div v-if="joinedProducts.length" class="joined-products-list">
            <h4>가입한 상품 목록 ({{ joinedProducts.length }} / 5)</h4>
            <ul>
                <li v-for="(product, idx) in joinedProducts" :key="product.fin_prdt_cd">
                    {{ idx + 1 }} :
                    ({{ product.product_type === 'deposit' ? '정기예금' : '정기적금' }})
                    {{ product.bank_name }} -
                    <router-link :to="{
                        name: 'product-detail',
                        params: {
                            type: product.product_type,
                            id: product.fin_prdt_cd
                        }
                    }" class="product-link">
                        {{ product.fin_prdt_nm }}
                    </router-link>
                </li>

            </ul>
        </div>

        <!-- 차트 -->
        <div class="chart-container" v-if="joinedProducts.length">
            <canvas ref="chart"></canvas>
        </div>

        <!-- 빈 상태 -->
        <div v-else class="no-products">
            가입한 상품이 없습니다.
        </div>
    </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import Chart from 'chart.js/auto'
import { useAccountStore } from '@/stores/accounts'

// 🟦 Pinia store 연결
const accountStore = useAccountStore()
const { joinedProducts } = storeToRefs(accountStore)

const chart = ref(null)
let chartInstance = null

// 📊 데이터 추출 함수
const getMaxRates = () => {
    return joinedProducts.value.map(product => {
        if (!product.options || product.options.length === 0) return null
        return Math.max(...product.options.map(opt => opt.intr_rate2 ?? 0))
    })
}

// 📈 차트 그리기
const renderChart = () => {
    if (chartInstance) {
        chartInstance.destroy()
    }
    if (!joinedProducts.value.length) return

    chartInstance = new Chart(chart.value, {
        type: 'bar',
        data: {
            labels: joinedProducts.value.map(p => p.fin_prdt_nm),
            datasets: [
                {
                    label: '기본 금리',
                    data: joinedProducts.value.map(p => {
                        const rates = p.options?.map(o => o.intr_rate ?? 0)
                        return rates?.length ? Math.max(...rates) : null
                    }),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)', // 파랑
                },
                {
                    label: '최고 우대금리',
                    data: joinedProducts.value.map(p => {
                        const rates = p.options?.map(o => o.intr_rate2 ?? 0)
                        return rates?.length ? Math.max(...rates) : null
                    }),
                    backgroundColor: 'rgba(75, 192, 75, 0.6)', // 초록
                },
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 0.5
                    }
                }
            }
        }
    })

}

// 🚀 초기 렌더 + 반응형 리렌더
onMounted(() => {
    renderChart()
})
watch(joinedProducts, () => {
    renderChart()
}, { deep: true })
</script>

<style scoped>
.joined-products-list {
    margin-bottom: 32px;
    padding: 18px 24px;
    background: #f6f8fa;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(60, 80, 120, 0.06);
}

.joined-products-list h4 {
    margin: 0 0 10px 0;
    font-size: 1.08em;
    color: #1a2633;
    font-weight: 700;
}

.joined-products-list ul {
    margin: 0;
    padding-left: 0;
    list-style: none;
    font-size: 1em;
}

.joined-products-list li {
    margin-bottom: 3px;
}

.chart-container {
    width: 100%;
    min-height: 300px;
}

@media (max-width: 600px) {
    .joined-products-list {
        padding: 14px 8px;
        font-size: 0.98em;
    }

    .chart-container {
        min-height: 180px;
    }
}

.no-products {
    margin: 2rem 0;
    padding: 2rem 1rem;
    background: #f3f3f3;
    border-radius: 10px;
    color: #666;
    text-align: center;
    font-size: 1.1em;
}

.product-link {
    color: #2a67cc;
    text-decoration: none;
    font-weight: 500;
}

.product-link:hover {
    text-decoration: underline;
}
</style>

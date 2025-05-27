<template>
  <section class="prod-slider-section" v-if="items.length">
    <h2 style="text-align: left;">{{ title }}</h2>

    <!-- 여기에 호버 이벤트 추가 -->
    <div
      class="slider-viewport"
      @mouseenter="pauseSlide"
      @mouseleave="resumeSlide"
    >
      <div class="slider-container" ref="containerRef">
        <div
          v-for="item in items"
          :key="item.fin_prdt_cd + '-' + item.option_id"
          class="slider-card"
        >
          <img
            :src="getBankLongIcon(item.bank.kor_co_nm)"
            alt="은행 로고"
            class="prod-card-thumb"
          />
          <div class="prod-card-body">
            <RouterLink
              :to="`/product/${item.product_type||'saving'}/${item.fin_prdt_cd}`"
              class="prod-name-link"
            >
              {{ item.fin_prdt_nm }}
            </RouterLink>
            <div class="prod-card-meta">
              <span>은행: {{ item.bank.kor_co_nm }}</span>
              <span>기간: {{ item.save_trm }}개월</span>
              <span>금리: {{ item.intr_rate }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import axios from 'axios'
import { getBankLongIcon } from '@/utils/bankIconMap'

const props = defineProps({
  title:         { type: String, default: '주목할 만한 금융 상품' },
  limit:         { type: Number, default: 2 },
  visibleCount:  { type: Number, default: 5 },
  interval:      { type: Number, default: 2000 }
})

const items       = ref([])
const containerRef= ref(null)
let slideTimer    = null
let currentIndex  = 0

onMounted(async () => {
  const { data } = await axios.get('/api/products/deposits/slider/', {
    params: { limit: props.limit }
  })
  items.value = data

  await nextTick()
  startAutoSlide()
})

onBeforeUnmount(() => {
  clearInterval(slideTimer)
})

/** 자동 슬라이드 시작 */
function startAutoSlide() {
  clearInterval(slideTimer)
  const container = containerRef.value
  if (!container || items.value.length <= props.visibleCount) return

  const card    = container.querySelector('.slider-card')
  const gapPx   = parseInt(getComputedStyle(container).gap) || 0
  const step    = card.offsetWidth + gapPx
  const maxIdx  = items.value.length - props.visibleCount

  slideTimer = setInterval(() => {
    currentIndex = currentIndex < maxIdx ? currentIndex + 1 : 0
    container.scrollTo({
      left: currentIndex * step,
      behavior: 'smooth'
    })
  }, props.interval)
}

/** 호버 시 일시정지 */
function pauseSlide() {
  clearInterval(slideTimer)
}

/** 마우스 떠날 때 재개 */
function resumeSlide() {
  startAutoSlide()
}
</script>

<style scoped>
.prod-slider-section {
  padding: 2rem 1rem;  /* padding을 줄여서 크기 일치 */
  background-color: #f0f6fd;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem; /* margin을 동일하게 설정 */
  height: auto; /* 높이를 자동으로 설정하여 유동적으로 크기 맞춤 */
}

.slider-viewport {
  overflow: hidden;
}

.slider-container {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 1rem;
  scroll-snap-type: x mandatory;
}

.slider-container::-webkit-scrollbar {
  height: 8px;
}

.slider-container::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.15);
  border-radius: 10px;
}

.slider-card {
  flex: 0 0 240px;
  scroll-snap-align: start;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.slider-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.prod-card-thumb {
  width: 100%;
  height: 120px;
  object-fit: contain;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.prod-card-body {
  padding: 1rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.prod-name-link {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  text-decoration: none;
  margin-bottom: 0.75rem;
  transition: color 0.3s;
}

.prod-name-link:hover {
  color: #2f80ed;
}

.prod-card-meta {
  font-size: 0.9rem;
  color: #6b7280;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: flex-start;
  margin-top: auto;
}
</style>

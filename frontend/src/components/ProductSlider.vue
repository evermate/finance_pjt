<!-- src/components/Sliding_Window/ProductSlider.vue -->
<template>
  <section class="prod-slider-section" v-if="items.length">
    <h2 class="slider-title">{{ title }}</h2>

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
            <!-- 가입 버튼 제거 -->
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
  title:         { type: String, default: '추천 금융상품' },
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

/** 자동 슬라이드 시작 (기존 startAutoSlide) */
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
  padding: 2rem 1rem;
}
.slider-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.slider-viewport {
  /* overflow 숨기고, hover 이벤트 감지할 wrapper */
  overflow: hidden;
}
.slider-container {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-bottom: 0.5rem;
}
.slider-container::-webkit-scrollbar {
  height: 6px;
}
.slider-container::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.2);
  border-radius: 3px;
}

.slider-card {
  flex: 0 0 240px;
  scroll-snap-align: start;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.prod-card-thumb {
  width: 100%;
  height: 120px;
  object-fit: contain;
  background: #f9f9f9;
}
.prod-card-body {
  padding: 0.75rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.prod-name-link {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1f2937;
  text-decoration: none;
}
.prod-card-meta {
  font-size: 0.85rem;
  color: #6b7280;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>

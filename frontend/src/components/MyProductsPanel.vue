<!-- src/components/MyProductsPanel.vue -->
<template>
    <div class="fab-wrapper" ref="wrapper" :style="{ top: `${position.top}px`, left: `${position.left}px` }"
        @mousedown="startDrag" @touchstart.prevent="startDrag">
        <button v-if="accountStore.user" class="fab-btn" @click="handleClick">
            가입한 상품 ({{ accountStore.user?.joined_products?.length || 0 }} / 5)
        </button>

        <transition name="slide-down">
            <div v-if="isOpen" class="fab-panel" ref="panel">
                <div class="panel-header">
                    <span>가입한 상품 ({{ accountStore.user?.joined_products?.length || 0 }} / 5)</span>
                    <div class="panel-tools">
                        <!-- ✅ SVG 압정 -->
                        <button class="pin-btn" @click="isFixed = !isFixed" :title="isFixed ? '고정됨' : '고정 해제'">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                                class="pin-icon" :class="{ active: isFixed }">
                                <path d="M9.293 2.293a1 1 0 011.414 0l2.828 2.828a1 1 0 010 1.414l-1.586 1.586 
                         2.121 2.121a1 1 0 010 1.414L12.414 13H11v3a1 1 0 01-2 0v-3H7.586a1 1 
                         0 01-.707-1.707l2.121-2.121-1.586-1.586a1 1 0 010-1.414L9.293 2.293z" />
                            </svg>
                        </button>

                        <button class="close-btn" @click="isOpen = false">✕</button>
                    </div>
                </div>

                <ul class="panel-list">
                    <li v-for="item in accountStore.user?.joined_products || []" :key="item.fin_prdt_cd"
                        class="panel-item">
                        <div class="product-name">{{ item.fin_prdt_nm }}</div>
                        <div class="bank-name">{{ item.bank_name }}</div>
                        <button class="leave-btn" @click="accountStore.leaveProduct(item.fin_prdt_cd)">
                            X
                        </button>
                    </li>
                </ul>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const isOpen = ref(false)
const isFixed = ref(false)
const isDragging = ref(false)
const wasDragged = ref(false)
const position = ref({ top: 200, left: 20 })
const mouseUpPosition = ref({ x: 0, y: 0 })  // ✅ 드래그 종료 좌표 저장
const wrapper = ref(null)

const accountStore = useAccountStore()
let offset = { x: 0, y: 0 }

const startDrag = (e) => {
    isDragging.value = true
    const clientX = e.clientX || e.touches[0].clientX
    const clientY = e.clientY || e.touches[0].clientY
    offset.x = clientX - position.value.left
    offset.y = clientY - position.value.top

    window.addEventListener('mousemove', onDrag)
    window.addEventListener('mouseup', stopDrag)
    window.addEventListener('touchmove', onDrag)
    window.addEventListener('touchend', stopDrag)
}

const onDrag = (e) => {
    if (!isDragging.value) return
    wasDragged.value = true
    const clientX = e.clientX || e.touches[0].clientX
    const clientY = e.clientY || e.touches[0].clientY
    position.value.left = clientX - offset.x
    position.value.top = clientY - offset.y
}

const stopDrag = (e) => {
    isDragging.value = false

    // ✅ 드래그 판정은 여기서 초기화
    setTimeout(() => {
        wasDragged.value = false  // 클릭보다 뒤에 실행되도록
    }, 0)

    const clientX = e.clientX || e.changedTouches?.[0]?.clientX
    const clientY = e.clientY || e.changedTouches?.[0]?.clientY
    mouseUpPosition.value = { x: clientX, y: clientY }  // ✅ 드래그 종료 위치 기록

    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
    window.removeEventListener('touchmove', onDrag)
    window.removeEventListener('touchend', stopDrag)
    localStorage.setItem('fabPosition', JSON.stringify(position.value))
}

const handleClick = (e) => {
    if (wasDragged.value) return
    const clickX = e.clientX
    const clickY = e.clientY
    const dx = Math.abs(clickX - mouseUpPosition.value.x)
    const dy = Math.abs(clickY - mouseUpPosition.value.y)
    const tolerance = 3  // ✅ 오차 허용값 (픽셀)

    const isTrueClick = dx < tolerance && dy < tolerance

    if (!isTrueClick) return
    if (isOpen.value && isFixed.value) return
    isOpen.value = !isOpen.value
}

const handleClickOutside = (e) => {
    if (
        isOpen.value &&
        !isFixed.value &&
        wrapper.value &&
        !wrapper.value.contains(e.target)
    ) {
        isOpen.value = false
    }
}

onMounted(() => {
    const saved = localStorage.getItem('fabPosition')
    if (saved) position.value = JSON.parse(saved)
    document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>


<style scoped>
.fab-wrapper {
    position: fixed;
    z-index: 1000;
}

.fab-btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.6rem 1rem;
    border-radius: 999px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    cursor: grab;
}

.fab-panel {
    position: absolute;
    top: calc(100% + 10px);
    left: 0;
    width: 260px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 1rem;
}

.slide-down-enter-active,
.slide-down-leave-active {
    transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    margin-bottom: 1rem;
}

.panel-tools {
    display: flex;
    gap: 0.3rem;
    align-items: center;
}

.pin-icon {
    width: 20px;
    height: 20px;
    color: #aaa;
    transition: transform 0.3s ease, color 0.3s ease;
}

.pin-icon.active {
    color: #df2e5a;
    transform: rotate(-45deg);
}

.panel-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.panel-item {
    margin-bottom: 0.8rem;
    font-size: 0.85rem;
    background: #f8f9fa;
    border-radius: 8px;
    padding: 0.6rem;
    position: relative;
}

.product-name {
    font-weight: bold;
}

.bank-name {
    color: #666;
    font-size: 0.8rem;
}

.leave-btn {
    position: absolute;
    top: 0.4rem;
    right: 0.6rem;
    background: none;
    border: none;
    color: #dc3545;
    font-size: 1rem;
    cursor: pointer;
}
</style>

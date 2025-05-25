<template>
    <div class="fab-wrapper" ref="wrapper" :style="{ top: `${position.top}px`, left: `${position.left}px` }"
        @mousedown="startDrag" @touchstart.prevent="startDrag">
        <button
            v-if="accountStore.user"
            class="fab-btn"
            @click="handleClick"
            :class="{ added: addedEffect, removed: removedEffect }"
        >
            가입한 상품 ({{ joinedCount }} / 5)
            <span v-if="addedEffect" class="effect-badge add">+1</span>
            <span v-if="removedEffect" class="effect-badge remove">-1</span>
        </button>

        <transition name="slide-down">
            <div v-if="isOpen" class="fab-panel" ref="panel">
                <div class="panel-header">
                    <span>가입한 상품 ({{ joinedCount }} / 5)</span>
                    <div class="panel-tools">
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
                        <button class="leave-btn" @click="leaveAndEffect(item.fin_prdt_cd)">
                            X
                        </button>
                    </li>
                </ul>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const isOpen = ref(false)
const isFixed = ref(false)
const isDragging = ref(false)
const wasDragged = ref(false)
const position = ref({ top: 200, left: 20 })
const mouseUpPosition = ref({ x: 0, y: 0 })
const wrapper = ref(null)

const accountStore = useAccountStore()
let offset = { x: 0, y: 0 }

const joinedCount = ref(accountStore.user?.joined_products?.length || 0)
const addedEffect = ref(false)
const removedEffect = ref(false)
let prevCount = accountStore.user?.joined_products?.length || 0
let autoPanelTimeout = null

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
    setTimeout(() => {
        wasDragged.value = false
    }, 0)
    const clientX = e.clientX || e.changedTouches?.[0]?.clientX
    const clientY = e.clientY || e.changedTouches?.[0]?.clientY
    mouseUpPosition.value = { x: clientX, y: clientY }
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
    const tolerance = 3
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

// "X"버튼 클릭 시 -> 계정 스토어 leave 호출
const leaveAndEffect = async (fin_prdt_cd) => {
    prevCount = accountStore.user?.joined_products?.length || 0
    await accountStore.leaveProduct(fin_prdt_cd)
    // fetchUser 이후 watch에서 이펙트/패널 자동 동작 처리
}

onMounted(() => {
    const saved = localStorage.getItem('fabPosition')
    if (saved) position.value = JSON.parse(saved)
    document.addEventListener('click', handleClickOutside)
})

// 실제 핵심! length가 변할 때마다 effect/panel 처리
watch(
    () => accountStore.user?.joined_products?.length,
    (newVal, oldVal) => {
        if (typeof oldVal !== 'number' || typeof newVal !== 'number') return

        // 신규 추가
        if (newVal > oldVal) {
            addedEffect.value = false
            void nextTick(() => {
                addedEffect.value = true
                setTimeout(() => {
                    addedEffect.value = false
                }, 700)
            })
            if (!isFixed.value) {
                isOpen.value = true
                clearTimeout(autoPanelTimeout)
                autoPanelTimeout = setTimeout(() => {
                    isOpen.value = false
                }, 1500)
            }
        }

        // 삭제
        if (newVal < oldVal) {
            removedEffect.value = false
            void nextTick(() => {
                removedEffect.value = true
                setTimeout(() => {
                    removedEffect.value = false
                }, 700)
            })
            if (!isFixed.value) {
                isOpen.value = true
                clearTimeout(autoPanelTimeout)
                autoPanelTimeout = setTimeout(() => {
                    isOpen.value = false
                }, 1500)
            }
        }

        joinedCount.value = newVal
    }
)

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
    clearTimeout(autoPanelTimeout)
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
    position: relative;
    transition: box-shadow 0.4s, transform 0.25s;
}

.fab-btn.added {
    box-shadow: 0 0 16px 4px #31d2f2, 0 0 24px 10px #b4e2f3;
    transform: scale(1.09);
    z-index: 10;
}
.fab-btn.removed {
    box-shadow: 0 0 16px 4px #df2e5a, 0 0 24px 10px #f6bbc6;
    transform: scale(1.09) rotate(-3deg);
    z-index: 10;
}

.effect-badge {
    position: absolute;
    top: -10px;
    right: -14px;
    font-weight: bold;
    border-radius: 50%;
    font-size: 0.95rem;
    padding: 0.13em 0.7em;
    pointer-events: none;
    box-shadow: 0 2px 10px rgba(49,210,242,0.4);
    animation: pop-in 0.7s cubic-bezier(0.5,1.8,0.6,1.1);
    opacity: 0;
}
.effect-badge.add {
    background: #31d2f2;
    color: white;
    opacity: 1;
}
.effect-badge.remove {
    background: #df2e5a;
    color: white;
    opacity: 1;
}

@keyframes pop-in {
    0% {
        transform: scale(0.7) translateY(-10px);
        opacity: 0.1;
    }
    30% {
        transform: scale(1.1) translateY(-8px);
        opacity: 1;
    }
    70% {
        transform: scale(1.09) translateY(-4px);
        opacity: 1;
    }
    100% {
        transform: scale(1) translateY(0);
        opacity: 0;
    }
}

/* 이하 기존 스타일 동일 */
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

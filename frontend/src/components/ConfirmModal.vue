<!-- src/components/common/ConfirmModal.vue -->
<template>
  <div class="modal-overlay" @click.self="cancel">
    <div class="modal-box">
      <button class="close-btn" @click="cancel">×</button>

      <h2 class="modal-title">{{ modal.title }}</h2>
      <p class="modal-desc">{{ modal.description }}</p>

      <div class="modal-actions">
        <!-- cancel 버튼: 왼쪽 (always gray, but hover depends on mode) -->
        <button
          v-if="modal.cancelText !== null"
          :class="['cancel-btn', modal.mode === 'danger' ? 'negative' : 'positive']"
          @click="cancel"
        >
          {{ modal.cancelText }}
        </button>

        <!-- confirm 버튼: 오른쪽 (hover에 강조색상) -->
        <button
          :class="['confirm-btn', modal.mode === 'danger' ? 'negative' : 'positive']"
          @click="confirm"
        >
          {{ modal.confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useModalStore } from '@/stores/modal'
const modal = useModalStore()

const confirm = () => modal.confirm()
const cancel = () => modal.cancel()

// 🛠️ 키보드 핸들러
const handleKeyDown = (e) => {
  if (e.key === 'Escape') {
    cancel()
  } else if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault()  // 스크롤 방지 (특히 Space)
    confirm()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  backdrop-filter: blur(2px);
}

.modal-box {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  position: relative;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #888;
  cursor: pointer;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #ff4040;
}

.modal-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #212529;
}

.modal-desc {
  margin-top: 0.4rem;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
  color: #666;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

/* 모든 버튼 기본 스타일 (회색) */
.cancel-btn,
.confirm-btn {
  flex: 1;
  padding: 0.6rem 1rem;
  font-weight: 600;
  font-size: 0.95rem;
  border-radius: 8px;
  background-color: #f1f3f5;
  color: #333;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* 긍정(positive) → 파랑 */
.confirm-btn.positive:hover,
.cancel-btn.negative:hover {
  background-color: #2b66f6;
  color: white;
}

/* 부정(negative) → 빨강 */
.confirm-btn.negative:hover,
.cancel-btn.positive:hover {
  background-color: #ff0000b6;
  color: white;
}

</style>


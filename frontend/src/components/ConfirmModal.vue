<!-- src/components/common/ConfirmModal.vue -->
<template>
  <div class="modal-overlay" @click.self="cancel">
    <div class="modal-box">
      <button class="close-btn" @click="cancel">×</button>
      <h2 class="modal-title">{{ modal.title }}</h2>
      <p class="modal-desc">{{ modal.description }}</p>
      <div class="modal-actions">
        <button
          v-if="modal.cancelText !== null"
          class="cancel-btn"
          @click="cancel"
        >
          {{ modal.cancelText }}
        </button>
        <button class="confirm-btn" @click="confirm">
          {{ modal.confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useModalStore } from '@/stores/modal'
const modal = useModalStore()

const confirm = () => modal.confirm()
const cancel = () => modal.cancel()
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
  /* animation: fadeInZoom 0.1s ease-out; */
  transition: transform 0.3s ease, opacity 0.3s ease;
  will-change: transform, opacity;
}

@keyframes fadeInZoom {
  0% {
    opacity: 0;
    transform: scale(0.92);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
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

.cancel-btn,
.confirm-btn {
  flex: 1;
  padding: 0.6rem 1rem;
  font-weight: 600;
  font-size: 0.95rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn {
  background-color: rgb(255, 255, 255);
  color: #333;
}

.cancel-btn:hover {
  background-color: #ff8080;
  color: white;
}

.confirm-btn {
  background-color: white;
}

.confirm-btn:hover {
  background-color: #4e6efd;
  color: white;
}
</style>

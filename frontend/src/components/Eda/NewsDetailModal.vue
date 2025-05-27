<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-backdrop" @click.self="close">
      <div class="modal-window">
        <button class="close-btn" @click="close">✕</button>
        <!-- 제목/메타는 그대로 -->
        <h1 class="title">{{ post.title }}</h1>
        <p class="meta">{{ post.date }} · {{ post.author }}</p>

        <!-- ▼ 이미지 삽입 구간 ▼ -->
        <img v-if="post.image" :src="post.image" alt="게시글 이미지" class="modal-image" />

        <!-- content 가 있으면 렌더, 없으면 iframe -->
        <div v-if="post.content" class="content" v-html="post.content"></div>
        <iframe v-else-if="post.link" :src="post.link" class="iframe-content" frameborder="0" />
        <p v-else>내용이 없습니다.</p>

      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  visible: Boolean,
  post: {
    type: Object,
    default: () => ({})
  }
})
const emit = defineEmits(['close'])

function close() {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-window {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
}

.modal-image {
  width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 1rem 0;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  border: none;
  background: none;
  font-size: 1.25rem;
  cursor: pointer;
}

.title {
  margin-top: 0;
  font-size: 1.6rem;
  font-weight: bold;
}

.meta {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.summary {
  font-style: italic;
  margin-bottom: 1rem;
}

.thumb {
  width: 100%;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.content {
  line-height: 1.6;
  white-space: pre-wrap;
}
</style>

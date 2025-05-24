<template>
  <div class="detail-container" v-if="post">
    <div class="header">
      <h1 class="title">{{ post.title }}</h1>
      <div class="meta">
        <span><strong>작성자:</strong> {{ post.author }}</span>
        <span><strong>작성일:</strong> {{ formatDate(post.created_at) }}</span>
        <span><strong>게시판:</strong> {{ boardLabel(post.board_type) }}</span>
      </div>
    </div>

    <div class="post-content">
      <p class="content-text">{{ post.content }}</p>

      <p v-if="post.board_type === 'REVIEW'" class="highlight">⭐ 평점: {{ post.rating }}/5</p>
      <p v-if="post.board_type === 'NEWS'" class="highlight">
        🔗 <a :href="post.link" target="_blank" class="news-link">관련 뉴스 보기</a>
      </p>
    </div>

    <div
      v-if="accountStore.user?.username === post.author"
      class="author-actions"
    >
      <button class="edit-btn" @click="goEdit">✏️ 수정</button>
      <button class="delete-btn" @click="deletePost">🗑️ 삭제</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()
const accountStore = useAccountStore()

const post = ref(null)

function boardLabel(type) {
  return { REVIEW: '리뷰', NEWS: '뉴스', FREE: '자유' }[type] || type
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString()
}

async function deletePost() {
  if (!confirm('정말 삭제하시겠습니까?')) return
  const success = await store.deletePost(post.value.id)
  if (success) {
    alert('삭제되었습니다.')
    router.push('/community')
  } else {
    alert('삭제 실패')
  }
}

function goEdit() {
  router.push({ name: 'community-edit', params: { id: post.value.id } })
}

onMounted(async () => {
  const id = route.params.id
  post.value = await store.fetchPost(id)
})
</script>

<style scoped>
.detail-container {
  padding: 2rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  max-width: 720px;
  margin: 0 auto;
  font-family: 'Pretendard', sans-serif;
}

.header .title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.post-content {
  margin-top: 2rem;
  line-height: 1.7;
  font-size: 1rem;
  color: #333;
}

.content-text {
  white-space: pre-wrap;
}

.highlight {
  margin-top: 1.2rem;
  font-weight: 500;
  color: #1e88e5;
}

.news-link {
  color: #1e88e5;
  text-decoration: underline;
}

.author-actions {
  margin-top: 2rem;
  display: flex;
  gap: 0.75rem;
}

.edit-btn,
.delete-btn {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}

.edit-btn {
  background-color: #e0f2f1;
  color: #00695c;
}

.delete-btn {
  background-color: #ffebee;
  color: #c62828;
}

.edit-btn:hover {
  background-color: #b2dfdb;
}

.delete-btn:hover {
  background-color: #ffcdd2;
}
</style>

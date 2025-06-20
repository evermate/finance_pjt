<template>
  <div class="detail-container" v-if="post">
    <div class="header">
      <h1 class="title">{{ post.title }}</h1>
      <div class="meta">
        <router-link :to="{ name: 'user-profile', params: { username: post.author } }">
          {{ post.author }}
        </router-link>
        <span><strong>작성일:</strong> {{ formatDate(post.created_at) }}</span>
        <span><strong>게시판:</strong> {{ boardLabel(post.board_type) }}</span>
        <span class="views"><strong>조회수:</strong> {{ post.views }}</span>
      </div>
    </div>

    <div class="post-content">
      <p class="content-text">{{ post.content }}</p>

      <p v-if="post.board_type === 'REVIEW'" class="highlight">⭐ 평점: {{ post.rating }}/5</p>
      <p v-if="post.board_type === 'NEWS'" class="highlight">
        🔗 <a :href="post.link" target="_blank" class="news-link">관련 뉴스 보기</a>
      </p>
    </div>

    <div v-if="accountStore.user?.username === post.author" class="author-actions">
      <button class="edit-btn" @click="goEdit">수정</button>
      <button class="delete-btn" @click="deletePost">삭제</button>
    </div>
  </div>

  <!-- 좋아요 영역 -->
  <div v-if="post" class="like-area">
    <button @click="toggleLike">
      <span v-if="post.is_liked">💖</span>
      <span v-else>🤍</span>
      {{ post.like_count }}
    </button>
  </div>

  <!-- 댓글 영역 -->
  <div class="comment-section" v-if="post">
    <h2>댓글</h2>
    <ul v-if="comments.length">
      <CommentItem v-for="comment in comments" :key="comment.id" :comment="comment" :post-id="post.id" />
    </ul>
    <p v-else>댓글이 없습니다.</p>

    <div v-if="accountStore.user" class="comment-form">
      <textarea v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
      <button @click="submitComment">댓글 작성</button>
    </div>
    <div v-else>
      <p>로그인 후 댓글을 작성할 수 있습니다.</p>
    </div>
  </div>

  <!-- 목록으로 돌아가기 -->
  <!-- <div class="back-button-wrapper">
    <button class="back-button" @click="goBack">← 목록으로 돌아가기</button>
  </div> -->
    <div class="back-to-list">
        <button @click="goBack">목록으로 돌아가기</button>
    </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import { useCommentStore } from '@/stores/comment'
import { useAccountStore } from '@/stores/accounts'
import { useModalStore } from '@/stores/modal'
import { useToast } from 'vue-toastification'
import CommentItem from '@/components/CommentItem.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()
const accountStore = useAccountStore()
const commentStore = useCommentStore()

const modal = useModalStore()
const toast = useToast()

const post = ref(null)
const newComment = ref('')
const comments = computed(() => commentStore.comments.results || [])

async function submitComment() {
  if (!newComment.value.trim()) return
  await commentStore.createComment(post.value.id, newComment.value)
  newComment.value = ''
}

function boardLabel(type) {
  return { REVIEW: '리뷰', NEWS: '뉴스', FREE: '자유' }[type] || type
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString()
}

async function deletePost() {
  const confirm = await modal.open({
    title: '게시글 삭제',
    description: '정말 이 게시글을 삭제하시겠습니까?',
    confirmText: '삭제',
    cancelText: '취소',
  })

  if (!confirm) return

  const success = await store.deletePost(post.value.id)

  if (success) {
    toast.success('✅ 게시글이 삭제되었습니다.', { timeout: 2000 })
    router.push('/community')
  } else {
    toast.error('❌ 삭제에 실패했습니다. 다시 시도해주세요.', { timeout: 2500 })
  }
}


async function toggleLike() {
  const token = localStorage.getItem('authToken')
  if (!token) return alert('로그인 후 이용 가능합니다.')
  const endpoint = post.value.is_liked ? 'unlike' : 'like'
  try {
    const res = await axios.post(
      `/api/community/posts/${post.value.id}/${endpoint}/`,
      {},
      { headers: { Authorization: `Token ${token}` } }
    )
    post.value.is_liked = res.data.liked
    post.value.like_count = res.data.like_count
  } catch (err) {
    alert('요청 실패')
    console.error(err)
  }
}

function goEdit() {
  router.push({ name: 'community-edit', params: { id: post.value.id } })
}

function goBack() {
  router.push({ name: 'community' })
}

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await axios.get(`/api/community/posts/${id}/`)
    post.value = res.data
  } catch (err) {
    console.error('게시글 조회 실패:', err)
  }
  await commentStore.fetchComments(id)

//   console.log('댓글 데이터 확인:', commentStore.comments)

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
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.views {
  margin-left: auto;
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

.comment-section {
  max-width: 720px;
  margin: 2rem auto;
  padding: 1.5rem 2rem;
  background-color: #fafafa;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  font-family: 'Pretendard', sans-serif;
}

.comment-section h2 {
  font-size: 1.3rem;
  margin-bottom: 1.2rem;
  color: #333;
}

.comment-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #444;
}

.comment-content {
  display: block;
  margin-top: 0.3rem;
  margin-left: 0.5rem;
}

.comment-form {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.comment-form textarea {
  width: 100%;
  min-height: 80px;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  resize: vertical;
  font-size: 0.95rem;
  font-family: 'Pretendard', sans-serif;
}

.comment-form button {
  align-self: flex-end;
  padding: 0.5rem 1.2rem;
  background-color: #1e88e5;
  color: white;
  font-size: 0.95rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.comment-form button:hover {
  background-color: #1565c0;
}

.like-area {
  max-width: 720px;
  margin: 1.5rem auto 0;
  padding: 1rem 2rem;
  text-align: right;
  font-family: 'Pretendard', sans-serif;
}

.like-area button {
  background-color: transparent;
  border: none;
  font-size: 1.1rem;
  color: #e53935;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.like-area button:hover {
  background-color: #ffe5e5;
}

.back-button-wrapper {
  max-width: 720px;
  margin: 2rem auto;
  text-align: center;
}

.back-button {
  background-color: #e3f2fd;
  color: #1565c0;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.back-button:hover {
  background-color: #bbdefb;
}
.back-to-list {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}
.back-to-list button {
  background-color: #a5d6a7;
  color: #1b5e20;
  font-size: 0.95rem;
  padding: 0.6rem 1.4rem;
  border: 1px solid #c8e6c9;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.back-to-list button:hover {
  background-color: #c8e6c9;
}
</style>

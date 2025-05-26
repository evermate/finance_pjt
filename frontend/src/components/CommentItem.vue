<template>
  <li class="comment-item">
    <div class="comment-body">
      <router-link
        :to="authorLink"
      >
        <strong>{{ comment.author }}</strong>
      </router-link>
      | {{ formatDate(comment.created_at) }}

      <p>{{ comment.content }}</p>

      <button v-if="isAuthor" @click="onDelete" class="delete-btn">삭제</button>
      <button v-if="isReplyAllowed" @click="toggleReply" class="reply-btn">답글</button>
    </div>

    <!-- 대댓글 작성 폼 -->
    <div v-if="showReplyForm" class="reply-form">
      <textarea v-model="replyContent" placeholder="답글을 입력하세요" />
      <button @click="submitReply">작성</button>
    </div>

    <!-- 자식 댓글 재귀 렌더링 -->
    <ul v-if="comment.children?.length" class="nested-comments">
      <CommentItem
        v-for="child in comment.children"
        :key="child.id"
        :comment="child"
        :post-id="postId"
      />
    </ul>
  </li>
</template>





<script setup>
import { ref, computed } from 'vue'
import { useCommentStore } from '@/stores/comment'
import { useAccountStore } from '@/stores/accounts'
import CommentItem from './CommentItem.vue'

const props = defineProps({
  comment: Object,
  postId: Number,
})

const store = useCommentStore()
const account = useAccountStore()

const isAuthor = computed(() => props.comment.author === account.user?.username)
const isReplyAllowed = computed(() => !props.comment.parent)

const showReplyForm = ref(false)
const replyContent = ref('')


const authorLink = computed(() => {
  return isAuthor.value
    ? { name: 'mypage' }
    : { name: 'user-profile', params: { username: props.comment.author } }
})


function toggleReply() {
  showReplyForm.value = !showReplyForm.value
}

async function submitReply() {
  if (!replyContent.value.trim()) return
  await store.createComment(props.postId, replyContent.value, props.comment.id)
  replyContent.value = ''
  showReplyForm.value = false
}

async function onDelete() {
  const confirmDelete = confirm('댓글을 삭제하시겠습니까?')
  if (!confirmDelete) return
  await store.deleteComment(props.postId, props.comment.id)
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString()
}
</script>


<style scoped>
.comment-item {
  margin-bottom: 1.5rem;
  font-family: 'Pretendard', sans-serif;
}

.comment-body {
  background-color: #f9f9f9;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  position: relative;
}

.comment-body strong {
  color: #1976d2;
}

.comment-body p {
  margin-top: 0.5rem;
  font-size: 0.95rem;
  color: #444;
}

.comment-body .meta {
  font-size: 0.8rem;
  color: #888;
}

.reply-btn,
.delete-btn {
  background: none;
  border: none;
  font-size: 0.85rem;
  cursor: pointer;
  margin-right: 0.5rem;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.reply-btn {
  color: #1e88e5;
}

.reply-btn:hover {
  background-color: #e3f2fd;
}

.delete-btn {
  color: #e53935;
}

.delete-btn:hover {
  background-color: #ffebee;
}

.reply-form {
  margin-top: 0.75rem;
}

.reply-form textarea {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.9rem;
  resize: vertical;
  font-family: 'Pretendard', sans-serif;
}

.reply-form button {
  margin-top: 0.5rem;
  background-color: #1e88e5;
  color: white;
  border: none;
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reply-form button:hover {
  background-color: #1565c0;
}

.nested-comments {
  margin-left: 1.5rem;
  border-left: 2px solid #e0e0e0;
  padding-left: 1rem;
  margin-top: 1rem;
}
</style>


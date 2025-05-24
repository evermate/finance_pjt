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
  margin-bottom: 1rem;
}

.reply-form textarea {
  width: 100%;
  margin-top: 0.5rem;
}

.nested-comments {
  margin-left: 1rem;
  border-left: 1px solid #ddd;
  padding-left: 1rem;
}
</style>

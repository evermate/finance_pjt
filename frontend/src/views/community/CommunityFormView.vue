<template>
  <div class="form-container">
    <h1 class="form-title">{{ isEdit ? '게시글 수정' : '게시글 작성' }}</h1>

    <form @submit.prevent="submitPost" class="form-box">
      <!-- 게시판 선택 -->
      <div class="form-group">
        <label>게시판 종류</label>
        <select v-model="form.board_type" required>
          <option value="REVIEW">💬 금융상품 리뷰</option>
          <option value="NEWS">📰 금융 뉴스</option>
          <option value="FREE">📝 자유 게시판</option>
        </select>
      </div>

      <!-- 제목 -->
      <div class="form-group">
        <label>제목</label>
        <input
          v-model="form.title"
          required
          placeholder="제목을 입력하세요"
        />
      </div>

      <!-- 내용 -->
      <div class="form-group">
        <label>내용</label>
        <textarea
          v-model="form.content"
          required
          placeholder="내용을 입력하세요"
          rows="6"
        />
      </div>

      <!-- 링크 (뉴스용) -->
      <div class="form-group" v-if="form.board_type === 'NEWS'">
        <label>뉴스 링크</label>
        <input v-model="form.link" type="url" placeholder="https://..." />
      </div>

      <!-- 평점 (리뷰용) -->
      <div class="form-group" v-if="form.board_type === 'REVIEW'">
        <label>평점 (1~5)</label>
        <input
          v-model.number="form.rating"
          type="number"
          min="1"
          max="5"
          placeholder="1~5점 입력"
        />
      </div>

      <button type="submit" class="submit-btn">
        {{ isEdit ? '수정 완료' : '작성 완료' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'

const router = useRouter()
const route = useRoute()
const store = useCommunityStore()

const isEdit = route.name === 'community-edit'
const postId = route.params.id

const form = ref({
  board_type: route.query.board_type || 'REVIEW',
  title: '',
  content: '',
  link: '',
  rating: null,
})

onMounted(async () => {
  if (isEdit) {
    const post = await store.fetchPost(postId)
    if (post) {
      form.value = {
        board_type: post.board_type,
        title: post.title,
        content: post.content,
        link: post.link,
        rating: post.rating,
      }
    } else {
      alert('글 정보를 불러오지 못했습니다.')
      router.push('/community')
    }
  }
})

async function submitPost() {
  const success = isEdit
    ? await store.updatePost(postId, form.value)
    : await store.createPost(form.value)

  if (success) {
    alert(isEdit ? '수정 완료!' : '작성 완료!')
    router.push('/community')
  } else {
    alert('요청 실패. 다시 시도해 주세요.')
  }
}
</script>

<style scoped>
.form-container {
  padding: 2rem;
  max-width: 680px;
  margin: 0 auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
  font-family: 'Pretendard', sans-serif;
}

.form-title {
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
}

.form-box {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
  color: #333;
}

input,
select,
textarea {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  background-color: #fafafa;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #42a5f5;
  background-color: #fff;
}

.submit-btn {
  background-color: #1e88e5;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.submit-btn:hover {
  background-color: #1565c0;
}
</style>

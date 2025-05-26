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

      <!-- 버튼 영역 -->
      <div class="button-group">
        <button type="button" class="cancel-btn" @click="router.back()">취소하기</button>
        <button type="submit" class="submit-btn">{{ isEdit ? '수정 완료' : '작성 완료' }}</button>
      </div>

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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  font-family: 'Pretendard', sans-serif;
}

.form-title {
  font-size: 1.7rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
  color: #222;
}

.form-box {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

input,
select,
textarea {
  width: 100%;
  padding: 0.7rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  background-color: #fafafa;
  transition: all 0.2s ease;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #ff9800;
  box-shadow: 0 0 0 2px rgba(255, 152, 0, 0.2);
  background-color: #fff;
}

.submit-btn {
  background-color: #ff7043;
  color: white;
  border: none;
  padding: 0.8rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-btn:hover {
  background-color: #f4511e;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.cancel-btn,
.submit-btn {
  flex: 1;
  padding: 0.9rem 0;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  max-width: 180px;
}

/* 취소 버튼 스타일 */
.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  border: none;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

/* 작성 버튼 스타일 (기존 오렌지) */
.submit-btn {
  background-color: #ffca28;
  color: #111;
  border: none;
}

.submit-btn:hover {
  background-color: #ffc107;
}

/* 2번 후보
.submit-btn {
  background-color: #4a90e2;
  color: white;
}

.submit-btn:hover {
  background-color: #357ab8;
}

.cancel-btn {
  background-color: #e3e9f1;
  color: #333;
}
.cancel-btn:hover {
  background-color: #d1dbe9;
} */

/* 3번 후보
.submit-btn {
  background-color: #ff6f3c;
  color: white;
}
.submit-btn:hover {
  background-color: #e65c27;
}
.cancel-btn {
  background-color: #f3f4f6;
  color: #333;
}
.cancel-btn:hover {
  background-color: #e0e0e0;
}
 */
@media (prefers-color-scheme: dark) {
  .form-container {
    background-color: #1e1e1e;
    color: #f0f0f0;
  }
  input, textarea, select {
    background-color: #2a2a2a;
    color: #fff;
    border-color: #555;
  }
  .cancel-btn {
    background-color: #333;
    color: #ccc;
  }
  .submit-btn {
    background-color: #ff9800;
    color: #000;
  }
}
</style>

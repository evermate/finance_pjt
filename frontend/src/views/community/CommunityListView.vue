<template>
  <div class="community-container">
    <h1 class="page-title">커뮤니티</h1>

    <!-- 게시판 종류 선택 -->
    <div class="board-type-select">
      <button @click="selectBoard('REVIEW')" :class="{ active: boardType === 'REVIEW' }">
        금융상품 리뷰
      </button>
      <button @click="selectBoard('NEWS')" :class="{ active: boardType === 'NEWS' }">
        금융 뉴스
      </button>
      <button @click="selectBoard('FREE')" :class="{ active: boardType === 'FREE' }">
        자유 게시판
      </button>
    </div>

    <!-- 글쓰기 버튼 -->
    <div class="actions">
      <button class="write-btn" @click="goWrite">글쓰기</button>
    </div>

    <!-- 게시글 목록 -->
    <div v-if="posts.length" class="post-list">
      <ul>
        <li v-for="post in posts" :key="post.id" @click="goDetail(post.id)" class="post-item">
          <span class="badge">{{ boardLabel(post.board_type) }}</span>
          <span class="title">{{ post.title }}</span>
          <span class="author">
            -
            <router-link :to="{ name: 'user-profile', params: { username: post.author } }" class="author-link" @click.stop>
              {{ post.author }}
            </router-link>
          </span>
        </li>
      </ul>
    </div>
    <div v-else class="empty">
      <p>게시글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCommunityStore } from '@/stores/community'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useCommunityStore()
const posts = ref([])
const boardType = ref('REVIEW')  // 기본값: 리뷰 게시판

function boardLabel(type) {
  return {
    REVIEW: '리뷰',
    NEWS: '뉴스',
    FREE: '자유'
  }[type] || type
}

function selectBoard(type) {
  boardType.value = type
  fetchPosts()
}

function goWrite() {
  router.push({
    name: 'community-write',
    query: { board_type: boardType.value }  // 현재 탭 값 전달
  })
}


function goDetail(id) {
  router.push({ name: 'community-detail', params: { id } })
}


async function fetchPosts() {
  posts.value = []
  await store.fetchPosts(boardType.value).then(data => {
    posts.value = data
  })
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.community-container {
  padding: 2rem;
  max-width: 720px;
  margin: 0 auto;
  background-color: #fff;
  font-family: 'Pretendard', sans-serif;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.board-type-select {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.board-type-select button {
  padding: 0.4rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f9f9f9;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.board-type-select button.active {
  background: #1e88e5;
  color: white;
  border-color: #1e88e5;
  font-weight: 600;
}

.board-type-select button:hover {
  background: #e3f2fd;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.write-btn {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  border-radius: 8px;
  background-color: #43a047;
  color: white;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}

.write-btn:hover {
  background-color: #388e3c;
}

.post-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.post-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.badge {
  background-color: #e0f2f1;
  color: #00796b;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.title {
  flex: 1;
  font-weight: 500;
}

.author {
  color: #666;
  font-size: 0.85rem;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.post-item {
  cursor: pointer;
  padding: 0.5rem 0;
  border-bottom: 1px solid #ddd;
}

.post-item:hover {
  background-color: #f9f9f9;
}
.author-link {
  color: #1e88e5;
  text-decoration: none;
}
.author-link:hover {
  text-decoration: underline;
}

</style>

<template>
  <div class="community-container">
    <h1 class="page-title">커뮤니티</h1>

    <!-- 게시방 종류 선택 -->
    <div class="board-type-select">
      <button @click="selectBoard('ALL')" :class="{ active: boardType === 'ALL' }">전체</button>
      <button @click="selectBoard('REVIEW')" :class="{ active: boardType === 'REVIEW' }">금융상품 리뷰</button>
      <button @click="selectBoard('NEWS')" :class="{ active: boardType === 'NEWS' }">금융 뉴스</button>
      <button @click="selectBoard('FREE')" :class="{ active: boardType === 'FREE' }">자유 게시판</button>
    </div>

    <!-- 게시판 종류 선택 위에 검색창 추가 -->
    <div class="search-bar">
      <input v-model="searchKeyword" @keyup.enter="handleSearch" placeholder="검색어를 입력하세요" />
      <button @click="handleSearch">검색</button>
    </div>

    <!-- 게시글 목록 -->
    <div v-if="posts.length" class="post-table-wrapper">
      <table class="post-table">
        <thead>
          <tr>
            <th>번호</th>
            <th>제목</th>
            <th>글쓴이</th>
            <th>날짜</th>
            <th>조회수</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(post, index) in posts" :key="post.id" @click="goDetail(post.id)">
            <td>{{ (totalCount - ((page - 1) * pageSize)) - index }}</td>
            <td class="title-cell">
              <span class="badge" :class="post.board_type.toLowerCase()">{{ boardLabel(post.board_type) }}</span>
              <span class="title">{{ post.title }}</span>
            </td>
            <td>{{ post.author }}</td>
            <td>{{ formatDate(post.created_at) }}</td>
            <td>{{ post.views }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="empty">
      <p>게시글이 없습니다.</p>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page === 1" @click="changePage(1)">처음</button>
      <button :disabled="page === 1" @click="changePage(page - 1)">이전</button>

      <button
        v-for="p in totalPages"
        :key="p"
        @click="changePage(p)"
        :class="{ active: p === page }"
      >
        {{ p }}
      </button>

      <button :disabled="page === totalPages" @click="changePage(page + 1)">다음</button>
      <button :disabled="page === totalPages" @click="changePage(totalPages)">마지막</button>
    </div>

    <!-- 글쓰기 -->
    <div class="write-action">
      <button class="write-btn" @click="goWrite">글쓰기</button>
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
const page = ref(1)
const totalPages = ref(1)
const totalCount = ref(0)
const boardType = ref('ALL')
const pageSize = 10

const searchKeyword = ref('')

async function handleSearch() {
  await fetchPosts(boardType.value, page.value, searchKeyword.value)
}

function boardLabel(type) {
  return {
    ALL: '전체',
    REVIEW: '리뷰',
    NEWS: '뉴스',
    FREE: '자유'
  }[type] || type
}

function selectBoard(type) {
  boardType.value = type
  page.value = 1
  fetchPosts()
}

function goWrite() {
  router.push({
    name: 'community-write',
    query: { board_type: boardType.value }
  })
}

function goDetail(id) {
  router.push({ name: 'community-detail', params: { id } })
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function changePage(p) {
  page.value = p
  fetchPosts()
}

// async function fetchPosts() {
//   const { posts: fetchedPosts, count } = await store.fetchPosts(boardType.value, page.value)
//   posts.value = fetchedPosts
//   totalCount.value = count
//   totalPages.value = Math.ceil(count / pageSize)
// }
async function fetchPosts() {
  const { posts: fetchedPosts, count } = await store.fetchPosts(
    boardType.value,
    page.value,
    searchKeyword.value  // ✅ 검색 키워드 추가 전달
  )
  posts.value = fetchedPosts
  totalCount.value = count
  totalPages.value = Math.ceil(count / pageSize)
}

onMounted(() => {
  fetchPosts()
})
</script>


<style scoped>
.community-container {
  padding: 2rem;
  max-width: 860px;
  margin: 0 auto;
  background-color: #fff;
  font-family: 'Pretendard', sans-serif;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.board-type-select {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.board-type-select button {
  padding: 0.4rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f4f6fa;
  cursor: pointer;
  font-size: 0.95rem;
  color: #333;
}

.board-type-select button.active {
  background: #1976d2;
  color: white;
  border-color: #1976d2;
  font-weight: 600;
}

.board-type-select button:hover {
  background: #e0ecff;
  color: #000;
}

.post-table-wrapper {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.post-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.post-table thead {
  background-color: #f9fafb;
}

.post-table th, .post-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.post-table tbody tr:hover {
  background-color: #f4f7fd;
  cursor: pointer;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
}

.badge.review {
  background-color: #e3f2fd;
  color: #1976d2;
}

.badge.news {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge.free {
  background-color: #fff3e0;
  color: #ef6c00;
}

.write-action {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.write-btn {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  border-radius: 8px;
  background-color: #ff7043;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.write-btn:hover {
  background-color: #f4511e;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #999;
}

/* ✅ 페이지네이션 스타일 */
.pagination {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  gap: 0.4rem;
}

.pagination button {
  padding: 0.4rem 0.8rem;
  border: none;
  background-color: #f0f0f0;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.pagination button.active {
  background-color: #1e88e5;
  color: white;
  font-weight: bold;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 🔍 검색바 스타일 */
.search-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.2rem;
}

.search-bar input {
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 0.95rem;
  width: 220px;
  transition: border-color 0.2s ease;
}

.search-bar input:focus {
  outline: none;
  border-color: #1e88e5;
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
}

.search-bar button {
  background-color: #e0e0e0;
  color: #333;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-bar button:hover {
  background-color: #d5d5d5;
}

</style>

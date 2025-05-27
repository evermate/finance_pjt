<template>
  <!-- ✅ 상단 배너 추가 -->
    <div class="banner-section">
      <img src="/image/community.jpg" alt="커뮤니티" class="banner-img" />
      <div class="banner-text">
        <h2>함께 나누는 금융 이야기</h2>
        <p>금융상품 리뷰부터 자유로운 정보 공유까지, 다양한 이야기를 들려주세요</p>
      </div>
    </div>
  <div class="community-container">
    <!-- 상단: 게시판 필터 + 글쓰기 버튼 -->
    <div class="top-actions">
      <div class="board-type-select">
        <button @click="selectBoard('ALL')" :class="{ active: boardType === 'ALL' }">전체</button>
        <button @click="selectBoard('REVIEW')" :class="{ active: boardType === 'REVIEW' }">금융상품 리뷰</button>
        <button @click="selectBoard('NEWS')" :class="{ active: boardType === 'NEWS' }">금융 뉴스</button>
        <button @click="selectBoard('FREE')" :class="{ active: boardType === 'FREE' }">자유 게시판</button>
      </div>
      <button class="write-btn" @click="goWrite">글쓰기</button>
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

    <!-- 하단: 페이지네이션 + 검색창 -->
    <div class="pagination-wrapper">
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

      <!-- 🔍 검색창 아래에 크게 -->
      <div class="search-bar">
        <input v-model="searchKeyword" @keyup.enter="handleSearch" placeholder="검색어를 입력하세요" />
        <button @click="handleSearch">검색</button>
      </div>
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
  return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

function changePage(p) {
  page.value = p
  fetchPosts()
}

async function fetchPosts() {
  const { posts: fetchedPosts, count } = await store.fetchPosts(
    boardType.value,
    page.value,
    searchKeyword.value
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

.top-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.board-type-select {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.board-type-select button {
  padding: 0.4rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f4f6fa;
  cursor: pointer;
  font-size: 0.95rem;
  color: #333;
  transition: all 0.2s ease-in-out;
}

.board-type-select button.active {
  background: linear-gradient(90deg, #1976d2, #42a5f5);
  color: white;
  font-weight: 700;
  border-color: transparent;
  box-shadow: 0 2px 6px rgba(25, 118, 210, 0.3);
}

.write-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1.4rem;
  font-size: 0.95rem;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease-in-out;
}

.write-btn:hover {
  background-color: #125ea6;
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
  padding: 0.25rem 0.7rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  color: white;
}

.badge.review {
  background-color: #1976d2;
}
.badge.news {
  background-color: #2e7d32;
}
.badge.free {
  background-color: #ef6c00;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #999;
  font-size: 1rem;
  background-color: #f9fafc;
  border: 1px dashed #ccc;
  border-radius: 8px;
  margin-top: 1rem;
}

.pagination-wrapper {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.pagination {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination button {
  padding: 0.4rem 0.8rem;
  border: none;
  background-color: #f0f0f0;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease-in-out;
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

.search-bar {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.search-bar input {
  padding: 0.65rem 1rem;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1rem;
  width: 300px;
}

.search-bar input:focus {
  outline: none;
  border-color: #1e88e5;
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
}

.search-bar button {
  background-color: #455a64;  /* 차콜 그레이 */
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.search-bar button:hover {
  background-color: #263238;
}

@media (max-width: 768px) {
  .search-bar, .top-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .search-bar input {
    width: 100%;
  }

  .pagination {
    justify-content: center;
  }
}
.banner-section {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 2.5rem;
}

.banner-img {
  width: 100%;
  height: 180%;
  object-fit: cover;
  object-position: bottom;
  filter: brightness(0.6);
}

.banner-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 2;
}

.banner-text h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.banner-text p {
  font-size: 1.1rem;
  font-weight: 400;
}
</style>

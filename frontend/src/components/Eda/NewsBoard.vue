<template>
  <section class="news-board">
    <h2 style="text-align: left;">최신 금융 뉴스</h2>

    <!-- 탭 -->
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.value === null ? 'all' : tab.value"
        :class="['tab', { active: selectedTab === tab.value }]" @click="selectTab(tab.value)">
        {{ tab.label }}
      </button>
    </div>

    <!-- 검색 (옵션) -->
    <div class="search-bar">
      <input v-model="searchKeyword" @keyup.enter="handleSearch" placeholder="검색어를 입력하세요" />
      <button @click="handleSearch">검색</button>
    </div>

    <!-- 게시판 테이블 -->
    <table class="board-table">
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
        <tr v-for="post in filteredPosts" :key="post.id">
          <td>{{ post.id }}</td>
          <td class="title-cell">
            <span :class="['badge', post.category]">{{ categoryLabel(post.category) }}</span>
            <a href="javascript:;" @click="openDetail(post)">{{ post.title }}</a>
          </td>
          <td>{{ post.author }}</td>
          <td>{{ post.date }}</td>
          <td>{{ post.views.toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 글쓰기 버튼 -->
    <!-- <div class="write-btn">
      <RouterLink to="/community/write">
        <button>글쓰기</button>
      </RouterLink>
    </div> -->

    <!-- ── 여기에 상세 모달 컴포넌트 넣어 주기 ── -->
    <NewsDetailModal :visible="showDetail" :post="currentPost" @close="showDetail = false" />

  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import NewsDetailModal from './NewsDetailModal.vue'
import { dummyPosts } from '@/data/dummy/news.js'

const posts = ref(dummyPosts)


const tabs = [
  // { label: '전체',           value: null   },
  // { label: '금융상품 리뷰', value: 'review' },
  // { label: '주요 뉴스',     value: 'news'   },
  // { label: '자유 게시판',   value: 'free'   },
]

const selectedTab = ref(null)
const searchQuery = ref('')
const showDetail = ref(false)
const currentPost = ref({})

// 예시 데이터 (실제 API 연동하셔도 됩니다)
// src/components/NewsBoard.vue


// 탭 선택
function selectTab(val) {
  selectedTab.value = val
}

// 검색 (임시 필터)
function onSearch() {
  // 간단히 searchQuery가 제목에 포함된 것만 보여주도록
  // 필요 없으면 지우셔도 됩니다
}

// 각 카테고리의 한글 레이블
function categoryLabel(cat) {
  switch (cat) {
    case 'review': return '리뷰'
    case 'news': return '뉴스'
    case 'free': return '자유'
    default: return ''
  }
}

// 실제로 테이블에 뿌릴 데이터
const filteredPosts = computed(() => {
  let list = posts.value.slice().sort((a, b) => b.id - a.id)
  if (selectedTab.value) {
    list = list.filter(p => p.category === selectedTab.value)
  }
  if (searchQuery.value) {
    list = list.filter(p => p.title.includes(searchQuery.value))
  }
  return list
})

// 제목 클릭
function openDetail(post) {
  post.views += 1                      // ✅ 조회수 증가
  currentPost.value = { ...post }     // ✅ 모달용 상태 갱신
  showDetail.value = true
}
</script>

<style scoped>
.news-board {
  padding: 2rem 1rem;  /* padding을 줄여서 크기 일치 */
  background-color: #f0f6fd;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem; /* margin을 동일하게 설정 */
  /* width: 2120; */
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.tab {
  padding: 0.6rem 1rem;
  border: 1px solid #ccc;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.tab:hover {
  background-color: #f0f0f0;
}

.tab.active {
  background: #2f80ed;
  color: white;
  border-color: #2f80ed;
}

.search-bar {
  display: flex;
  justify-content: right;
  flex-wrap: wrap;
  gap: 0.6rem;
}


.search input {
  padding: 0.4rem 0.6rem;
}
.search-bar input {
  padding: 0.65rem 1rem;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1rem;
  width: 300px;
}

.search button {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ccc;
  border-left: none;
  border-radius: 0 4px 4px 0;
  background: #2f80ed;
}
.search-bar input:focus {
  outline: none;
  border-color: #1e88e5;
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
}

.search-bar button {
  background-color: #455a64;
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

.board-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
}


.board-table th,
.board-table td {
  padding: 0.75rem 0.5rem;
}
.board-table th, .board-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 1rem;
}

.board-table th {
  font-weight: 700;
  color: #333;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge {
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  font-size: 0.85rem;
  color: white;
}


.badge.review { background: #3b82f6; } /* 파랑 */
.badge.news   { background: #10b981; } /* 초록 */
.badge.free   { background: #6b7280; } /* 회색 */

.title-cell a {
  color: #333;
  text-decoration: none;
  font-weight: 600;
}

.title-cell a:hover {
  text-decoration: underline;
}

/* 글쓰기 버튼 */
.write-btn {
  text-align: right;
}

.write-btn button {
  padding: 0.6rem 1.2rem;
  background: #2f80ed;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

</style>

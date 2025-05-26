<template>
  <section class="search-wrapper">
    <!-- 상단 검색 카드 -->
    <div class="search-card">
      <h1 style="text-align: center;">📺 관심 종목 검색</h1>
      <p style="text-align: center;">주식/경제 관련 유튜브 영상을 빠르게 찾아보세요</p>

      <div class="search-bar">
        <input
          v-model="query"
          @keyup.enter="onSearch"
          placeholder="검색어를 입력하세요 (예: 삼성전자)"
        />
        <button @click="onSearch" :disabled="youtubeStore.loading">
          {{ youtubeStore.loading ? '검색 중…' : '검색' }}
        </button>
      </div>

      <div class="sort-bar" v-if="youtubeStore.videos.length">
        <label>정렬:</label>
        <select v-model="sortOption">
          <option value="date">최신순</option>
          <option value="viewCount">조회수순</option>
          <option value="title">제목순</option>
        </select>
      </div>

      <p v-if="youtubeStore.error" class="error">
        오류 발생: {{ youtubeStore.error.message }}
      </p>

      <LoadingSpinner v-if="youtubeStore.loading" class="mx-auto my-4" />
    </div>

    <!-- 검색 결과 카드 -->
    <div v-if="youtubeStore.videos.length" class="result-card">
      <div class="video-grid">
        <div
          v-for="item in sortedVideos"
          :key="item.id.videoId"
          class="video-card"
        >
          <RouterLink
            :to="{ name: 'video-detail', params: { id: item.id.videoId } }"
            class="video-card-link"
          >
            <div class="thumbnail-wrapper">
              <img :src="item.snippet.thumbnails.high.url" class="thumbnail" />
              <div class="play-overlay">▶</div>
            </div>
            <div class="video-info">
              <h3 class="video-title">{{ item.snippet.title }}</h3>
              <p class="channel">{{ item.snippet.channelTitle }}</p>
              <p class="date">{{ item.snippet.publishedAt.slice(0, 10) }}</p>
            </div>
          </RouterLink>
        </div>
      </div>

            <!-- 페이지네이션 (숫자 기반) -->
      <div v-if="totalPages > 1" class="pagination">
        <!-- <button @click="goToPage(1)" :disabled="currentPage === 1">처음</button> -->
        <button @click="prevPage" :disabled="currentPage === 1">이전</button>

        <button
          v-for="page in pageNumbers"
          :key="page"
          @click="goToPage(page)"
          :class="['page-btn', { active: page === currentPage }]"
        >
          {{ page }}
        </button>

        <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
        <!-- <button @click="goToPage(totalPages)" :disabled="currentPage === totalPages">마지막</button> -->
      </div>
    </div>
    <p v-else-if="!youtubeStore.loading" class="no-result">검색 결과가 없습니다.</p>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { useYoutubeStore } from '@/stores/youtube'

const youtubeStore = useYoutubeStore()
const query = ref('')
const currentPage = ref(1)
const perPage = 6
const sortOption = ref('date')

const totalPages = computed(() => Math.ceil(youtubeStore.videos.length / perPage))
const sortedVideos = computed(() => {
  const sorted = [...youtubeStore.videos]
  if (sortOption.value === 'viewCount') {
    sorted.sort((a, b) => (b.statistics?.viewCount || 0) - (a.statistics?.viewCount || 0))
  } else if (sortOption.value === 'title') {
    sorted.sort((a, b) => a.snippet.title.localeCompare(b.snippet.title))
  } else {
    sorted.sort((a, b) => new Date(b.snippet.publishedAt) - new Date(a.snippet.publishedAt))
  }
  const start = (currentPage.value - 1) * perPage
  return sorted.slice(start, start + perPage)
})

const pageNumbers = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages
})

function onSearch() {
  const q = query.value.trim()
  if (!q) return
  currentPage.value = 1
  youtubeStore.searchVideos(q)
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}
function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>

<style scoped>
.search-wrapper {
  max-width: 1024px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Pretendard', sans-serif;
}

.search-card, .result-card {
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  padding: 2rem;
  margin-bottom: 2rem;
}

.search-card h1 {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #1a237e;
}
.search-card p {
  color: #555;
  margin-bottom: 1.5rem;
}

.search-bar {
  display: flex;
  gap: 0.5rem;
  max-width: 600px;
  margin: 0 auto 1rem;
  justify-content: center;
}
.search-bar input {
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.search-bar button {
  padding: 0.75rem 1.2rem;
  background: #0074ff;
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.search-bar button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.sort-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;

  /* ✅ 중앙 제한 삭제 */
  max-width: none;
  margin-left: 0;
  margin-right: 0;
}

.sort-bar select {
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.error {
  color: #c00;
  text-align: center;
  margin-top: 1rem;
}

.no-result {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 2rem;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.video-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease;
  position: relative;
}
.video-card:hover {
  transform: translateY(-6px);
}

.thumbnail-wrapper {
  position: relative;
}
.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 2rem;
  padding: 0.3rem 0.8rem;
  border-radius: 50%;
  pointer-events: none;
}

.thumbnail {
  width: 100%;
  height: auto;
  display: block;
}

.video-info {
  padding: 1rem;
}
.video-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}
.channel, .date {
  font-size: 0.85rem;
  color: #777;
  margin: 0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.4rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.pagination button {
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  background: #f8f9fa;
  cursor: pointer;
  font-size: 0.95rem;
  min-width: 2.5rem;
}

.pagination button.active,
.pagination .page-btn.active {
  background: #007bff;
  color: white;
  font-weight: bold;
  border: none;
}

.pagination button:disabled {
  background-color: #eee;
  color: #aaa;
  cursor: not-allowed;
}
.video-card-link {
  text-decoration: none;
  color: inherit;
}
</style>

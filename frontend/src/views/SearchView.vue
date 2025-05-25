<template>
  <section class="search-container">
    <h1>관심 종목 영상 검색</h1>

    <!-- 검색 바 -->
    <div class="search-bar">
      <input
        v-model="query"
        @keyup.enter="onSearch"
        placeholder="검색어를 입력하세요"
      />
      <button @click="onSearch" :disabled="youtubeStore.loading">
        {{ youtubeStore.loading ? '검색 중…' : '검색' }}
      </button>
    </div>

    <!-- 에러 메시지 -->
    <p v-if="youtubeStore.error" class="error">
      오류 발생: {{ youtubeStore.error.message }}
    </p>

    <!-- 로딩 스피너 -->
    <LoadingSpinner v-if="youtubeStore.loading" class="mx-auto my-4" />

    <!-- 결과 그리드 -->
    <div v-if="youtubeStore.videos.length" class="video-grid">
      <div
        v-for="item in youtubeStore.videos"
        :key="item.id.videoId"
        class="video-card"
      >
        <!-- AFTER (앱 내부의 상세 페이지로 이동) -->
        <RouterLink
          :to="{ name: 'video-detail', params: { id: item.id.videoId } }"
          class="video-card-link"
        >
  <img :src="item.snippet.thumbnails.medium.url" />
  <h3>{{ item.snippet.title }}</h3>
</RouterLink>

        <p class="channel">{{ item.snippet.channelTitle }}</p>
        <p class="date">{{ item.snippet.publishedAt.slice(0,10) }}</p>
      </div>
    </div>

    <!-- 결과 없을 때 안내 -->
    <p v-else-if="!youtubeStore.loading">검색 결과가 없습니다.</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { useYoutubeStore } from '@/stores/youtube'

const youtubeStore = useYoutubeStore()
const query = ref('')

// 검색 실행
function onSearch() {
  const q = query.value.trim()
  if (!q) return
  youtubeStore.searchVideos(q)
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.search-bar input {
  flex:1;
  padding:0.5rem;
  border:1px solid #ccc;
  border-radius:4px;
}
.search-bar button {
  padding:0.5rem 1rem;
  background:#0074ff;
  color:#fff;
  border:none;
  border-radius:4px;
  cursor:pointer;
}
.error {
  color: #c00;
}
.video-grid {
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(240px,1fr));
  gap:1rem;
}
.video-card {
  background:#fff;
  padding:1rem;
  border-radius:6px;
  box-shadow:0 2px 8px rgba(0,0,0,0.1);
}
.video-card img {
  width:100%;
  border-radius:4px;
}
.video-card h3 {
  font-size:1rem;
  margin:0.5rem 0;
}
.channel, .date {
  font-size:0.85rem;
  color:#666;
}
</style>

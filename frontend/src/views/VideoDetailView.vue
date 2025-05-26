<template>
  <section class="video-detail-wrapper">
    <div class="inner-card">
      <button @click="goBack" class="back-btn">
        <span>←</span>검색으로 돌아가기
      </button>

      <div v-if="youtube.loading" class="center">
        <LoadingSpinner message="동영상 상세 정보 불러오는 중..." />
      </div>

      <div v-else-if="youtube.detail" class="detail-card">
        <!-- 영상 플레이어 -->
        <div class="player-box">
          <iframe
            :src="`https://www.youtube.com/embed/${videoId}`"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen
            class="player"
          ></iframe>
        </div>

        <!-- 영상 정보 -->
        <div class="info-box">
          <h1>{{ youtube.detail.snippet.title }}</h1>
          <p class="meta">
            채널: {{ youtube.detail.snippet.channelTitle }} ｜ 게시일: {{ youtube.detail.snippet.publishedAt.slice(0,10) }}
          </p>
          <p class="stats">
            조회수: {{ Number(youtube.detail.statistics.viewCount).toLocaleString() }}회 ｜ 좋아요: {{ Number(youtube.detail.statistics.likeCount).toLocaleString() }}개
          </p>
          <div class="description">
            <h3>설명</h3>
            <p>{{ youtube.detail.snippet.description }}</p>
          </div>
        </div>
      </div>

      <p v-else-if="youtube.error" class="error">
        상세 정보를 불러오지 못했습니다: {{ youtube.error.message }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { useYoutubeStore } from '@/stores/youtube'

const route = useRoute()
const router = useRouter()
const videoId = route.params.id
const youtube = useYoutubeStore()

onMounted(() => {
  youtube.fetchVideoDetail(videoId)
})

function goBack() {
  router.push({ name: 'search' })
}
</script>

<style scoped>
.video-detail-wrapper {
  max-width: 960px;
  margin: 2rem auto;
  padding: 1rem;
}

.inner-card {
  background: #f3f6fd;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}

.detail-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.player-box {
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.player {
  width: 100%;
  height: 480px;
  border: none;
}

.info-box h1 {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #222;
}

.meta,
.stats {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 0.4rem;
}

.description {
  margin-top: 1rem;
}
.description h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}
.description p {
  white-space: pre-line;
  color: #444;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: white;
  background-color: #60a5fa;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-bottom: 1.2rem;
}

.back-btn:hover {
  background-color: #3b82f6; /* hover 시 조금 더 진하게 */
}

.back-btn:focus {
  outline: 2px solid #94a3b8;
}

.error {
  color: red;
  margin-top: 2rem;
}

.center {
  text-align: center;
  margin-top: 2rem;
}
</style>

<template>
  <section class="video-detail">
    <button @click="goBack" class="back-btn">← 검색으로 돌아가기</button>

    <div v-if="youtube.loading" class="center">
      <LoadingSpinner message="동영상 상세 정보 불러오는 중..." />
    </div>

    <div v-else-if="youtube.detail" class="detail-card">
      <!-- 1) iframe 플레이어 -->
      <iframe
        :src="`https://www.youtube.com/embed/${videoId}`"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen
        class="player"
      ></iframe>

      <!-- 2) 영상 정보 -->
      <h1>{{ youtube.detail.snippet.title }}</h1>
      <p class="meta">
        채널: {{ youtube.detail.snippet.channelTitle }}
        ｜ 게시일: {{ youtube.detail.snippet.publishedAt.slice(0,10) }}
      </p>
      <p class="stats">
        조회수: {{ youtube.detail.statistics.viewCount }}회
        ｜ 좋아요: {{ youtube.detail.statistics.likeCount }}개
      </p>
      <div class="description">
        <h3>설명</h3>
        <p>{{ youtube.detail.snippet.description }}</p>
      </div>
    </div>

    <p v-else-if="youtube.error" class="error">
      상세 정보를 불러오지 못했습니다: {{ youtube.error.message }}
    </p>
  </section>
</template>

<script setup>
import { onMounted }        from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LoadingSpinner      from '@/components/LoadingSpinner.vue'
import { useYoutubeStore } from '@/stores/youtube'

const route     = useRoute()
const router    = useRouter()
const videoId   = route.params.id   // URL param
const youtube   = useYoutubeStore()

onMounted(() => {
  youtube.fetchVideoDetail(videoId)
})

function goBack() {
  router.push({ name: 'search' })
}
</script>

<style scoped>
.back-btn { margin-bottom: 1rem; }
.player {
  width: 100%; height: 480px; border-radius: 8px; margin-bottom: 1rem;
}
.detail-card h1 { font-size: 1.5rem; margin-bottom: 0.5rem; }
.meta, .stats { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
.description { margin-top: 1rem; }
.error { color: red; }
.center { text-align: center; margin-top: 2rem; }
</style>

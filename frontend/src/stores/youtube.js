// src/stores/youtube.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useYoutubeStore = defineStore('youtube', () => {
  const videos  = ref([])
  const detail  = ref(null)
  const loading = ref(false)
  const error   = ref(null)

  /** YouTube API 호출 */
  async function searchVideos(query) {
    loading.value = true
    error.value   = null
    try {
      const res = await axios.get('/api/youtube/search/', { params: { q: query } })
      // YouTube Search API의 items 배열을 담습니다
      videos.value = res.data.items || []
    } catch (err) {
      error.value  = err
      videos.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchVideoDetail(id) {
    loading.value = true; error.value = null; detail.value = null
    try {
      const res = await axios.get('/api/youtube/video-detail/', { params:{ id } })
      detail.value = res.data
    } catch (err) {
      error.value = err; detail.value = null
    } finally { loading.value = false }
  }

  return { videos, detail, loading, error, searchVideos, fetchVideoDetail }
})

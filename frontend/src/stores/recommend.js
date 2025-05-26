// src/stores/recommend.js
import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useRecommendStore = defineStore('recommend', () => {
  // ✅ 일반 추천 상태
  const recommendations = ref([])
  const loading = ref(false)
  const error = ref(null)

  // ✅ AI 추천 상태 (추가)
  const aiAsset = ref(0)
  const aiRecs = ref([])
  const aiLoading = ref(false)
  const aiError = ref(null)

  /**
   * 로그인 사용자 프로필 기반 금리 추천 API 호출
   * @param {number} asset  사용자 자산 (원 단위)
   * @param {number} top_n  추천 개수 (기본값 10)
   */
  async function fetchByProfile(asset, top_n = 10) {
    loading.value = true
    error.value = null
    try {
      const res = await axios.get(
        '/api/products/recommends/recommend_by_profile/',
        { params: { asset, top_n } }
      )
      recommendations.value = res.data
      console.log('추천 결과:', recommendations.value)
    } catch (err) {
      error.value = err
      recommendations.value = []
    } finally {
      loading.value = false
    }
  }

  /**
   * ✅ AI 추천 API 호출
   */
  async function fetchAiRecommend() {
    aiLoading.value = true
    aiError.value = null
    try {
      const res = await axios.get('/api/products/ai-recommend/', {
        params: { asset: aiAsset.value }
      })
      aiRecs.value = res.data
    } catch (err) {
      aiError.value = err
      aiRecs.value = []
    } finally {
      aiLoading.value = false
    }
  }

  function resetAll() {
  recommendations.value = []
  error.value = null
  aiAsset.value = 0
  aiRecs.value = []
  aiError.value = null
}

  return {
    // 일반 추천 관련
    recommendations,
    loading,
    error,
    fetchByProfile,

    // ✅ AI 추천 관련
    aiAsset,
    aiRecs,
    aiLoading,
    aiError,
    fetchAiRecommend,
    resetAll
  }
})

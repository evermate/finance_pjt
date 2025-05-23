// src/stores/recommend.js
import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useRecommendStore = defineStore('recommend', () => {
  // 추천 결과 목록
  const recommendations = ref([])
  // 로딩 상태
  const loading = ref(false)
  // 에러 객체
  const error = ref(null)

  /**
   * 로그인 사용자 프로필 기반 금리 추천 API 호출
   * @param {number} asset  사용자 자산 (원 단위)
   * @param {number} top_n  추천 개수 (기본값 5)
   */
  async function fetchByProfile(asset, top_n = 5) {
    loading.value = true
    error.value = null

    try {
      // axios.defaults.baseURL 과
      // axios.defaults.headers.common['Authorization'] 은
      // main.js 와 accounts 스토어에서 이미 세팅되어 있다고 가정
      const res = await axios.get(
        '/api/products/deposits/recommend_by_profile/',
        {
          params: { asset, top_n }
        }
      )
      recommendations.value = res.data
    } catch (err) {
      error.value = err
      recommendations.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    recommendations,
    loading,
    error,
    fetchByProfile
  }
})

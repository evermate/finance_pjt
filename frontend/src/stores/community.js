import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useCommunityStore = defineStore('community', () => {
  const posts = ref([])
  const pageInfo = ref({})
  /**
   * 게시글 목록 가져오기
   * @param {string} boardType - 'REVIEW' | 'NEWS' | 'FREE'
   * @returns {Promise<Array>} 게시글 배열
   */


  async function fetchPosts(boardType = 'ALL', page = 1, search = '') {
    try {
      const params = { page }
      if (boardType !== 'ALL') {
        params.board_type = boardType
      }
      if (search) params.search = search

      const response = await axios.get('/api/community/posts/', { params })
      posts.value = response.data.results
      pageInfo.value = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous
      }
      return {
        posts: posts.value,
        count: response.data.count
      }
    } catch (error) {
      console.error('게시글 조회 실패:', error)
      posts.value = []
      pageInfo.value = {}
      return {
        posts: [],
        count: 0
      }
    }
  }


  async function createPost(postData) {
    const token = localStorage.getItem('authToken')  

    if (!token) {
      alert('로그인 후 작성 가능합니다.')
      return false
    }

    try {
      const response = await axios.post('/api/community/posts/', postData, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      return true
    } catch (error) {
      console.error('게시글 작성 실패:', error)
      return false
    }
  }


  async function fetchPost(id) {
    try {
      const res = await axios.get(`/api/community/posts/${id}/`)
      return res.data
    } catch (err) {
      console.error('게시글 조회 실패:', err)
      return null
    }
  }

  async function deletePost(id) {
    try {
      const token = localStorage.getItem('authToken')
      if (!token) {
        alert('로그인 후 삭제 가능합니다.')
        return false
      }
      await axios.delete(`/api/community/posts/${id}/`, {
        headers: { Authorization: `Token ${token}` }
      })
      return true
    } catch (err) {
      console.error('삭제 실패:', err)
      return false
    }
  }
  async function updatePost(id, postData) {
    try {
      const token = localStorage.getItem('authToken')
      if (!token) {
        alert('로그인 후 수정 가능합니다.')
        return false
      }
      await axios.put(`/api/community/posts/${id}/`, postData, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      return true
    } catch (error) {
      console.error('수정 실패:', error)
      return false
    }
  }


  return {
    posts,
    pageInfo,
    fetchPosts,
    fetchPost,
    createPost,
    deletePost,
    updatePost,
  }
})

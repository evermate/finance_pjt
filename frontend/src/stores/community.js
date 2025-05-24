import { defineStore } from 'pinia'
import axios from 'axios'

export const useCommunityStore = defineStore('community', () => {
  /**
   * 게시글 목록 가져오기
   * @param {string} boardType - 'REVIEW' | 'NEWS' | 'FREE'
   * @returns {Promise<Array>} 게시글 배열
   */
  async function fetchPosts(boardType) {
    try {
      const response = await axios.get(`/api/community/posts/?board_type=${boardType}`)
      return response.data  // 배열 형태 기대
    } catch (error) {
      console.error('게시글 조회 실패:', error)
      return []
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
      const token = localStorage.getItem('token')
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
    fetchPosts,
    fetchPost,
    createPost,
    deletePost,
    updatePost,
  }
})

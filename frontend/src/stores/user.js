// stores/user.js
import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL } from '@/const/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),
  actions: {
    async register(payload) {
      try {
        const res = await axios.post(`${API_URL}/registration/`, payload)
        console.log('회원가입 성공:', res.data)
      } catch (err) {
        console.error('회원가입 실패:', err.response.data)
        throw err
      }
    },
    async login(payload) {
      try {
        const res = await axios.post(`${API_URL}/login/`, payload)
        this.token = res.data.access
        localStorage.setItem('token', this.token)
        await this.fetchUser()
      } catch (err) {
        console.error('로그인 실패:', err.response.data)
        throw err
      }
    },
    async fetchUser() {
      try {
        const res = await axios.get(`${API_URL}/user/`, {
          headers: { Authorization: `Bearer ${this.token}` },
        })
        this.user = res.data
      } catch (err) {
        console.error('유저 정보 불러오기 실패:', err.response?.data)
      }
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
    },
  },
})

// store/accounts.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'

  const token = ref(null)
  const user = ref(null)

  // ✅ 회원가입
  const signUp = ({ username, age, email, password1, password2 }) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: { username, age, email, password1, password2 }
    })
      .then(() => {
        console.log('회원가입 성공!')
      })
      .catch(err => console.error('회원가입 실패:', err))
  }

  // ✅ 로그인
  const logIn = ({ username, password }) => {
    console.log('로그인 요청 중...', username, password)  // ✅ 이 줄 추가
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/login/`,
      data: { username, password }
    })
      .then(res => {
        console.log(res)
        token.value = res.data.key
        fetchUser() 
      })
      .catch(err => console.error('로그인 실패:', err))
  }

  // ✅ 유저 정보 요청
  const fetchUser = () => {
    axios({
      method: 'GET',
      url: `${ACCOUNT_API_URL}/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        console.log('✅ 유저 정보:', res.data)
        user.value = res.data
      })
      .catch(err => console.error('유저 정보 불러오기 실패:', err))
  }

  // ✅ 로그아웃
  const logout = () => {
    token.value = null
    user.value = null
  }

  // ✅ 로그인 여부
  const isLoggedIn = computed(() => !!token.value)

  return {
    signUp,
    logIn,
    fetchUser,
    logout,
    token,
    user,
    isLoggedIn,
  }
}, { persist: true })

// store/accounts.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const router = useRouter()

  const token = ref(null)
  const user = ref(null)

  // ✅ 회원가입
  const signUp = ({ username, birth_date, email, password1, password2 }) => {
    axios({
      method: 'POST',
      url: `${ACCOUNT_API_URL}/signup/`,
      data: { username, birth_date, email, password1, password2 }
    })
      .then(() => {
        alert('회원가입이 완료되었습니다!')
        router.push({ name: 'home' })
      })
      .catch(err => {
        console.error('회원가입 실패:', err)
        alert('회원가입에 실패했습니다. 다시 시도해주세요.')
      })
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
      url: `${ACCOUNT_API_URL}/mypage/`,  // 🔄 수정된 URL
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
    router.push('/')
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

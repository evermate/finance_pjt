// src/stores/accounts.js
import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = '/accounts'
  const router = useRouter()

  // 1) state
  const token = ref(localStorage.getItem('authToken') || null)
  const user = ref(null)
  const isLoggedIn = computed(() => !!token.value)

  // 2) 회원가입
  const signUp = async ({ username, birth_date, email, password1, password2 }) => {
    try {
      await axios.post(`${ACCOUNT_API_URL}/signup/`, {
        username, birth_date, email, password1, password2
      })
      alert('회원가입이 완료되었습니다!')
      router.push({ name: 'login' })
    } catch (err) {
      console.error('회원가입 실패:', err)
      alert('회원가입에 실패했습니다. 다시 시도해주세요.')
    }
  }

  // 3) 로그인
  const logIn = async ({ username, password }) => {
    try {
      const res = await axios.post(`${ACCOUNT_API_URL}/login/`, {
        username, password
      })
      token.value = res.data.key
      localStorage.setItem('authToken', token.value)
      axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
      await fetchUser()             // ← 이 호출도 이후에 정의된 fetchUser를 가리키게 됩니다.
      router.push({ name: 'home' })
    } catch (err) {
      console.error('로그인 실패:', err)
      alert('로그인에 실패했습니다. 아이디/비밀번호를 확인하세요.')
    }
  }

  // 4) 유저 정보 요청
  const fetchUser = async () => {
    try {
      const res = await axios.get(`${ACCOUNT_API_URL}/mypage/`)
      user.value = res.data
    } catch (err) {
      console.error('유저 정보 불러오기 실패:', err)
    }
  }

  // ✅ 4-1) 금융상품 가입 함수
  const joinProduct = async (productId) => {
    try {
      await axios.post(`${ACCOUNT_API_URL}/join-product/`, {
        product_id: productId
      }, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      alert('가입이 완료되었습니다.')
      await fetchUser()  // 가입 목록 갱신
    } catch (err) {
      if (err.response?.status === 404) {
        alert('상품을 찾을 수 없습니다.')
      } else {
        alert('가입 처리 중 오류가 발생했습니다.')
      }
      console.error(err)
    }
  }

  // 5) 로그아웃
  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('authToken')
    delete axios.defaults.headers.common['Authorization']
    router.push({ name: 'login' })
  }

  // 6) 토큰 동기화용 watch
  watch(token, (newVal) => {
    if (!newVal) localStorage.removeItem('authToken')
  })

  // 7) **함수 선언 이후에** 초기 토큰 체크 & 자동 로그인
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
    fetchUser()
  }

  return {
    token,
    user,
    isLoggedIn,
    signUp,
    logIn,
    fetchUser,
    logout,
    joinProduct,
  }
}, {
  persist: true,
})

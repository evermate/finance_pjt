// src/stores/accounts.js
import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useModalStore } from '@/stores/modal'

export const useAccountStore = defineStore('account', () => {
  const ACCOUNT_API_URL = '/accounts'
  const router = useRouter()

  // 1) state
  const token = ref(localStorage.getItem('authToken') || null)
  const user = ref(null)
  const isLoggedIn = computed(() => !!token.value)
  const modal = useModalStore()

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
      console.log('유저 정보:', user.value)
    } catch (err) {
      console.error('유저 정보 불러오기 실패:', err)
    }
  }

  // ✅ 4-1) 금융상품 가입 함수
  const joinProduct = async (productId, optionId, productName = '') => {
    console.log('joinProduct called with:', productId, optionId)

    const confirmJoin = await modal.open({
      title: `${productName}`,
      description: '이 상품에 가입할까요?',
      confirmText: '지금 가입',
      cancelText: '돌아가기',
    })
    if (!confirmJoin) return  // 사용자가 취소한 경우

    try {
      await axios.post(`${ACCOUNT_API_URL}/join-product/`, {
        product_id: productId,
        option_id: optionId
      }, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      await fetchUser()
    } catch (err) {
      if (err.response?.status === 403) {
        await modal.open({
          title: '제한 초과',
          description: '가입 가능한 상품은 최대 5개입니다.',
          confirmText: '확인',
          cancelText: null,
        })
      } else if (err.response?.status === 404) {
        await modal.open({
          title: '상품 없음',
          description: '상품을 찾을 수 없습니다.',
          confirmText: '확인',
          cancelText: null,
        })
      } else {
        await modal.open({
          title: '가입 오류',
          description: '가입 처리 중 오류가 발생했습니다.',
          confirmText: '확인',
          cancelText: null,
        })
      }
      console.error(err)
    }
  }


  // ✅ 4-2) 금융상품 탈퇴 함수
  const leaveProduct = async (productId, optionId, productName = '') => {
    const confirmLeave = await modal.open({
      title: `${productName}`,
      description: '이 상품의 가입을 취소할까요?',
      confirmText: '가입 취소',
      cancelText: '계속 유지',
    })
    if (!confirmLeave) return  // 사용자가 취소한 경우

    try {
      await axios.delete(`${ACCOUNT_API_URL}/leave-product/`, {
        data: { product_id: productId, option_id: optionId },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      await fetchUser()
    } catch (err) {
      await modal.open({
        title: '취소 실패',
        description: '가입 취소 중 오류가 발생했습니다.',
        confirmText: '확인',
        cancelText: null,
      })
      console.error(err)
    }
  }

  // ✅ 4-3) 가입한 금융상품 목록
  // 이 computed 속성은 user가 로드된 후에만 유효합니다.
  // 따라서 user가 null이 아닐 때만 접근해야 합니다.
  // 만약 user가 null이라면 빈 배열을 반환합니다.
  const joinedProducts = computed(() => {
    return user.value?.joined_products || []
  })

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
    leaveProduct,
    joinedProducts,
  }
}, {
  persist: true,
})

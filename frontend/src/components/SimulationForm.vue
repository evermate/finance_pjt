<!-- src/components/SimulationForm.vue -->
<template>
  <form @submit.prevent="submit" class="simulation-form">
    <!-- 시작 나이 -->
    <div class="form-group">
      <label for="start_age">시작 나이</label>
      <input
        id="start_age"
        v-model="form.start_age"
        type="number"
        :placeholder="'입력예시: ' + defaultStartAge"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 은퇴 나이 -->
    <div class="form-group">
      <label for="retirement_age">은퇴 나이</label>
      <input
        id="retirement_age"
        v-model="form.retirement_age"
        type="number"
        :placeholder="'입력예시: '+ '60'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 종료 나이 -->
    <div class="form-group">
      <label for="end_age">종료 나이</label>
      <input
        id="end_age"
        v-model="form.end_age"
        type="number"
        :placeholder="'입력예시: ' + '100'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 현재 자산 -->
    <div class="form-group">
      <label for="initial_assets">현재 자산 (원)</label>
      <input
        id="initial_assets"
        v-model="form.initial_assets"
        type="number"
        :placeholder="'입력예시: ' + '10000'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 연간 저축액 -->
    <div class="form-group">
      <label for="initial_savings">연간 저축액 (원)</label>
      <input
        id="initial_savings"
        v-model="form.initial_savings"
        type="number"
        :placeholder="'입력예시: '+'12000000'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 저축 성장률 -->
    <div class="form-group">
      <label for="savings_growth_rate">저축 성장률 (%)</label>
      <input
        id="savings_growth_rate"
        v-model="form.savings_growth_rate"
        type="number"
        step="0.01"
        :placeholder="'입력예시: '+'0.02'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 기대 수익률 -->
    <div class="form-group">
      <label for="mean_return">기대 수익률 (%)</label>
      <input
        id="mean_return"
        v-model="form.mean_return"
        type="number"
        step="0.01"
        :placeholder="'입력예시: ' + '0.12'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 연간 지출 -->
    <div class="form-group">
      <label for="annual_expense">연간 지출 (원)</label>
      <input
        id="annual_expense"
        v-model="form.annual_expense"
        type="number"
        :placeholder="'입력예시: '+'50000000'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <!-- 시뮬레이션 횟수 -->
    <div class="form-group">
      <label for="n_simulations">시뮬레이션 횟수</label>
      <input
        id="n_simulations"
        v-model="form.n_simulations"
        type="number"
        :placeholder="'입력예시: ' + '1000'"
        class="w-full border rounded px-3 py-2"
      />
    </div>

    <div class="form-actions">
      <button type="submit" :disabled="loading">
        {{ loading ? '시뮬레이션 실행 중…' : '시뮬레이션 실행' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, computed, onMounted } from 'vue'
import { useSimulationStore } from '@/stores/simulation.js'
import { useAccountStore }    from '@/stores/accounts.js'

const store         = useSimulationStore()
const accountStore = useAccountStore()

// 계정에서 birth_date로부터 계산한 사용자 나이
const defaultStartAge = computed(() => {
  const bd = accountStore.user?.birth_date  // "YYYY-MM-DD"
  if (!bd) return 26
  const [y,m,d] = bd.split('-').map(Number)
  const today = new Date()
  let age = today.getFullYear() - y
  if (
    today.getMonth()+1 < m ||
    (today.getMonth()+1===m && today.getDate()<d)
  ) age--
  return age
})

const form = reactive({
  start_age:           '',  // 빈 문자열로 두면 placeholder가 보입니다
  retirement_age:      '',
  end_age:             '',
  initial_assets:      '',
  initial_savings:     '',
  savings_growth_rate: '',
  mean_return:         '',
  annual_expense:      '',
  n_simulations:       ''
})

onMounted(() => {
  // 컴포넌트 로드 시 placeholder 대체용으로 폼 값도 세팅
  form.start_age           = defaultStartAge.value
  form.savings_growth_rate = 0.02
  form.mean_return         = 0.12
  form.annual_expense      = 50000000
  form.n_simulations       = 1000
})

 function submit() {
   // 1) 빈 값 검증
   const keys = [
     'start_age','retirement_age','end_age',
     'initial_assets','initial_savings',
     'savings_growth_rate','mean_return',
     'annual_expense','n_simulations'
   ]
   for (const k of keys) {
     if (form[k] === '' || isNaN(Number(form[k]))) {
       alert('모든 항목을 입력해주세요.')
       return
     }
   }

   // 2) 논리적 순서 검증 (옵션)
   if (Number(form.start_age) >= Number(form.retirement_age)) {
     alert('은퇴 나이는 시작 나이보다 커야 합니다.')
     return
   }
   if (Number(form.retirement_age) >= Number(form.end_age)) {
     alert('종료 나이는 은퇴 나이보다 커야 합니다.')
     return
   }

   // 3) 모두 통과했으면 API 호출
   store.run({
     start_age:           Number(form.start_age),
     retirement_age:      Number(form.retirement_age),
     end_age:             Number(form.end_age),
     initial_assets:      Number(form.initial_assets),
     initial_savings:     Number(form.initial_savings),
     savings_growth_rate: Number(form.savings_growth_rate),
     mean_return:         Number(form.mean_return),
     annual_expense:      Number(form.annual_expense),
     n_simulations:       Number(form.n_simulations),
   })
 }
</script>

<style scoped>
.simulation-form {
  /* 전체 최대 폭 & 가운데 정렬 */
  max-width: 800px;
  margin: 0 auto;
  /* 2컬럼 그리드, 최소 260px, 자동 맞춤 */
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}
.form-group label {
  margin-bottom: 0.25rem;
  font-weight: 500;
}
.form-group input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  /* 마지막 버튼 블록은 2컬럼 모두 차지 */
  grid-column: 1 / -1;
  text-align: center;
  margin-top: 0.5rem;
}

.form-actions button {
  padding: 0.75rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}
.form-actions button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}
.form-actions button:not(:disabled):hover {
  background-color: #2563eb;
}
</style>

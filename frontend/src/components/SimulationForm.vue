<!-- src/components/SimulationForm.vue -->
<template>
  <form @submit.prevent="submit" class="simulation-form">
    <div class="form-group">
      <label for="start_age">시작 나이</label>
      <input id="start_age" v-model.number="form.start_age" type="number" />
    </div>
    <div class="form-group">
      <label for="retirement_age">은퇴 나이</label>
      <input id="retirement_age" v-model.number="form.retirement_age" type="number" />
    </div>
    <div class="form-group">
      <label for="end_age">종료 나이</label>
      <input id="end_age" v-model.number="form.end_age" type="number" />
    </div>
    <div class="form-group">
      <label for="initial_assets">현재 자산 (원)</label>
      <input id="initial_assets" v-model.number="form.initial_assets" type="number" />
    </div>
    <div class="form-group">
      <label for="initial_savings">연간 저축액 (원)</label>
      <input id="initial_savings" v-model.number="form.initial_savings" type="number" />
    </div>
    <div class="form-group">
      <label for="savings_growth_rate">저축 성장률 (%)</label>
      <input id="savings_growth_rate" v-model.number="form.savings_growth_rate" type="number" step="0.01" />
    </div>
    <div class="form-group">
      <label for="mean_return">기대 수익률 (%)</label>
      <input id="mean_return" v-model.number="form.mean_return" type="number" step="0.01" />
    </div>
    <div class="form-group">
      <label for="annual_expense">연간 지출 (원)</label>
      <input id="annual_expense" v-model.number="form.annual_expense" type="number" />
    </div>
    <div class="form-group">
      <label for="n_simulations">시뮬레이션 횟수</label>
      <input id="n_simulations" v-model.number="form.n_simulations" type="number" />
    </div>

    <!-- 버튼은 그리드 끝단 전체를 차지하도록 -->
    <div class="form-actions">
      <button type="submit" :disabled="loading">
        {{ loading ? '시뮬레이션 중…' : '시뮬레이션 실행' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useSimulationStore } from '@/stores/simulation.js'

const store = useSimulationStore()

const form = reactive({
  start_age: 26,
  retirement_age: 55,
  end_age: 100,
  initial_assets: 108000000,
  initial_savings: 18000000,
  savings_growth_rate: 0.02,
  mean_return: 0.12,
  annual_expense: 50000000,
  n_simulations: 1000
})

function submit() {
   // reactive form의 속성값(숫자)만 plain object로 넘깁니다.
   store.run({ 
     start_age:           form.start_age,
     retirement_age:      form.retirement_age,
     end_age:             form.end_age,
     initial_assets:      form.initial_assets,
     initial_savings:     form.initial_savings,
     savings_growth_rate: form.savings_growth_rate,
     mean_return:         form.mean_return,
     annual_expense:      form.annual_expense,
     n_simulations:       form.n_simulations,
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

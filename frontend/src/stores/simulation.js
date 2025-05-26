import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useSimulationStore = defineStore('simulation', () => {
  const data    = ref(null)
  const loading = ref(false)
  const error   = ref(null)

  async function run(params) {
    loading.value = true
    error.value   = null
    try {
      const res = await axios.post('/api/simulation/', params)
      data.value = res.data
    } catch (e) {
      error.value = e
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, run }
})

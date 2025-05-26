// src/stores/modal.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalStore = defineStore('modal', () => {
  const show = ref(false)
  const title = ref('')
  const description = ref('')
  let resolveFn = null

const confirmText = ref('확인')
const cancelText = ref('취소')
const icon = ref('❓')

const open = ({
  title: t,
  description: d,
  confirmText: c = '확인',
  cancelText: x = '취소',
  icon: i = '❓',
}) => {
  title.value = t
  description.value = d
  confirmText.value = c
  cancelText.value = x
  icon.value = i
  show.value = true

  return new Promise((resolve) => {
    resolveFn = resolve
  })
}


  const confirm = () => {
    show.value = false
    resolveFn(true)
  }

  const cancel = () => {
    show.value = false
    resolveFn(false)
  }

  const alert = ({ title, description, icon = '⚠️', confirmText = '확인' }) => {
  return new Promise((resolve) => {
    open({ title, description, icon, confirmText, cancelText: null }).then(() => resolve())
  })
}

  return {
  show, title, description,
  confirmText, cancelText, icon,   // ✅ 추가
  open, confirm, cancel, alert
  }
})
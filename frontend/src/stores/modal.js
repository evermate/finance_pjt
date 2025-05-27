// src/stores/modal.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalStore = defineStore('modal', () => {
  const show = ref(false)
  const title = ref('')
  const description = ref('')
  const confirmText = ref('확인')
  const cancelText = ref('취소')
  const icon = ref('❓')
  const mode = ref('primary')  // ✅ 추가: 기본값은 primary

  let resolveFn = null

  const open = ({
    title: t,
    description: d,
    confirmText: c = '확인',
    cancelText: x = '취소',
    icon: i = '❓',
    mode: m = 'primary'       // ✅ 여기서도 mode 받음
  }) => {
    title.value = t
    description.value = d
    confirmText.value = c
    cancelText.value = x
    icon.value = i
    mode.value = m
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

  const alert = ({
    title,
    description,
    icon = '⚠️',
    confirmText = '확인'
  }) => {
    return new Promise((resolve) => {
      open({
        title,
        description,
        icon,
        confirmText,
        cancelText: null,
        mode: 'primary'
      }).then(() => resolve())
    })
  }

  return {
    show,
    title,
    description,
    confirmText,
    cancelText,
    icon,
    mode,            // ✅ export도 해줘야 .vue에서 modal.mode 로 접근 가능
    open,
    confirm,
    cancel,
    alert,
  }
})

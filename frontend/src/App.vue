<template>
  <div id="app">
    <HeaderNav />
    <!-- 아래 주석 버튼을 조건부 렌더링 할때 필요함 지우지 말것  -->
    <!-- <MyProductsPanel v-if="route.meta.showProductsPanel" /> -->
    <MyProductsPanel/>

    <main class="main-container">
      <router-view />
    </main>
  </div>
   <!-- 전역 모달 -->
  <ConfirmModal
    v-if="modal.show"
    :message="modal.message"
    @confirm="modal.confirm"
    @cancel="modal.cancel"
  />
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import MyProductsPanel from '@/components/MyProductsPanel.vue'
import { useRoute } from 'vue-router'
import { useModalStore } from '@/stores/modal'
import ConfirmModal from '@/components/ConfirmModal.vue'

const modal = useModalStore()
const route = useRoute()
</script>

<style scoped>
#app {
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f7f9fc;
  min-height: 100vh;
}

.main-container {
  padding: 2rem;
}
</style>

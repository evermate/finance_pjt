<template>
  <div id="app">
    <HeaderNav />
    <MyProductsPanel />

    <main class="main-container">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import MyProductsPanel from '@/components/MyProductsPanel.vue'
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

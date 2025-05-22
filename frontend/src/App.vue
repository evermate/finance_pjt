<template>
  <div id="app">
    <HeaderNav />

    <main class="main-container">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
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

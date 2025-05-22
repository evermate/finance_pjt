<template>
  <div id="app">
    <HeaderNav />

    <main class="container">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue'
import { RouterView } from 'vue-router'
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}
</style>

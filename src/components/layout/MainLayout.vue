<template>
  <div class="layout">
    <!-- 左侧导航栏 -->
    <NavBar class="sidebar" />

    <!-- 右侧内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import NavBar from './NavBar.vue'
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 左侧导航栏 */
.sidebar {
  width: 220px;
  background-color: #1e1e2f;
  flex-shrink: 0;
}

/* 右侧主区域 */
.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: #f5f5f5;
}
</style>

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
  position: relative;
  background: #f5f5f5; /* 添加默认背景色 */
}

/* 左侧导航栏 */
.sidebar {
  width: 220px;
  background-color: rgba(30, 30, 47, 0.85);
  flex-shrink: 0;
  backdrop-filter: blur(8px);
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

/* 右侧主区域 - 渐变背景 */
.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  position: relative;
  
  /* 渐变背景 */
  background: linear-gradient(
    135deg,
    rgba(30, 35, 65, 0.95) 0%,
    rgba(50, 60, 90, 0.93) 50%,
    rgba(70, 85, 120, 0.9) 100%
  );
  box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.5);
  
  /* 毛玻璃效果 */
  backdrop-filter: blur(12px);
  
}

/* 添加磨砂玻璃效果边缘 */
.main-content::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 1px;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(255, 255, 255, 0.5),
    transparent
  );
}

/* 响应式调整 */
@media (max-width: 768px) {
  .sidebar {
    width: 70px;
  }
  
  .main-content {
    padding: 1rem;
  }
}
</style>
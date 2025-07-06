<template>
    <div class="analysis-page">
      <!-- 切换按钮 -->
      <div class="button-group">
        <button
          :class="{ active: currentTab === 'production' }"
          @click="currentTab = 'production'"
        >
          🎬 电影产量分析
        </button>
        <button
          :class="{ active: currentTab === 'boxoffice' }"
          @click="currentTab = 'boxoffice'"
        >
          💰 电影票房分析
        </button>
      </div>
  
      <!-- 动态内容切换 -->
      <div class="content-area">
        <ProductionChart v-if="currentTab === 'production'" />
        <BoxOfficeChart v-else />
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import ProductionChart from '@/components/analysis/ProductionChart.vue'
  import BoxOfficeChart from '@/components/analysis/BoxOfficeChart.vue'
  
  const currentTab = ref<'production' | 'boxoffice'>('production')
  </script>
  
<style scoped>
  .analysis-page {
    padding: 2rem;
  }
  
  .button-group {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .button-group button {
    padding: 0.8rem 1.6rem;
    border: none;
    background-color: #e5e7eb;
    border-radius: 999px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
  }
  
  .button-group button.active {
    background-color: #3b82f6;
    color: white;
  }
</style>
  
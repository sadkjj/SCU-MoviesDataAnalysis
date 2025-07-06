<template>
    <div class="analysis-page">
      <!-- 切换按钮 -->
      <div class="button-group">
        <button
          :class="{ active: currentTab === 'genre' }"
          @click="currentTab = 'genre'"
        >
          🎞 类型分析
        </button>
        <button
          :class="{ active: currentTab === 'boxoffice' }"
          @click="currentTab = 'boxoffice'"
        >
          💰 类型与票房分析
        </button>
        <button
          :class="{ active: currentTab === 'rating' }"
          @click="currentTab = 'rating'"
        >
          ⭐ 类型与评分分析
        </button>
      </div>
  
      <!-- 内容区 -->
      <div class="content-area">
        <GenrePieChart v-if="currentTab === 'genre'" />
        <GenreBoxOfficeChart v-if="currentTab === 'boxoffice'" />
        <GenreRatingChart v-if="currentTab === 'rating'" />
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import GenrePieChart from '@/components/analysis/GenrePieChart.vue'
  import GenreBoxOfficeChart from '@/components/analysis/GenreBoxOfficeChart.vue'
  import GenreRatingChart from '@/components/analysis/GenreRatingChart.vue'
  
  const currentTab = ref<'genre' | 'boxoffice' | 'rating'>('genre')
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
    background-color: #10b981;
    color: white;
  }
</style>
  
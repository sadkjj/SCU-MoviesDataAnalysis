<template>
    <div class="audience-market-page">
      <!-- 切换按钮 -->
      <div class="button-group">
        <button
          :class="{ active: currentTab === 'market' }"
          @click="currentTab = 'market'"
        >
          📊 市场趋势分析
        </button>
        <button
          :class="{ active: currentTab === 'preference' }"
          @click="currentTab = 'preference'"
        >
          🔄 观影偏好变化趋势
        </button>
      </div>
  
      <!-- 内容区域 -->
      <div class="content-area">
        <RatingInsight v-if="currentTab === 'rating'" />
        <MarketTrend v-if="currentTab === 'market'" />
        <PreferenceEvolution v-if="currentTab === 'preference'" />
      </div>
    </div>
</template>
  
<script setup lang="ts">
  import { ref } from 'vue'
  import MarketTrend from '@/components/analysis/MarketTrend.vue'
  import PreferenceEvolution from '@/components/analysis/PreferenceEvolution.vue'
  const currentTab = ref<'market' | 'preference'>('market')
</script>
  
<style scoped>
  .audience-market-page {
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
    background-color: #ef4444;
    color: white;
  }
</style>
  
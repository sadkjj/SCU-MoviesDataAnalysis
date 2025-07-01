<<<<<<< HEAD
<template>
    <div class="spatial-page">
      <!-- 切换按钮 -->
      <div class="button-group">
        <button
          :class="{ active: currentTab === 'time' }"
          @click="currentTab = 'time'"
        >
          🕒 时间维度分析
        </button>
        <button
          :class="{ active: currentTab === 'region' }"
          @click="currentTab = 'region'"
        >
          🌍 地域分析
        </button>
      </div>
  
      <!-- 动态内容区域 -->
      <div class="content-area">
        <TimeDimension v-if="currentTab === 'time'" />
        <RegionDimension v-if="currentTab === 'region'" />
      </div>
    </div>
</template>
  
<script setup lang="ts">
  import { ref } from 'vue'
  import TimeDimension from '@/components/analysis/TimeDimension.vue'
  import RegionDimension from '@/components/analysis/RegionDimension.vue'
  
  const currentTab = ref<'time' | 'region'>('time')
</script>
  
<style scoped>
  .spatial-page {
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
    background-color: #f59e0b;
    color: white;
  }
</style>
=======
<template>
    <div class="spatial-page">
      <!-- 切换按钮 -->
      <div class="button-group">
        <button
          :class="{ active: currentTab === 'time' }"
          @click="currentTab = 'time'"
        >
          🕒 时间维度分析
        </button>
        <button
          :class="{ active: currentTab === 'region' }"
          @click="currentTab = 'region'"
        >
          🌍 地域分析
        </button>
      </div>
  
      <!-- 动态内容区域 -->
      <div class="content-area">
        <TimeDimension v-if="currentTab === 'time'" />
        <RegionDimension v-if="currentTab === 'region'" />
      </div>
    </div>
</template>
  
<script setup lang="ts">
  import { ref } from 'vue'
  import TimeDimension from '@/components/analysis/TimeDimension.vue'
  import RegionDimension from '@/components/analysis/RegionDimension.vue'
  
  const currentTab = ref<'time' | 'region'>('time')
</script>
  
<style scoped>
  .spatial-page {
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
    background-color: #f59e0b;
    color: white;
  }
</style>
>>>>>>> 2169fedfedc3d443e3192294224aa2ddb9a5d482
  
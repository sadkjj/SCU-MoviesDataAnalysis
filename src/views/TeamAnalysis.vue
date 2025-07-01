<<<<<<< HEAD
<template>
    <div class="team-analysis-page">
      <!-- 切换按钮 -->
      <div class="button-group">
        <button
          :class="{ active: currentTab === 'director' }"
          @click="currentTab = 'director'"
        >
          🎬 导演分析
        </button>
        <button
          :class="{ active: currentTab === 'actor' }"
          @click="currentTab = 'actor'"
        >
          🧑‍🎤 演员分析
        </button>
      </div>
  
      <!-- 动态内容区域 -->
      <div class="content-area">
        <DirectorAnalysis v-if="currentTab === 'director'" />
        <ActorAnalysis v-if="currentTab === 'actor'" />
      </div>
    </div>
</template>
  
<script setup lang="ts">
  import { ref } from 'vue'
  import DirectorAnalysis from '@/components/analysis/DirectorAnalysis.vue'
  import ActorAnalysis from '@/components/analysis/ActorAnalysis.vue'
  
  const currentTab = ref<'director' | 'actor'>('director')
</script>
  
<style scoped>
  .team-analysis-page {
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
    background-color: #6366f1;
    color: white;
  }
</style>
=======
<template>
    <div class="team-analysis-page">
      <!-- 切换按钮 -->
      <div class="button-group">
        <button
          :class="{ active: currentTab === 'director' }"
          @click="currentTab = 'director'"
        >
          🎬 导演分析
        </button>
        <button
          :class="{ active: currentTab === 'actor' }"
          @click="currentTab = 'actor'"
        >
          🧑‍🎤 演员分析
        </button>
      </div>
  
      <!-- 动态内容区域 -->
      <div class="content-area">
        <DirectorAnalysis v-if="currentTab === 'director'" />
        <ActorAnalysis v-if="currentTab === 'actor'" />
      </div>
    </div>
</template>
  
<script setup lang="ts">
  import { ref } from 'vue'
  import DirectorAnalysis from '@/components/analysis/DirectorAnalysis.vue'
  import ActorAnalysis from '@/components/analysis/ActorAnalysis.vue'
  
  const currentTab = ref<'director' | 'actor'>('director')
</script>
  
<style scoped>
  .team-analysis-page {
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
    background-color: #6366f1;
    color: white;
  }
</style>
>>>>>>> 2169fedfedc3d443e3192294224aa2ddb9a5d482
  
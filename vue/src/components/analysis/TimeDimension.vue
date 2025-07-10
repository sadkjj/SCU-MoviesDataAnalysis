<template>
  <div class="section">
    <h2>🕒 时间维度分析</h2>
    <!-- 搜索栏 -->
    <div class="filter-container">
      <label for="movie">电影名称：</label>
      <input 
        v-model="movieName" 
        placeholder="请输入电影名称，如：哪吒" 
        @keyup.enter="fetchMovieData"
      />
      <button @click="fetchMovieData" :disabled="loading">
        {{ loading ? '搜索中...' : '🔍 搜索' }}
      </button>
    </div>

    <!-- 状态提示 -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    
    <!-- 图表展示 -->
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'
// 定义接口类型
interface MovieData {
  status: boolean
  times: string[]
  box_offices: number[]
}

// 响应式变量
const chartRef = ref<HTMLDivElement | null>(null)
const movieName = ref<string>('')
const loading = ref<boolean>(false)
const errorMessage = ref<string>('')
let chartInstance: ECharts | null = null

// 初始化图表
onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chartInstance?.resize())
  }
})

// 渲染图表
const renderChart = (data: MovieData) => {
  if (!chartInstance) return

  const option = {
    title: { 
      text: `${movieName.value ? `《${movieName.value}》` : ''}票房变化趋势`, 
      left: 'center',
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        return `
          <strong>${params[0].axisValue}</strong><br/>
          票房: ${params[0].data} 万元
        `
      }
    },
    xAxis: {
      type: 'category',
      data: data.times,
      name: '时间',
      axisLabel: {
        interval: 0,
        rotate: data.times.length > 6 ? 30 : 0
      }
    },
    yAxis: {
      type: 'value',
      name: '票房（万元）',
      axisLine: {
        show: true
      }
    },
    series: [
      {
        name: '票房',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 3,
          color: '#5470C6'
        },
        itemStyle: {
          color: '#5470C6'
        },
        data: data.box_offices,
        label: {
          show: true,
          position: 'top',
          formatter: '{c}万元'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(84, 112, 198, 0.5)' },
            { offset: 1, color: 'rgba(84, 112, 198, 0.1)' }
          ])
        }
      }
    ],
    grid: {
      top: '20%',
      bottom: '15%',
      containLabel: true
    }
  }

  chartInstance.setOption(option, true)
}

// 清空图表
const clearChart = () => {
  if (chartInstance) {
    chartInstance.clear()
    chartInstance.setOption({
      title: {
        text: '暂无数据',
        left: 'center',
        top: 'center',
        textStyle: {
          color: '#999',
          fontSize: 16
        }
      },
      xAxis: { show: false },
      yAxis: { show: false },
      series: []
    })
  }
}

// 获取电影数据
const fetchMovieData = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    const params= {
          movie_name: movieName.value.trim()
        }
        console.log(params);
        
    const { data } = await axios.get<MovieData>(
      `${API_BASE_URL}/timeline`,
      {
        params: {
          movie_name: movieName.value.trim()
        }
      }
    )
      console.log(data);
      
    // 直接渲染返回的数据，不做额外验证
    renderChart(data)
  } catch (error) {
    console.error('请求失败:', error)
    errorMessage.value = '获取数据失败，请检查网络连接'
    clearChart()
  } finally {
    loading.value = false
  }
}

// 组件卸载时清理
onBeforeUnmount(() => {
  window.removeEventListener('resize', () => chartInstance?.resize())
  chartInstance?.dispose()
})
</script>

<style scoped>
.section {
  background-color: #e6f0ff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.filter-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.filter-container label {
  font-weight: bold;
  min-width: 80px;
}

.filter-container input {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 1rem;
  min-width: 200px;
  transition: border-color 0.3s;
}

.filter-container input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.filter-container button {
  padding: 0.5rem 1.5rem;
  background-color: #3b82f6;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.filter-container button:hover:not(:disabled) {
  background-color: #2563eb;
}

.filter-container button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.chart {
  width: 100%;
  height: 500px;
  margin-top: 1rem;
}

.error-message {
  color: #ef4444;
  padding: 0.75rem;
  margin: 0.5rem 0;
  background-color: #fee2e2;
  border-radius: 0.5rem;
  text-align: center;
}

@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-container input {
    width: 100%;
  }
}
</style>
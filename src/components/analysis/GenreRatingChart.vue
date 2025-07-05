<template>
  <div class="chart-container">
    <h2 class="chart-title">⭐ 类型与评分分析</h2>

    <!-- 筛选条件区域 -->
    <div class="filter-container">
      <div class="filter-group">
        <label>起始年份：</label>
        <select v-model="startYear">
          <option v-for="year in yearRange" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>

      <div class="filter-group">
        <label>终止年份：</label>
        <select v-model="endYear">
          <option v-for="year in yearRange" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>

      <div class="filter-group">
        <label>国家/地区：</label>
        <input 
          v-model="country" 
          type="text" 
          placeholder="输入国家(可选)"
          @keyup.enter="handleSearch"
        >
      </div>

      <!-- 搜索按钮 -->
      <div class="filter-group search-button">
        <button @click="handleSearch" :disabled="loading">
          {{ loading ? '加载中...' : '🔍 搜索' }}
        </button>
      </div>
    </div>

    <!-- 状态提示 -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="timeRange" class="info-message">
      查询范围: {{ timeRange }} | 电影总数: {{ totalMovies }}
    </div>

    <!-- 图表区域 -->
    <div ref="ratingChart" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import axios from 'axios'

// 图表引用
const ratingChart = ref<HTMLElement | null>(null)
let chartInstance: ECharts | null = null

// 筛选条件
const startYear = ref(2020)
const endYear = ref(2023)
const country = ref('')
const selectedType = ref('')
const yearRange = Array.from({ length: 16 }, (_, i) => 2010 + i)

// 数据状态
const allTypes = ref<string[]>([])
const rawData = ref<any[]>([])
const timeRange = ref('')
const totalMovies = ref(0)
const loading = ref(false)
const errorMessage = ref('')

// API接口配置
const API_URL = 'http://127.0.0.1:4523/m1/6680275-6389502-default/Type_score'

// 接口响应类型
interface RatingDistribution {
  '0-3': number
  '3-6': number
  '6-7': number
  '7-8': number
  '8-9': number
  '9-10': number
}

interface AnalysisItem {
  type: string
  avgRating: number
  medianRating: number
  ratingDistribution: RatingDistribution
}

interface ApiResponse {
  code: number
  message: string
  data: {
    timeRange: string
    totalMovies: number
    analysis: AnalysisItem[]
  }
}

// 获取数据
const fetchData = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    
    const params = {
      startYear: startYear.value,
      endYear: endYear.value,
      country: country.value || undefined // 不传空字符串
    }

    const { data } = await axios.get<ApiResponse>(API_URL, { params })

    if (data.code === 200) {
      rawData.value = data.data.analysis
      allTypes.value = [...new Set(data.data.analysis.map(item => item.type))]
      timeRange.value = data.data.timeRange
      totalMovies.value = data.data.totalMovies
      drawChart()
    } else {
      return {
        message: data.message || 'error' // 确保返回message字段
      }
    }
  } catch (error: any) {
    console.error('请求失败:', error)
    // 捕获400错误并返回标准格式
    if (error.response && error.response.status === 400) {
      return {
        message: error.response.data.message || 'error'
      }
    }
    // 其他错误也返回标准格式
    return {
      message: 'error'
    }
  }
}

// 绘制图表
const drawChart = () => {
  if (!ratingChart.value) return

  const target = selectedType.value
  const data = target
    ? rawData.value.filter(item => item.type === target)
    : rawData.value

  const categories = data.map(d => d.type)
  const avgRatings = data.map(d => d.avgRating)
  const medianRatings = data.map(d => d.medianRating)

  // 初始化图表
  if (!chartInstance) {
    chartInstance = echarts.init(ratingChart.value)
    window.addEventListener('resize', () => chartInstance?.resize())
  }

  // 设置图表选项
  chartInstance.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const item = data[params[0].dataIndex]
        let distStr = ''
        for (const [range, count] of Object.entries(item.ratingDistribution)) {
          distStr += `${range}分: ${count}部<br/>`
        }
        return `
          <strong>${item.type}</strong><br/>
          平均评分: ${item.avgRating.toFixed(1)}<br/>
          中位数: ${item.medianRating}<br/>
          评分分布:<br/>${distStr}
        `
      }
    },
    legend: { 
      data: ['平均评分', '中位数评分'],
      bottom: 10
    },
    grid: {
      top: '15%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: { 
      type: 'category', 
      data: categories,
      axisLabel: {
        interval: 0,
        rotate: categories.length > 5 ? 30 : 0
      }
    },
    yAxis: { 
      type: 'value', 
      name: '评分 (0~10)',
      min: 0,
      max: 10
    },
    series: [
      {
        name: '平均评分',
        type: 'bar',
        data: avgRatings,
        itemStyle: { color: '#5470c6' },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      },
      {
        name: '中位数评分',
        type: 'bar',
        data: medianRatings,
        itemStyle: { color: '#91cc75' },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      }
    ]
  }, true)
}

// 搜索处理
const handleSearch = () => {
  if (startYear.value > endYear.value) {
    errorMessage.value = '起始年份不能大于终止年份'
    return
  }
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.chart-container {
  padding: 2rem;
  background-color: #fefce8;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.chart-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  color: #333;
}

/* 筛选器整体样式 */
.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #fff8dc;
  border: 1px solid #fceabb;
  border-radius: 0.75rem;
}

/* 单个筛选项 */
.filter-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 14px;
  min-width: 120px;
}

.filter-group label {
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.filter-group select,
.filter-group input {
  padding: 0.4rem 0.75rem;
  width: 100%;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #fff;
  transition: border-color 0.2s;
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-color: #a78bfa;
}

/* 图表区域 */
.chart {
  width: 100%;
  height: 500px;
  margin-top: 1rem;
}

.search-button button {
  margin-top: 1.5rem;
  padding: 0.5rem 1.5rem;
  background-color: #facc15;
  border: none;
  border-radius: 6px;
  color: #333;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.search-button button:hover:not(:disabled) {
  background-color: #eab308;
  transform: translateY(-1px);
}

.search-button button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: #ef4444;
  padding: 0.75rem;
  margin: 1rem 0;
  background-color: #fee2e2;
  border-radius: 0.5rem;
  text-align: center;
}

.info-message {
  color: #3b82f6;
  padding: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .filter-group {
    width: 100%;
  }
  
  .chart {
    height: 400px;
  }
}
</style>
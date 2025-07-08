<template>
  <div class="chart-placeholder">
    <h2>📊-💰 类型与票房分析</h2>

    <!-- 筛选条件 -->
    <div class="filter-container">
      <div class="filter-group">
        <label>起始年份：</label>
        <input 
          v-model.number="startYear" 
          type="number" 
          @change="validateYears"
        >
      </div>

      <div class="filter-group">
        <label>终止年份：</label>
        <input 
          v-model.number="endYear" 
          type="number" 
          @change="validateYears"
        >
      </div>

      <div class="filter-group">
        <button @click="fetchData" :disabled="loading">
          {{ '🔍 搜索' }}
        </button>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

// 图表引用
const chartRef = ref(null)
let chartInstance: echarts.ECharts | null = null

// 筛选条件
const startYear = ref(2020)
const endYear = ref(2023)

// 状态管理
const loading = ref(false)
const errorMessage = ref('')
const unit = ref('亿元')

// 接口响应类型
interface GenreAnalysis {
  type: string
  avgBoxOffice: number
  maxBoxOffice: number
  minBoxOffice: number
  totalBoxOffice: number
}

interface ApiResponse {
  code: number
  message: string
  data: {
    analysis: GenreAnalysis[]
  }
}

// 初始化图表
const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
    window.addEventListener('resize', () => chartInstance?.resize())
  }
}

// 年份验证
const validateYears = () => {
  // 最大年份限制
  if (endYear.value > 2025) {
    endYear.value = 2025
  }
  
  // 起始年份不能大于终止年份
  if (startYear.value > endYear.value) {
    errorMessage.value = '起始年份不能大于终止年份'
  } else {
    errorMessage.value = ''
    fetchData()
  }
}

// 元转亿元并保留两位小数
const yuanToYi = (value: number): number => {
  return parseFloat((value / 100000000).toFixed(1))
}

// 获取数据
const fetchData = async () => {
  try {
    
    loading.value = true
    errorMessage.value = ''

    const params = {
      startYear: startYear.value,
      endYear: endYear.value
    }

    const { data } = await axios.get<ApiResponse>(
      `${API_BASE_URL}/boxOffice`,
      { params }
    )

    if (data.code === 200) {
      console.log(data);
      
      updateChart(data.data.analysis)
    } else {
      errorMessage.value = data.message || '获取数据失败'
    }
  } catch (error: any) {
    console.error('请求失败:', error)
    errorMessage.value = error.response?.data?.message || '请求发生错误'
  } finally {
    loading.value = false
  }
}

// 更新图表
const updateChart = (analysisData: GenreAnalysis[]) => {
  if (!chartInstance) return

  const types = analysisData.map(d => d.type)
  const avg = analysisData.map(d => yuanToYi(d.avgBoxOffice))
  const max = analysisData.map(d => yuanToYi(d.maxBoxOffice))
  const min = analysisData.map(d => yuanToYi(d.minBoxOffice))
  const total = analysisData.map(d => yuanToYi(d.totalBoxOffice))

  const option = {
    title: { 
      text: '不同类型电影票房分析',
      subtext: `${startYear.value}-${endYear.value}年 | 单位: ${unit.value}`,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const [avgParam, maxParam, minParam, totalParam] = params
        return `
          <strong>${avgParam.name}</strong><br/>
          平均票房: ${avgParam.value} ${unit.value}<br/>
          最高票房: ${maxParam.value} ${unit.value}<br/>
          最低票房: ${minParam.value} ${unit.value}<br/>
          总票房: ${totalParam.value} ${unit.value}
        `
      }
    },
    legend: { 
      data: ['平均票房', '最高票房', '最低票房', '总票房'],
      bottom: 10
    },
    grid: {
      top: '20%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: { 
      type: 'category', 
      data: types,
      axisLabel: {
        interval: 0,
        rotate: types.length > 5 ? 30 : 0
      }
    },
    yAxis: { 
      type: 'value', 
      name: `票房 (${unit.value})`,
      axisLine: {
        show: true
      }
    },
    series: [
      { 
        name: '平均票房', 
        type: 'bar', 
        data: avg,
        itemStyle: {
          color: '#5470C6'
        },
        label: {
          show: true,
          position: 'top',
          formatter: `{c} ${unit.value}`
        }
      },
      { 
        name: '最高票房', 
        type: 'bar', 
        data: max,
        itemStyle: {
          color: '#91CC75'
        },
        label: {
          show: true,
          position: 'top',
          formatter: `{c} ${unit.value}`
        }
      },
      { 
        name: '最低票房', 
        type: 'bar', 
        data: min,
        itemStyle: {
          color: '#FAC858'
        },
        label: {
          show: true,
          position: 'top',
          formatter: `{c} ${unit.value}`
        }
      },
      { 
        name: '总票房', 
        type: 'bar', 
        data: total,
        itemStyle: {
          color: '#EE6666'
        },
        label: {
          show: true,
          position: 'top',
          formatter: `{c} ${unit.value}`
        }
      }
    ]
  }

  chartInstance.setOption(option, true)
}

// 监听年份变化自动更新
watch([startYear, endYear], () => {
  fetchData()
})

onMounted(() => {
  initChart()
  fetchData()
})
</script>

<style scoped>
.chart-placeholder {
  padding: 2rem;
  background-color: #e6f0ff;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.chart {
  width: 100%;
  height: 500px;
  margin-top: 1rem;
}

.filter-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  margin-bottom: 1.5rem;
  background-color: #e6f0ff;
  border: 1px solid #b9ceeeee;
  border-radius: 0.75rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 14px;
  font-weight: 500;
  color: #444;
}

.filter-group label {
  min-width: 80px;
  text-align: right;
}

.filter-group input {
  padding: 0.4rem 0.75rem;
  width: 80px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background-color: #fff;
  font-size: 14px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: border 0.3s, box-shadow 0.3s;
}

.filter-group input:focus {
  outline: none;
  border-color: #facc15;
  box-shadow: 0 0 0 2px rgba(250, 204, 21, 0.3);
}

.filter-group button {
  padding: 0.5rem 1.2rem;
  background-color: #facc15;
  border: none;
  border-radius: 6px;
  color: #333;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.filter-group button:hover:not(:disabled) {
  background-color: #fbbf24;
  transform: translateY(-1px);
}

.filter-group button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: #ef4444;
  margin: 1rem 0;
  padding: 0.5rem;
  background-color: #fee2e2;
  border-radius: 0.5rem;
}
</style>
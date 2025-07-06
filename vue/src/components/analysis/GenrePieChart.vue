<template>
  <div class="chart-placeholder">
    <h2>📊 类型分析</h2>
    <div class="filter-container">
      <label for="startYear">起始年份:</label>
      <input 
        type="number" 
        id="startYear" 
        v-model.number="startYear" 
        class="filter-input"
        min="1900"
        max="2100"
      >
      
      <label for="endYear">结束年份:</label>
      <input 
        type="number" 
        id="endYear" 
        v-model.number="endYear" 
        class="filter-input"
        min="1900"
        max="2100"
      >
      
      <label for="country">上映地区:</label>
      <input 
        type="text" 
        id="country" 
        v-model="country" 
        class="filter-input"
        placeholder="输入国家/地区"
      >

      <button @click="fetchData" class="filter-button">🔍 搜索</button>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div ref="genreChart" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'
// 图表容器引用
const genreChart = ref<HTMLDivElement | null>(null)
const chartInstance = ref<echarts.ECharts | null>(null)

// 筛选条件
const startYear = ref<number>(2010)
const endYear = ref<number>(2023)
const country = ref<string>('')
const errorMessage = ref<string>('')

// 响应数据类型
interface GenreData {
  genre: string
  count: number
  percentage: number
}

interface ApiResponse {
  code: number
  message: string
  data: GenreData[]
}

// 初始化图表
onMounted(() => {
  if (genreChart.value) {
    chartInstance.value = echarts.init(genreChart.value)
    fetchData()
  }
})

// 获取数据
const fetchData = async () => {
  try {
    errorMessage.value = ''
    
    // 参数验证
    if (startYear.value > endYear.value) {
      errorMessage.value = '起始年份不能大于结束年份'
      return
    }

    const params = {
      startYear: startYear.value,
      endYear: endYear.value,
      country: country.value.trim() || undefined // 空字符串不传
    }

    const { data } = await axios.get<ApiResponse>(
      `${API_BASE_URL}/type_p`,
      { params }
    )

    if (data.code === 200) {
      if (data.data && data.data.length > 0) {
        updateChart(data.data)
      } else {
        errorMessage.value = '暂无数据'
        clearChart()
      }
    } else {
      errorMessage.value = data.message || '获取数据失败'
      clearChart()
    }
  } catch (error: any) {
    console.error('请求失败:', error)
    if (error.response && error.response.status === 400) {
      errorMessage.value = error.response.data.message || '请求参数错误'
    } else {
      errorMessage.value = '请求数据失败，请检查网络连接'
    }
    clearChart()
  }
}

// 清空图表
const clearChart = () => {
  if (chartInstance.value) {
    chartInstance.value.clear()
    chartInstance.value.setOption({
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

// 更新图表
const updateChart = (chartData: GenreData[]) => {
  if (!chartInstance.value) return

  const option = {
    title: {
      text: '电影类型分布',
      subtext: `${startYear.value}-${endYear.value}${country.value ? ` | ${country.value}` : ''}`,
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const data = params.data
        return `
          <strong>${data.name}</strong><br/>
          数量: ${data.value}部<br/>
          占比: ${data.percentage}%
        `
      }
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 10,
      top: 'middle',
      textStyle: {
        overflow: 'truncate',
        width: 100
      }
    },
    series: [
      {
        name: '电影类型',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
        data: chartData.map(item => ({
          value: item.count,
          name: item.genre,
          percentage: item.percentage
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          show: true,
          formatter: '{b}: {d}%'
        },
        labelLine: {
          show: true
        }
      }
    ]
  }

  chartInstance.value.setOption(option, true)
}
</script>

<style scoped>
.chart-placeholder {
  padding: 2rem;
  background-color: #fefce8;
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
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  width: 120px;
  transition: border-color 0.3s;
}

.filter-input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.filter-button {
  padding: 0.5rem 1.5rem;
  background-color: #007bff;
  border: none;
  border-radius: 6px;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.filter-button:hover {
  background-color: #0056b3;
}

.filter-container label {
  margin-right: 0.5rem;
  font-weight: bold;
  align-self: center;
}

.error-message {
  color: #f56c6c;
  padding: 0.75rem;
  margin: 1rem 0;
  background-color: #fee2e2;
  border-radius: 0.5rem;
  text-align: center;
}

@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-input {
    width: 100%;
  }
}
</style>
<template>
  <div class="section">
    <h2>🌍 地域分析</h2>

    <!-- 年份输入框 -->
    <div class="filter-container">
      <label for="year">选择年份：</label>
      <input
        v-model.number="selectedYear"
        type="number"
        min="2010"
        :max="currentYear"
        @change="validateYear"
        @keyup.enter="fetchData"
      />
      <button @click="fetchData">查询</button>
    </div>

    <!-- 状态提示 -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- 地图展示 -->
    <div ref="mapChartRef" class="map-chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import axios from 'axios'
import worldMap from '@/assets/world.json' 

// 定义接口类型
interface TypeData {
  type: string
  count: number
}

interface AreaData {
  area: string
  type_data: TypeData[]
}

interface ApiResponse {
  year: string
  area_data: AreaData[]
}

// 响应式变量
const selectedYear = ref<number>(2023)
const currentYear = new Date().getFullYear()
const mapChartRef = ref<HTMLDivElement | null>(null)
const errorMessage = ref<string>('')
let chartInstance: ECharts | null = null

// 注册地图数据
onMounted(() => {
  if (mapChartRef.value) {
    echarts.registerMap('world', worldMap) 
    chartInstance = echarts.init(mapChartRef.value)
    fetchData()
    window.addEventListener('resize', () => chartInstance?.resize())
  }
})

// 年份验证
const validateYear = () => {
  //if (selectedYear.value < 2010) selectedYear.value = 2010
  if (selectedYear.value > currentYear) selectedYear.value = currentYear
}

// 获取数据
const fetchData = async () => {
  try {
    errorMessage.value = ''

    const response = await axios.get('http://localhost:5000/area', {
      params: {
        year: selectedYear.value
      }
    })

    const areaData = response.data?.data
    if (!Array.isArray(areaData)) {
      throw new Error('后端返回的 data 格式不正确')
    }

    const chartData = areaData.map(area => ({
      name: area.area,
      value: area.type_data.reduce((sum, t) => sum + t.count, 0)
    }))

    const maxValue = Math.max(...chartData.map(item => item.value), 100)
    updateChart(chartData, maxValue, `${selectedYear.value}`) // 没有 year 字段，直接用选中的年份
  } catch (error) {
    console.error('请求失败:', error)
    errorMessage.value = '获取数据失败，请检查网络或接口格式'
    clearChart()
  }
}
// 更新图表
const updateChart = (data: { name: string; value: number }[], maxValue: number, year: string) => {
  if (!chartInstance) return

  chartInstance.setOption({
    title: { 
      text: `${year}年 各国家/地区电影产量`, 
      left: 'center',
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        return `${params.name}<br/>产量：${params.value} 部`
      }
    },
    visualMap: {
      min: 0,
      max: maxValue,
      left: 'left',
      bottom: '20px',
      text: ['高', '低'],
      inRange: { 
        color: ['#e0f3f8', '#abd9e9', '#74add1', '#4575b4'] 
      },
      calculable: true
    },
    series: [
      {
        name: '电影产量',
        type: 'map',
        map: 'world',
        roam: true,
        emphasis: {
          label: {
            show: true
          }
        },
        data: data,
        itemStyle: {
          areaColor: '#eee',
          borderColor: '#aaa'
        }
      }
    ]
  }, true)
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
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.filter-container label {
  font-weight: 600;
  color: #065f46;
}

.filter-container input {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 1rem;
  width: 120px;
  transition: border-color 0.3s;
}

.filter-container input:focus {
  outline: none;
  border-color: #10b981;
}

.filter-container button {
  padding: 0.5rem 1rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.filter-container button:hover {
  background-color: #059669;
}

.map-chart {
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
    align-items: flex-start;
  }
  
  .filter-container input {
    width: 100%;
  }
}
</style>
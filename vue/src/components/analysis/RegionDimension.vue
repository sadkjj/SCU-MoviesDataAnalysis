<template>
  <div class="section">
    <h2>🌍 地域分析</h2>

    <!-- 年份选择器 -->
    <div class="filter-container">
      <label for="year">选择年份：</label>
      <select v-model="selectedYear" @change="fetchData">
        <option v-for="year in yearList" :key="year" :value="year">{{ year }}</option>
      </select>
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
const selectedYear = ref<number>(2026)
const yearList = Array.from({ length: 16 }, (_, i) => 2010 + i)
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

// 获取数据
const fetchData = async () => {
  try {
    errorMessage.value = ''

    const { data } = await axios.get<ApiResponse>(
      //'http://127.0.0.1:4523/m1/6680275-6389502-default/area',
      'http://localhost:5000/area',
      {
        params: {
          year: selectedYear.value
        }
      }
    )

    // 处理数据
    const chartData = data.area_data.map(area => ({
      name: area.area,
      value: area.type_data.reduce((sum, t) => sum + t.count, 0)
    }))

    // 计算最大值用于视觉映射
    const maxValue = Math.max(...chartData.map(item => item.value), 100)

    // 更新图表
    updateChart(chartData, maxValue, data.year)
  } catch (error) {
    console.error('请求失败:', error)
    errorMessage.value = '获取数据失败，请检查网络连接'
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
  background-color: #ecfdf5;
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

.filter-container select {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 1rem;
  min-width: 120px;
  transition: border-color 0.3s;
}

.filter-container select:focus {
  outline: none;
  border-color: #10b981;
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
  
  .filter-container select {
    width: 100%;
  }
}
</style>
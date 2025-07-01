<<<<<<< HEAD
<template>
  <div class="dashboard-container">
    <h2 class="dashboard-title">🎬 电影票房与成本分析</h2>
    
    <!-- 筛选条件 -->
    <div class="filter-container">
      <div class="filter-group">
        <label>榜单类型：</label>
        <select v-model="filter.type" @change="updateRankingChart">
          <option value="total">总榜单</option>
          <option value="yearly">年度榜单</option>
          <option value="monthly">月度榜单</option>
        </select>
      </div>
      
      <div class="filter-group" v-if="filter.type === 'yearly'">
        <label>选择年份：</label>
        <select v-model="filter.year" @change="updateRankingChart">
          <option v-for="y in availableYears" :value="y" :key="y">{{ y }}年</option>
        </select>
      </div>
      
      <div class="filter-group" v-if="filter.type === 'monthly'">
        <label>选择月份：</label>
        <select v-model="filter.month" @change="updateRankingChart">
          <option v-for="m in 12" :value="m" :key="m">{{ m }}月</option>
        </select>
      </div>
    </div>

    <!-- 票房排行图表 -->
    <div class="chart-card">
      <h3>{{ chartTitle }}票房排行</h3>
      <div ref="rankingChart" class="chart"></div>
    </div>
    
    <!-- 成本关系图表 -->
    <div class="chart-card">
      <h3>电影票房-成本关系</h3>
      <div ref="relationChart" class="chart"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'

interface MovieData {
  name: string
  boxOffice: number
  cost: number
  roi?: number
}

interface YearlyRanking {
  [key: number]: MovieData[]
}

interface MonthlyRanking {
  [key: string]: MovieData[]
}

// 筛选条件
const filter = ref({
  type: 'total',
  year: 2023,
  month: 1
})

const availableYears = [2023, 2022, 2021, 2020]

// 图表DOM引用
const rankingChart = ref<HTMLElement | null>(null)
const relationChart = ref<HTMLElement | null>(null)

// 图表实例
let rankingChartInstance: ECharts | null = null
let relationChartInstance: ECharts | null = null

// 计算属性
const chartTitle = computed(() => {
  switch(filter.value.type) {
    case 'yearly': return `${filter.value.year}年度`
    case 'monthly': return `${filter.value.year}年${filter.value.month}月`
    default: return '历史总'
  }
})

// 模拟数据
const mockData = {
  // 榜单数据
  totalRanking: [
    { name: '长津湖', boxOffice: 57.75, cost: 5.2, roi: 11.1 },
    { name: '战狼2', boxOffice: 56.94, cost: 2.0, roi: 28.5 },
    { name: '你好，李焕英', boxOffice: 54.13, cost: 3.5, roi: 15.5 },
    { name: '哪吒之魔童降世', boxOffice: 50.35, cost: 0.6, roi: 83.9 },
    { name: '流浪地球', boxOffice: 46.86, cost: 3.2, roi: 14.6 }
  ] as MovieData[],
  yearlyRanking: {
    2023: [
      { name: '满江红', boxOffice: 45.44, cost: 1.5, roi: 30.3 },
      { name: '流浪地球2', boxOffice: 40.29, cost: 5.8, roi: 6.9 },
      { name: '孤注一掷', boxOffice: 38.48, cost: 1.2, roi: 32.1 }
    ],
    2022: [
      { name: '长津湖之水门桥', boxOffice: 40.67, cost: 5.0, roi: 8.1 },
      { name: '独行月球', boxOffice: 31.03, cost: 3.0, roi: 10.3 },
      { name: '这个杀手不太冷静', boxOffice: 26.27, cost: 1.5, roi: 17.5 }
    ]
  } as YearlyRanking,
  monthlyRanking: {
    '2023-1': [
      { name: '流浪地球2', boxOffice: 40.29, cost: 5.8 },
      { name: '满江红', boxOffice: 38.12, cost: 1.5 },
      { name: '熊出没·伴我熊芯', boxOffice: 14.95, cost: 0.8 }
    ],
    '2023-2': [
      { name: '满江红', boxOffice: 45.44, cost: 1.5 },
      { name: '流浪地球2', boxOffice: 40.29, cost: 5.8 },
      { name: '熊出没·伴我熊芯', boxOffice: 14.95, cost: 0.8 }
    ]
  } as MonthlyRanking,
  
  // 静态的成本-票房关系数据（不受筛选影响）
  costRelationData: [
    { name: '哪吒之魔童降世', boxOffice: 50.35, cost: 0.6 },
    { name: '战狼2', boxOffice: 56.94, cost: 2.0 },
    { name: '你好，李焕英', boxOffice: 54.13, cost: 3.5 },
    { name: '流浪地球', boxOffice: 46.86, cost: 3.2 },
    { name: '长津湖', boxOffice: 57.75, cost: 5.2 },
    { name: '满江红', boxOffice: 45.44, cost: 1.5 },
    { name: '流浪地球2', boxOffice: 40.29, cost: 5.8 }
  ] as MovieData[]
}

// 获取当前榜单数据
const getCurrentRankingData = (): MovieData[] => {
  switch(filter.value.type) {
    case 'yearly':
      return mockData.yearlyRanking[filter.value.year] || []
    case 'monthly':
      const key = `${filter.value.year}-${filter.value.month}`
      return mockData.monthlyRanking[key] || []
    default:
      return mockData.totalRanking
  }
}

// 更新榜单图表
const updateRankingChart = () => {
  const data = getCurrentRankingData()
  
  if (rankingChartInstance && rankingChart.value) {
    rankingChartInstance.setOption({
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          const item = params.data
          return `
            <div style="font-weight:bold">${item.name}</div>
            <div>票房: ${item.boxOffice} 亿元</div>
            <div>成本: ${item.cost} 亿元</div>
            <div>回报率: ${item.roi?.toFixed(1) || (item.boxOffice/item.cost).toFixed(1)} 倍</div>
          `
        }
      },
      xAxis: {
        type: 'value',
        name: '票房(亿元)'
      },
      yAxis: {
        type: 'category',
        data: data.map(item => item.name)
      },
      series: [{
        data: data.map(item => item.boxOffice),
        type: 'bar',
        itemStyle: {
          color: (params: any) => {
            const item = data[params.dataIndex]
            const roi = item.roi || item.boxOffice / item.cost
            return roi > 15 ? '#67c23a' : roi > 10 ? '#e6a23c' : '#f56c6c'
          }
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}亿'
        }
      }]
    })
  }
}

// 初始化成本-票房关系图（静态数据）
const initRelationChart = () => {
  if (relationChart.value) {
    relationChartInstance = echarts.init(relationChart.value)
    relationChartInstance.setOption({
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          const item = params.data
          return `
            <div style="font-weight:bold">${item.name}</div>
            <div>成本: ${item.value[0]} 亿元</div>
            <div>票房: ${item.value[1]} 亿元</div>
            <div>回报率: ${item.roi.toFixed(1)} 倍</div>
          `
        }
      },
      xAxis: {
        type: 'value',
        name: '制作成本(亿元)'
      },
      yAxis: {
        type: 'value',
        name: '票房收入(亿元)'
      },
      series: [{
        data: mockData.costRelationData.map(item => ({
          name: item.name,
          value: [item.cost, item.boxOffice],
          roi: item.boxOffice/item.cost
        })),
        type: 'scatter',
        symbolSize: (data: any) => Math.sqrt(data.roi) * 10,
        itemStyle: {
          color: (params: any) => {
            const roi = params.data.roi
            return roi > 15 ? '#67c23a' : roi > 10 ? '#e6a23c' : '#f56c6c'
          }
        },
        label: {
          show: true,
          formatter: '{b}',
          position: 'top'
        }
      }]
    })
  }
}

// 初始化所有图表
const initCharts = () => {
  if (rankingChart.value) {
    rankingChartInstance = echarts.init(rankingChart.value)
    updateRankingChart()
  }
  initRelationChart()
}

// 响应式调整
const handleResize = () => {
  rankingChartInstance?.resize()
  relationChartInstance?.resize()
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  rankingChartInstance?.dispose()
  relationChartInstance?.dispose()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.filter-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
}

.filter-group label {
  margin-right: 10px;
  font-size: 14px;
}

.filter-group select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}

.chart-card {
  margin-bottom: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 15px;
}

.chart-card h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  text-align: center;
  color: #555;
}

.chart {
  width: 100%;
  height: 400px;
}

@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    gap: 10px;
  }
  
  .chart {
    height: 300px;
  }
}
</style>
=======
<template>
    <div class="chart-placeholder">
      <h2>💹 电影票房分析图表区域</h2>
      <!-- 图表内容未来添加 -->
    </div>
</template>
  
<style scoped>
  .chart-placeholder {
    padding: 2rem;
    background-color: #f9fafb;
    border-radius: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    text-align: center;
  }
</style>
  
>>>>>>> 2169fedfedc3d443e3192294224aa2ddb9a5d482

<template>
  <div class="dashboard-container">
    <!-- 榜单筛选 -->
    <div class="filter-container">
      <div class="filter-group">
        <label>榜单类型：</label>
        <select v-model="rankingFilter.type" @change="handleRankingTypeChange">
          <option value="total">总榜单</option>
          <option value="yearly">年度榜单</option>
          <option value="genre">类型榜单</option>
        </select>
      </div>
      <div class="filter-group" v-if="rankingFilter.type === 'yearly'">
        <label>年份：</label>
        <input 
          v-model.number="rankingFilter.year" 
          type="number" 
          min="2000" 
          :max="new Date().getFullYear()"
          @change="handleYearInput"
        >
      </div>
      <div class="filter-group" v-if="rankingFilter.type === 'genre'">
        <label>电影类型：</label>
        <input
          v-model="rankingFilter.genre"
          type="text"
          @change="fetchRankingData"
          placeholder="输入电影类型"
        >
      </div>
      <div class="filter-group">
        <label>显示数量：</label>
        <input 
          v-model.number="rankingFilter.limit" 
          type="number" 
          min="1" 
          max="50"
          @change="fetchRankingData"
        >
      </div>
    </div>

    <div class="chart-card">
      <div ref="rankingChart" class="chart"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

// 图表DOM引用
const rankingChart = ref<HTMLElement | null>(null)

// 筛选条件
const rankingFilter = ref({
  type: 'total',  // total/yearly/genre
  year: new Date().getFullYear(),
  genre: '',
  limit: 10
})

// 图表实例
let rankingChartInstance: echarts.ECharts | null = null

// 响应数据类型
interface RankingItem {
  rank: number
  movie_id: number
  title: string
  box_office: number
  country: string
  release_year: number
}

interface RankingData {
  success: boolean
  data: RankingItem[]
}

// 计算标题
const rankingTitle = computed(() => {
  if (rankingFilter.value.type === 'yearly') return `${rankingFilter.value.year}年度票房排行榜`
  if (rankingFilter.value.type === 'genre') return `${rankingFilter.value.genre}类型票房排行榜`
  return '历史总票房排行榜'
})

// 初始化图表
const initCharts = () => {
  if (rankingChart.value) {
    rankingChartInstance = echarts.init(rankingChart.value)
    window.addEventListener('resize', () => rankingChartInstance?.resize())
  }
}

// 处理榜单类型变化
const handleRankingTypeChange = () => {
  if (rankingFilter.value.type === 'yearly') {
    rankingFilter.value.year = new Date().getFullYear()
  } else if (rankingFilter.value.type === 'genre') {
    rankingFilter.value.genre = ''
  }
  fetchRankingData()
}

// 处理年份输入
const handleYearInput = () => {
  const currentYear = new Date().getFullYear()
  if (rankingFilter.value.year < 1800) {
    rankingFilter.value.year = 1900
  } else if (rankingFilter.value.year > currentYear) {
    rankingFilter.value.year = currentYear
  }
  fetchRankingData()
}

// 获取票房排行榜数据
const fetchRankingData = async () => {
  try {
    const params: any = {
      type: rankingFilter.value.type,
      limit: rankingFilter.value.limit
    }

    if (rankingFilter.value.type === 'yearly') {
      params.year = rankingFilter.value.year
    } else if (rankingFilter.value.type === 'genre') {
      params.genre = rankingFilter.value.genre
    }

    const { data } = await axios.get<RankingData>(
      `${API_BASE_URL}/api/basic/boxoffice/ranking`,
      { params }
    )

    if (data.success && rankingChartInstance) {
      // 按票房从高到低排序
      const sortedData = [...data.data].sort((a, b) => b.box_office - a.box_office)
      
      // 重新计算排名（可选）
      sortedData.forEach((item, index) => {
        item.rank = index + 1
      })

      const chartData = sortedData.map(item => ({
        name: item.title,
        value: item.box_office,
        itemStyle: {
          color: getColorByRank(item.rank)
        },
        meta: item // 保存完整数据用于tooltip
      }))

      rankingChartInstance.setOption({
        tooltip: {
          trigger: 'item',
          formatter: (params: any) => {
            const dataItem = params.data.meta
            return `
              <strong>${dataItem.title}</strong><br/>
              排名: 第${dataItem.rank}名<br/>
              票房: ${formatNumber(dataItem.box_office)}万元<br/>
              国家: ${dataItem.country}<br/>
              年份: ${dataItem.release_year}
            `
          }
        },
        xAxis: {
          type: 'value',
          name: '票房（万元）',
          axisLabel: {
            formatter: (value: number) => formatNumber(value) + '万'
          }
        },
        yAxis: {
          type: 'category',
          data: chartData.map(d => d.name),
          axisLabel: {
            interval: 0,
            width: 150,
            overflow: 'truncate',
            formatter: (value: string) => {
              return value.length > 10 ? value.substring(0, 10) + '...' : value
            }
          },
          inverse: true // 使图表从上到下显示
        },
        series: [{
          type: 'bar',
          data: chartData,
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => formatNumber(params.value) + '万'
          },
          itemStyle: {
            color: (params: any) => params.data.itemStyle.color
          }
        }],
        title: {
          text: rankingTitle.value,
          left: 'center',
          textStyle: {
            fontSize: 18,
            fontWeight: 'bold'
          }
        },
        grid: {
          left: '3%',
          right: '7%',
          bottom: '3%',
          containLabel: true
        }
      }, true)
    }
  } catch (error) {
    console.error('获取排行榜数据失败:', error)
  }
}

// 根据排名获取颜色
const getColorByRank = (rank: number): string => {
  const colors = [
    '#FF4500', // 第一名
    '#FF8C00', // 第二名
    '#FFA500', // 第三名
    '#1E90FF', // 4-6名
    '#4682B4', // 7-10名
  ]
  
  if (rank === 1) return colors[0]
  if (rank === 2) return colors[1]
  if (rank === 3) return colors[2]
  if (rank <= 6) return colors[3]
  return colors[4]
}

// 数字格式化
const formatNumber = (num: number): string => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

onMounted(() => {
  initCharts()
  fetchRankingData()
})
</script>
<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
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
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #606266;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
  color: #606266;
}

.filter-group select:hover,
.filter-group input:hover {
  border-color: #c0c4cc;
}

.filter-group input {
  width: 120px;
}

.chart-card {
  margin-bottom: 30px;
  background-color: #e6f0ff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.chart {
  width: 100%;
  height: 500px;
}

@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    gap: 10px;
  }

  .chart {
    height: 350px;
  }
}
</style>
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
        <select v-model="rankingFilter.year" @change="fetchRankingData">
          <option v-for="y in availableYears" :value="y" :key="y">{{ y }}年</option>
        </select>
      </div>
      <div class="filter-group" v-if="rankingFilter.type === 'genre'">
        <label>电影类型：</label>
        <select v-model="rankingFilter.genre" @change="fetchRankingData">
          <option v-for="g in availableGenres" :value="g" :key="g">{{ g }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>显示数量：</label>
        <input v-model.number="rankingFilter.limit" type="number" min="1" @change="fetchRankingData">
      </div>
    </div>

    <div class="chart-card">
      <div ref="rankingChart" class="chart"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

// 图表DOM引用
const rankingChart = ref<HTMLElement | null>(null)
const costChart = ref<HTMLElement | null>(null)

// 可用年份
const availableYears = [2020, 2021, 2022, 2023]
// 可用电影类型
const availableGenres = ref(['动作', '喜剧', '科幻', '爱情', '悬疑'])

// 筛选条件
const rankingFilter = ref({
  type: 'total',  // total/yearly/genre
  year: 2023,
  genre: availableGenres.value[0], // 默认第一个类型
  limit: 10
})

const costFilter = ref({
  year: 'all',    // 默认所有年份
  genre: 'all'    // 默认所有类型
})

// 图表实例
let rankingChartInstance: echarts.ECharts | null = null
let costChartInstance: echarts.ECharts | null = null

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
  }
  if (costChart.value) {
    costChartInstance = echarts.init(costChart.value)
  }
}

// 处理榜单类型变化
const handleRankingTypeChange = () => {
  // 重置相关参数
  if (rankingFilter.value.type === 'yearly') {
    rankingFilter.value.year = availableYears[0]
  } else if (rankingFilter.value.type === 'genre') {
    rankingFilter.value.genre = availableGenres.value[0]
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
      'http://127.0.0.1:4523/m1/6680275-6389502-default/api/basic/boxoffice/ranking',
      { params }
    )

    if (data.success && rankingChartInstance) {
      const chartData = data.data.map(item => ({
        name: item.title,
        value: item.box_office
      }))

      rankingChartInstance.setOption({
        tooltip: {
          trigger: 'item',
          formatter: (params: any) => {
            const dataItem = data.data[params.dataIndex]
            return `
              ${dataItem.title}<br/>
              排名: ${dataItem.rank}<br/>
              票房: ${dataItem.box_office} 万元<br/>
              国家: ${dataItem.country}<br/>
              年份: ${dataItem.release_year}
            `
          }
        },
        xAxis: {
          type: 'value',
          name: '票房（万元）',
          axisLabel: {
            formatter: '{value} 万'
          }
        },
        yAxis: {
          type: 'category',
          data: chartData.map(d => d.name),
          axisLabel: {
            interval: 0,
            width: 100,
            overflow: 'truncate'
          }
        },
        series: [{
          type: 'bar',
          data: chartData.map(d => d.value),
          label: {
            show: true,
            position: 'right',
            formatter: '{c} 万元'
          },
          itemStyle: {
            color: (params: any) => {
              const colors = ['#3b82f6', '#6366f1', '#8b5cf6', '#ec4899']
              return colors[params.dataIndex % colors.length]
            }
          }
        }],
        title: {
          text: rankingTitle.value,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      })
    }
  } catch (error) {
    console.error('获取排行榜数据失败:', error)
  }
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

.filter-group select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
  color: #606266;
  cursor: pointer;
}

.filter-group select:hover {
  border-color: #c0c4cc;
}

.chart-card {
  margin-bottom: 30px;
  background: white;
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

.filter-group input {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  width: 80px;
  /* 固定宽度 */
}
</style>
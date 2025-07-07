<template>
  <div class="dashboard">
    <h1>🎬 导演数据分析</h1>

    <!-- 票房排行榜 -->
    <div class="chart-card">
      <h2>导演票房排行榜</h2>
      <div class="filter-container">
        <div class="filter-group">
          <label>开始年份：</label>
          <select v-model="startYear">
            <option v-for="year in years" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>结束年份：</label>
          <select v-model="endYear">
            <option v-for="year in years" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>显示数量：</label>
          <select v-model="topN">
            <option v-for="n in 10" :value="n">前{{ n }}名</option>
          </select>
        </div>
      </div>
      <div ref="boxOfficeChart" class="chart"></div>
    </div>

    <!-- 评分分析（重构） -->
    <div class="chart-card">
      <h2>导演评分分析</h2>
      <div class="filter-container">
        <div class="filter-group">
          <label>开始年份：</label>
          <select v-model="ratingStartYear">
            <option v-for="year in years" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>结束年份：</label>
          <select v-model="ratingEndYear">
            <option v-for="year in years" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>显示数量：</label>
          <select v-model="ratingTopN">
            <option v-for="n in 10" :value="n">前{{ n }}名</option>
          </select>
        </div>
        <div class="filter-group">
          <button @click="fetchRatingChartData">获取评分排行</button>
        </div>
      </div>
      <div ref="ratingChart" class="chart"></div>
    </div>

    <!-- 类型偏好 -->
    <div class="chart-card">
      <h2>导演类型偏好</h2>
      <div class="filter-container">
        <div class="filter-group">
          <label>搜索导演：</label>
          <input v-model="searchDirector" type="text" placeholder="请输入导演姓名" />
          <button @click="fetchGenreData">搜索</button>
        </div>
        <div class="filter-group">
          <label>开始年份：</label>
          <select v-model="genreStartYear">
            <option v-for="year in years" :value="year">{{ year }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>结束年份：</label>
          <select v-model="genreEndYear">
            <option v-for="year in years" :value="year">{{ year }}</option>
          </select>
        </div>
      </div>
      <div ref="genreChart" class="chart"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

const years = Array.from({ length: 30 }, (_, i) => 1995 + i)
const startYear = ref(2010)
const endYear = ref(2023)
const topN = ref(10)
const ratingTopN = ref(5)
const ratingStartYear = ref(2010)
const ratingEndYear = ref(2023)
const searchDirector = ref('')
const genreStartYear = ref(2010)
const genreEndYear = ref(2023)

const boxOfficeChart = ref(null)
const ratingChart = ref(null)
const genreChart = ref(null)
let boxOfficeChartInstance = null
let ratingChartInstance = null
let genreChartInstance = null

const fetchBoxOfficeData = async () => {
  const res = await axios.get(`${API_BASE_URL}/production-ranking`, {
    params: {
      startYear: startYear.value,
      endYear: endYear.value,
      top_N: topN.value
    }
  })
  const data = res.data.ranking
  if (!boxOfficeChartInstance && boxOfficeChart.value && boxOfficeChart.value.clientWidth > 0) {
    boxOfficeChartInstance = echarts.init(boxOfficeChart.value)
  }
  boxOfficeChartInstance.setOption({
    tooltip: {
      trigger: 'item',
      formatter: p => `导演：${p.data.name}<br>票房：${p.data.totalBoxOffice}亿<br>作品数：${p.data.totalMovies}部`
    },
    xAxis: { type: 'value', name: '票房 (亿元)' },
    yAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: { interval: 0, rotate: 30 }
    },
    series: [
      {
        type: 'bar',
        data: data.map(item => ({ ...item, value: item.totalBoxOffice })),
        label: { show: true, position: 'right', formatter: '{c} 亿' },
        itemStyle: { color: '#5470C6' }
      }
    ]
  })
}

const fetchRatingChartData = async () => {
  const res = await axios.get(`${API_BASE_URL}/director_score`, {
    params: {
      startYear: ratingStartYear.value,
      endYear: ratingEndYear.value,
      topN: ratingTopN.value
    }
  })
  const data = res.data.data
  if (!ratingChartInstance && ratingChart.value && ratingChart.value.clientWidth > 0) {
    ratingChartInstance = echarts.init(ratingChart.value)
  }
  ratingChartInstance.setOption({
    tooltip: {
      trigger: 'item',
      formatter: p => `导演：${p.data.name}<br>平均评分：${p.data.value}<br>代表作品：<br>${p.data.movies.join('<br>')}`
    },
    xAxis: { type: 'value', name: '平均评分', min: 0, max: 10 },
    yAxis: {
      type: 'category',
      data: data.map(d => d.name),
      axisLabel: { interval: 0, rotate: 30 }
    },
    series: [
      {
        type: 'bar',
        data: data.map(item => ({
          name: item.name,
          value: item.averageRating,
          movies: item.movies
        })),
        label: { show: true, position: 'right', formatter: '{c}' },
        itemStyle: { color: '#91cc75' }
      }
    ]
  })
}

const fetchGenreData = async () => {
  if (!searchDirector.value) return
  const res = await axios.get(`${API_BASE_URL}/director_like`, {
    params: {
      director_name: searchDirector.value,
      startYear: genreStartYear.value,
      endYear: genreEndYear.value
    }
  })
  const data = res.data.data
  if (!genreChartInstance && genreChart.value && genreChart.value.clientWidth > 0) {
    genreChartInstance = echarts.init(genreChart.value)
  }
  genreChartInstance.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}部 ({d}%)' },
    legend: { orient: 'vertical', right: 10, top: 'center' },
    series: [
      {
        name: '类型偏好',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
        label: { show: true, formatter: '{b}: {c}部' },
        data: data.genreCounts.map(item => ({ name: item.genre, value: item.count }))
      }
    ]
  })
}

onMounted(() => {
  nextTick(() => {
    fetchBoxOfficeData()
  })
  window.addEventListener('resize', () => {
    boxOfficeChartInstance?.resize()
    ratingChartInstance?.resize()
    genreChartInstance?.resize()
  })
})

watch([startYear, endYear, topN], fetchBoxOfficeData)
watch([ratingStartYear, ratingEndYear, ratingTopN], fetchRatingChartData)
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.chart-card {
  background-color: #e6f0ff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 30px;
}

.chart-card h2 {
  margin-top: 0;
  color: #555;
  font-size: 1.5rem;
}

.filter-container {
  display: flex;
  gap: 15px;
  margin: 15px 0;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
}

.filter-group label {
  margin-right: 8px;
  font-size: 0.9rem;
  white-space: nowrap;
}

select, input, button {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  background-color: #fff;
  min-width: 100px;
}

button {
  background-color: #409EFF;
  color: white;
  border: none;
  cursor: pointer;
}

.chart {
  width: 100%;
  height: 400px;
  margin-top: 15px;
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

<template>
  <div class="dashboard">
    <!-- <h1>🎬 导演数据分析</h1> -->

    <!-- 票房排行榜 -->
    <div class="chart-card">
      <h2>导演票房排行榜</h2>
      <div class="filter-container">
        <div class="filter-group">
          <label>开始年份：</label>
          <input v-model.number="startYear" type="number" @change="validateYear('startYear')" />
        </div>
        <div class="filter-group">
          <label>结束年份：</label>
          <input v-model.number="endYear" type="number" @change="validateYear('endYear')" />
        </div>
        <div class="filter-group">
          <label>显示数量：</label>
          <input v-model.number="topN" type="number" min="1" max="50" @change="validateTopN('topN')" />
        </div>
        <div class="filter-group">
          <button @click="fetchBoxOfficeData">获取数据</button>
        </div>
      </div>
      <div ref="boxOfficeChart" class="chart"></div>
    </div>

    <!-- 评分分析 -->
    <div class="chart-card">
      <h2>导演评分分析</h2>
      <div class="filter-container">
        <div class="filter-group">
          <label>开始年份：</label>
          <input v-model.number="ratingStartYear" type="number" @change="validateYear('ratingStartYear')" />
        </div>
        <div class="filter-group">
          <label>结束年份：</label>
          <input v-model.number="ratingEndYear" type="number" @change="validateYear('ratingEndYear')" />
        </div>
        <div class="filter-group">
          <label>显示数量：</label>
          <input v-model.number="ratingTopN" type="number" min="1" max="50" @change="validateTopN('ratingTopN')" />
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
          <label>选择导演：</label>
          <input v-model="searchQuery" @input="filterDirectors" placeholder="搜索导演" />
        </div>
        <div class="filter-group">
          <label>开始年份：</label>
          <input v-model.number="genreStartYear" type="number" @change="validateYear('genreStartYear')" />
        </div>
        <div class="filter-group">
          <label>结束年份：</label>
          <input v-model.number="genreEndYear" type="number" @change="validateYear('genreEndYear')" />
        </div>
        <div class="filter-group">
          <button @click="fetchGenreData">获取偏好</button>
        </div>
      </div>
      <div ref="genreChart" class="chart"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

// 年份和显示数量输入框
const startYear = ref(1990)
const endYear = ref(2023)
const topN = ref(10)
const ratingTopN = ref(5)
const ratingStartYear = ref(1990)
const ratingEndYear = ref(2023)
const genreDirector = ref('')
const genreStartYear = ref(1990)
const genreEndYear = ref(2023)
const searchQuery = ref('')
const filteredDirectors = ref([])

const boxOfficeChart = ref(null)
const ratingChart = ref(null)
const genreChart = ref(null)
let boxOfficeChartInstance = null
let ratingChartInstance = null
let genreChartInstance = null

const directorNames = ref([])

// 元转亿元并保留2位小数
const yuanToYi = (yuan) => {
  return parseFloat((yuan / 100000000).toFixed(2))
}

// 年份验证
const validateYear = (field) => {
  const currentYear = new Date().getFullYear()
  const value = refs[field].value
  if (value < 1900) refs[field].value = 1900
  if (value > currentYear) refs[field].value = currentYear
}

// 显示数量验证
const validateTopN = (field) => {
  const value = refs[field].value
  if (value < 1) refs[field].value = 1
  if (value > 50) refs[field].value = 50
}

//导演票房分析
const fetchBoxOfficeData = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/production-ranking`, {
      params: {
        startYear: startYear.value,
        endYear: endYear.value,
        top_N: topN.value
      }
    })
    
    const data = res.data.ranking.map(item => ({
      ...item,
      totalBoxOffice: yuanToYi(item.totalBoxOffice) // 转换为亿元
    }))
    
    directorNames.value = data.map(item => item.name)
    filteredDirectors.value = directorNames.value
    
    if (!boxOfficeChartInstance && boxOfficeChart.value) {
      boxOfficeChartInstance = echarts.init(boxOfficeChart.value)
    }
    
    boxOfficeChartInstance.setOption({
      tooltip: {
        trigger: 'item',
        formatter: p => `导演：${p.data.name}<br>票房：${p.data.totalBoxOffice}亿<br>作品数：${p.data.totalMovies}部`
      },
      xAxis: { 
        type: 'value', 
        name: '票房 (亿元)',
        axisLabel: {
          formatter: '{value} 亿'
        }
      },
      yAxis: {
        inverse: true,
        type: 'category',
        data: data.map(item => item.name),
        axisLabel: { interval: 0, rotate: 30 }
      },
      series: [
        {
          type: 'bar',
          data: data.map(item => ({ 
            ...item, 
            value: item.totalBoxOffice 
          })),
          label: { 
            show: true, 
            position: 'right', 
            formatter: '{c} 亿' 
          },
          itemStyle: { color: '#5470C6' }
        }
      ]
    })
  } catch (error) {
    console.error('获取票房数据失败:', error)
  }
}

//导演评分分析
const fetchRatingChartData = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/director_score`, {
      params: {
        startYear: ratingStartYear.value,
        endYear: ratingEndYear.value,
        topN: ratingTopN.value
      }
    })

    const rawData = Array.isArray(res.data?.data) ? res.data.data : []
    if (!rawData.length) {
      console.error('返回的数据为空或格式不正确：', res.data)
      return
    }

    if (!ratingChartInstance && ratingChart.value) {
      ratingChartInstance = echarts.init(ratingChart.value)
    }

    ratingChartInstance.setOption({
      tooltip: {
        trigger: 'item',
        formatter: p => `导演：${p.data.name}<br>平均评分：${p.data.value}<br>代表作品：<br>${p.data.movies.join('<br>')}`
      },
      xAxis: { 
        type: 'value', 
        name: '平均评分', 
        min: 0, 
        max: 10 
      },
      yAxis: {
        inverse: true,
        type: 'category',
        data: rawData.map(d => d.name),
        axisLabel: { interval: 0, rotate: 30 }
      },
      series: [
        {
          type: 'bar',
          data: rawData.map(item => ({
            name: item.name,
            value: item.averageRating,
            movies: item.movies
          })),
          label: { show: true, position: 'right', formatter: '{c}' },
          itemStyle: { color: '#91cc75' }
        }
      ]
    })
  } catch (err) {
    console.error('获取导演评分数据失败：', err)
  }
}

//导演类型偏好
const fetchGenreData = async () => {
  // 🔧 在点击按钮时同步导演姓名
  genreDirector.value = searchQuery.value.trim()
  if (!genreDirector.value) {
    console.warn('导演姓名为空，已取消请求')
    return
  }

  try {
    const params = {
      director_name: genreDirector.value,
      startYear: genreStartYear.value,
      endYear: genreEndYear.value
    }
    console.log('请求参数：', params)

    const res = await axios.get(`http://localhost:5000/director_like`, {
      params
    })
    console.log('返回数据：', res)

    const rawData = Array.isArray(res.data?.data?.genreCounts) ? res.data.data.genreCounts : []
    if (!rawData.length) {
      console.error('返回的数据为空或格式不正确：', res.data)
      return
    }

    if (!genreChartInstance && genreChart.value) {
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
          itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
          label: { show: true, formatter: '{b}: {c}部' },
          data: rawData.map(item => ({ name: item.genre, value: item.count }))
        }
      ]
    })
  } catch (err) {
    console.error('获取导演类型偏好失败：', err)
  }
}

const filterDirectors = () => {
  const query = searchQuery.value.toLowerCase()
  filteredDirectors.value = directorNames.value.filter(director => director.toLowerCase().includes(query))
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
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 0.9rem;
  white-space: nowrap;
  min-width: 70px;
}

input {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  background-color: #fff;
  width: 80px;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  background-color: #409EFF;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
}

button:hover {
  background-color: #66b1ff;
}

.chart {
  width: 100%;
  height: 400px;
  margin-top: 15px;
}

@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .filter-group {
    width: 100%;
  }

  input {
    width: 100%;
    max-width: 100px;
  }

  .chart {
    height: 300px;
  }
}

.input-error {
  border-color: #f56c6c !important;
}

.error-message {
  color: #f56c6c;
  padding: 8px;
  margin: 8px 0;
  background-color: #fef0f0;
  border-radius: 4px;
  font-size: 14px;
}
</style>
<template>
  <div class="actor-dashboard">
    <!-- <h1>🧑‍🎤 演员数据分析（单人搜索）</h1> -->

    <!-- 筛选条件 -->
    <div class="filter-container">
      <div class="filter-group">
        <label>搜索演员：</label>
        <input 
          v-model="searchActor" 
          type="text" 
          placeholder="请输入演员姓名" 
          @keyup.enter="fetchActorData"
        />
        <button @click="fetchActorData">搜索</button>
      </div>
      <div class="filter-group">
        <label>开始年份：</label>
        <input 
          v-model.number="startYear" 
          type="number" 
          min="1900"
          :max="currentYear"
        />
      </div>
      <div class="filter-group">
        <label>结束年份：</label>
        <input 
          v-model.number="endYear" 
          type="number" 
          min="1900"
          :max="currentYear"
        />
      </div>
    </div>

    <!-- 演员类型偏好 -->
    <div class="chart-card">
      <h2>演员类型偏好</h2>
      <div v-if="actorData">
        <p><strong>参演电影数量：</strong> {{ actorData.totalMovies }} 部</p>
        <p><strong>平均评分：</strong> {{ actorData.overallRating.average }} 分</p>
      </div>
      <div ref="genreChart" class="chart"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

const searchActor = ref('')
const startYear = ref(2018)
const endYear = ref(2023)
const currentYear = new Date().getFullYear()

const genreChart = ref(null)
let genreChartInstance = null

const actorData = ref(null)

const fetchActorData = async () => {
  if (!searchActor.value) return
  
  try {
    const res = await axios.get(`${API_BASE_URL}/actor`, {
      params: {
        actor_name: searchActor.value,
        startYear: startYear.value,
        endYear: endYear.value
      }
    })
    actorData.value = res.data.data
    updateGenreChart()
  } catch (err) {
    console.error('获取演员数据失败：', err)
    actorData.value = null
    clearChart() // 出错时清空图表
  }
}

const updateGenreChart = () => {
  if (!actorData.value) {
    clearChart()
    return
  }
  
  const data = actorData.value.genreStats?.map(g => ({ 
    name: g.genre, 
    value: g.count 
  })) || []
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center'
    },
    series: [
      {
        name: '类型偏好',
        type: 'pie',
        radius: ['40%', '70%'],
        data,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c}次'
        }
      }
    ]
  }
  
  if (!genreChartInstance && genreChart.value) {
    genreChartInstance = echarts.init(genreChart.value)
  }
  genreChartInstance.setOption(option)
}

const clearChart = () => {
  if (genreChartInstance) {
    genreChartInstance.clear() // 清空图表
  }
}

onMounted(() => {
  window.addEventListener('resize', () => {
    genreChartInstance?.resize()
  })
})
</script>

<style scoped>
.actor-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.filter-container {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #e6f0ff;
  border-radius: 8px;
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
  width: 100px;
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
  font-size: 1.3rem;
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
    max-width: 120px;
  }

  .chart {
    height: 300px;
  }
}
</style>
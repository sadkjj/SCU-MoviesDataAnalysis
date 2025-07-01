<template>
  <div class="analysis-container">
    <div class="chart-placeholder">
    <!-- 年度产量筛选器 -->
    <div class="filter-group">
      <label>起始年份：<input v-model="startYear" type="number" min="2000" max="2025" /></label>
      <label>结束年份：<input v-model="endYear" type="number" min="2000" max="2025" /></label>
      <label>国家：<select v-model="selectedCountry">
        <option>全部</option>
        <option>中国</option>
        <option>美国</option>
        <option>韩国</option>
        <option>日本</option>
      </select></label>
      <button @click="updateYearChart">更新</button>
    </div>

    <div class="chart-section">
      <h3>年度电影产量趋势</h3>
      <div ref="yearChart" class="chart"></div>
    </div>

    <!-- 月度产量筛选器 -->
    <div class="filter-group">
      <label>年份：<input v-model="selectedMonthYear" type="number" min="2000" max="2025" /></label>
      <button @click="updateMonthChart">更新</button>
    </div>

    <div class="chart-section">
      <h3>月度电影产量趋势</h3>
      <div ref="monthChart" class="chart"></div>
    </div>

    <!-- 国家产量筛选器 -->
    <div class="filter-group">
      <label>年份：<input v-model="selectedRegionYear" type="number" min="2000" max="2025" /></label>
      <button @click="updateRegionChart">更新</button>
    </div>

    <div class="chart-section">
      <h3>国家/地区电影产量对比</h3>
      <div ref="regionChart" class="chart"></div>
    </div>
  </div>

    </div>

</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as echarts from 'echarts'

const yearChart = ref(null)
const monthChart = ref(null)
const regionChart = ref(null)

const startYear = ref(2018)
const endYear = ref(2023)
const selectedCountry = ref('全部')
const selectedMonthYear = ref(2023)
const selectedRegionYear = ref(2023)

function updateYearChart() {
  const yearInstance = echarts.init(yearChart.value)
  const years = []
  const values = []
  for (let y = startYear.value; y <= endYear.value; y++) {
    years.push(y.toString())
    values.push(Math.floor(Math.random() * 300 + 200))
  }
  yearInstance.setOption({
    xAxis: { type: 'category', data: years },
    yAxis: { type: 'value' },
    series: [{ type: 'line', data: values, smooth: true, areaStyle: {} }],
    title: { text: '年度产量', left: 'center' }
  })
}

function updateMonthChart() {
  const monthInstance = echarts.init(monthChart.value)
  monthInstance.setOption({
    xAxis: {
      type: 'category',
      data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: Array.from({ length: 12 }, () => Math.floor(Math.random() * 100 + 30)),
      itemStyle: { color: '#5470C6' }
    }],
    title: { text: `${selectedMonthYear.value}年 月度产量`, left: 'center' }
  })
}

function updateRegionChart() {
  const regionInstance = echarts.init(regionChart.value)
  regionInstance.setOption({
    tooltip: {},
    xAxis: {
      type: 'category',
      data: ['中国', '美国', '韩国', '日本', '英国', '法国']
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: Array.from({ length: 6 }, () => Math.floor(Math.random() * 800 + 200)),
      itemStyle: { color: '#91cc75' }
    }],
    title: { text: `${selectedRegionYear.value}年 地区产量`, left: 'center' }
  })
}

onMounted(() => {
  updateYearChart()
  updateMonthChart()
  updateRegionChart()
})
</script>

<style scoped>
.analysis-container {
  padding: 2rem;
  color: #333;
}

.chart-placeholder {
  padding: 2rem;
  background-color: #fefce8;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-align: center;
  margin-bottom: 2rem;
}

.chart-section {
  margin-bottom: 2rem;
}

.chart {
  width: 100%;
  height: 400px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: #f1f5f9;
  border-radius: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group input,
.filter-group select {
  padding: 0.4rem 0.6rem;
  border-radius: 0.375rem;
  border: 1px solid #ccc;
}

.filter-group button {
  padding: 0.4rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}

.filter-group button:hover {
  background-color: #2563eb;
}
</style>

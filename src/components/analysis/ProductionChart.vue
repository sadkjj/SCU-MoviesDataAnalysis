<template>
  <div class="chart-placeholder">

  <div class="chart-row">

    <div class="chart-section">
      <h3>年度电影产量趋势</h3>
      <div ref="yearChart" class="chart"></div>
    </div>

    <div class="chart-section">
        <h3>月度电影产量趋势</h3>
        <div ref="monthChart" class="chart"></div>
    </div>

  </div>

  
  <div class="chart-row">

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
const genreChart = ref(null)

onMounted(() => {
const yearInstance = echarts.init(yearChart.value)
yearInstance.setOption({
  xAxis: {
    type: 'category',
    data: ['2018', '2019', '2020', '2021', '2022', '2023']
  },
  yAxis: { type: 'value' },
  series: [{
    type: 'line',
    data: [320, 450, 300, 500, 620, 710],
    smooth: true,
    areaStyle: {}
  }],
  title: { text: '年度产量', left: 'center' }
})

const monthInstance = echarts.init(monthChart.value)
monthInstance.setOption({
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar',
    data: [40, 50, 65, 70, 60, 80, 100, 90, 70, 60, 55, 50],
    itemStyle: { color: '#5470C6' }
  }],
  title: { text: '月度产量', left: 'center' }
})

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
    data: [500, 800, 300, 400, 350, 280],
    itemStyle: { color: '#91cc75' }
  }],
  title: { text: '地区对比', left: 'center' }
})

})
</script>

<style scoped>
.analysis-container {
padding: 2rem;
color: #333;
}

.chart-placeholder {
padding: 2rem;
background-color: #f9fafb;
border-radius: 1rem;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
text-align: center;
margin-bottom: 2rem;
}

.chart-section {
margin-bottom: 2rem;
flex: 1;


}

.chart-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.chart {
width: 100%;
height: 400px;
}
</style>
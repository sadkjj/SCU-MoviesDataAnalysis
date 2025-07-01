<template>
  <div class="chart-placeholder">
    <h2>📊-💰 类型与票房分析</h2>
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)

const mockData = [
  { type: '动画', avgBoxOffice: 8.7, maxBoxOffice: 50.1, minBoxOffice: 0.1, totalBoxOffice: 215.3 },
  { type: '剧情', avgBoxOffice: 12.3, maxBoxOffice: 88.2, minBoxOffice: 0.5, totalBoxOffice: 500.1 },
  { type: '动作', avgBoxOffice: 15.4, maxBoxOffice: 100.7, minBoxOffice: 0.3, totalBoxOffice: 620.9 },
  { type: '喜剧', avgBoxOffice: 10.1, maxBoxOffice: 70.5, minBoxOffice: 0.2, totalBoxOffice: 430.2 },
  { type: '爱情', avgBoxOffice: 6.8, maxBoxOffice: 40.9, minBoxOffice: 0.1, totalBoxOffice: 300.0 }
]

onMounted(() => {
  const chart = echarts.init(chartRef.value)

  const types = mockData.map(d => d.type)
  const avg = mockData.map(d => d.avgBoxOffice)
  const max = mockData.map(d => d.maxBoxOffice)
  const min = mockData.map(d => d.minBoxOffice)
  const total = mockData.map(d => d.totalBoxOffice)

  chart.setOption({
    title: {
      text: '不同类型电影与票房关系',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      bottom: 10
    },
    xAxis: {
      type: 'category',
      data: types
    },
    yAxis: {
      type: 'value',
      name: '票房（亿）'
    },
    series: [
      {
        name: '平均票房',
        type: 'bar',
        data: avg
      },
      {
        name: '最高票房',
        type: 'bar',
        data: max
      },
      {
        name: '最低票房',
        type: 'bar',
        data: min
      },
      {
        name: '总票房',
        type: 'bar',
        data: total
      }
    ]
  })
})
</script>

<style scoped>
.chart-placeholder {
  padding: 2rem;
  background-color: #fefce8;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-align: center;
}

/* 图表容器 */
.chart {
  width: 100%;
  height: 420px;
  margin-top: 1rem;
}
</style>

<template>
  <div class="chart-placeholder">
    <h2>📊 类型分析</h2>
    <div ref="genreChart" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import * as echarts from 'echarts'

// 图表容器引用
const genreChart = ref<HTMLDivElement | null>(null)

onMounted(() => {
  const chart = echarts.init(genreChart.value!)

  chart.setOption({
    title: {
      text: '不同种类电影占比',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      bottom: 10,
      left: 'center'
    },
    series: [
      {
        name: '电影类型',
        type: 'pie',
        radius: '60%',
        data: [
          { value: 320, name: '剧情' },
          { value: 240, name: '动作' },
          { value: 180, name: '喜剧' },
          { value: 150, name: '爱情' },
          { value: 120, name: '科幻' },
          { value: 100, name: '悬疑' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
          }
        }
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

/* 图表容器尺寸设置 */
.chart {
  width: 100%;
  height: 400px;
  margin-top: 1rem;
}
</style>

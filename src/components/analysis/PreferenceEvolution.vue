<template>
  <div class="section">
    <h2>🔄 观影偏好变化趋势</h2>
    
    <!-- 筛选区域 -->
    <div class="filter-container">
      <div class="filter-group">
        <label>电影类型：</label>
        <input 
          v-model="customType" 
          placeholder="输入电影类型，如：科幻"
          class="type-input"
        />
      </div>
      
      <div class="filter-group">
        <label>开始时间：</label>
        <select v-model="startMonth" @change="clearError">
          <option v-for="month in availableMonths" :value="month.value">{{ month.label }}</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>结束时间：</label>
        <select v-model="endMonth" @change="clearError">
          <option v-for="month in availableMonths" :value="month.value">{{ month.label }}</option>
        </select>
      </div>
      
      <button @click="fetchData" class="query-btn">查询</button>
    </div>
    
    <!-- 错误提示 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    
    <!-- 图表容器 -->
    <div v-if="!errorMessage" ref="chart" class="chart-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import axios from 'axios'

// 当前日期用于计算最近12个月
const currentDate = new Date()
const currentYear = currentDate.getFullYear()
const currentMonth = currentDate.getMonth() + 1

// 生成最近12个月的选项
const availableMonths = computed(() => {
  const months = []
  let year = currentYear
  let month = currentMonth
  
  for (let i = 0; i < 12; i++) {
    months.unshift({
      value: `${year}-${month.toString().padStart(2, '0')}`,
      label: `${year}年${month}月`
    })
    
    month--
    if (month === 0) {
      month = 12
      year--
    }
  }
  return months
})

// 默认选中最近3个月
const defaultStartMonth = computed(() => {
  if (availableMonths.value.length >= 3) {
    return availableMonths.value[availableMonths.value.length - 3].value
  }
  return availableMonths.value[0]?.value || ''
})

const defaultEndMonth = computed(() => {
  return availableMonths.value[availableMonths.value.length - 1]?.value || ''
})

// 筛选条件
const customType = ref('')
const startMonth = ref(defaultStartMonth.value)
const endMonth = ref(defaultEndMonth.value)
const errorMessage = ref('')

// 图表相关
const chart = ref<HTMLElement | null>(null)
let chartInstance: ECharts | null = null

// 清除错误信息
const clearError = () => {
  errorMessage.value = ''
}

// 验证日期是否合法
const validateDates = () => {
  if (!startMonth.value || !endMonth.value) {
    errorMessage.value = '请选择完整的时间范围'
    return false
  }

  const start = new Date(startMonth.value)
  const end = new Date(endMonth.value)

  if (start > end) {
    errorMessage.value = '请重新筛选时间：结束时间不能早于开始时间'
    return false
  }

  // 限制查询范围不超过12个月
  const diffMonths = (end.getFullYear() - start.getFullYear()) * 12 + (end.getMonth() - start.getMonth()) + 1
  if (diffMonths > 12) {
    errorMessage.value = '查询时间范围不能超过12个月'
    return false
  }

  return true
}

// 从接口获取数据
const fetchData = async () => {
  if (!validateDates()) return
  try {
    errorMessage.value = ''
    const response = await axios.get('http://127.0.0.1:4523/m1/6680275-6389502-default/preference', {
      params: {
        type: customType.value,
        start_month: startMonth.value,
        end_month: endMonth.value
      }
    })

    renderChart(response.data)
  } catch (error) {
    console.error('获取数据失败:', error)
    errorMessage.value = '获取数据失败，请稍后重试'
    clearChart()
  }
}

// 渲染图表
const renderChart = (data: any) => {
  nextTick(() => {
    if (!chart.value) return

    if (chartInstance) {
      chartInstance.dispose()
    }
    chartInstance = echarts.init(chart.value)

    chartInstance.setOption({
      title: {
        text: `${customType.value || '电影'}观影人次趋势`,
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any[]) => {
          const index = params[0].dataIndex
          return `
            <div>${data.times[index]}</div>
            <div style="color:#91cc75">观影人次: ${data.attendees[index]} 万人次</div>
          `
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: data.times,
        axisLabel: { 
          rotate: 45,
          formatter: (value: string) => {
            return value.split('-')[1] + '月'
          }
        }
      },
      yAxis: {
        type: 'value',
        name: '观影人次 (万)',
        axisLine: { lineStyle: { color: '#91cc75' } }
      },
      series: [
        {
          name: '观影人次',
          type: 'line',
          data: data.attendees,
          itemStyle: { color: '#91cc75' },
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(145, 204, 117, 0.8)' },
              { offset: 1, color: 'rgba(145, 204, 117, 0.1)' }
            ])
          }
        }
      ]
    })
  })
}

// 清空图表
const clearChart = () => {
  if (chartInstance) {
    chartInstance.clear()
  }
}

// 响应式调整图表大小
const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.section {
  background-color: #fef2f2;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.filter-container {
  display: flex;
  gap: 15px;
  margin: 20px 0;
  flex-wrap: wrap;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #666;
}

.type-input {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  min-width: 120px;
}

select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
  min-width: 100px;
}

.query-btn {
  padding: 8px 20px;
  background-color: #f43f5e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.query-btn:hover {
  background-color: #fb7185;
}

.error-message {
  color: #f43f5e;
  margin: 15px 0;
  padding: 10px;
  background-color: #fff1f2;
  border-radius: 4px;
  border: 1px solid #fecdd3;
}

.chart-container {
  width: 100%;
  height: 400px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .filter-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-group {
    width: 100%;
    justify-content: space-between;
  }
  
  .type-input, select {
    flex: 1;
  }
  
  .query-btn {
    width: 100%;
  }
  
  .chart-container {
    height: 300px;
  }
}
</style>
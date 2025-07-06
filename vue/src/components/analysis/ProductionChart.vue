<template>
  <div class="analysis-container">
    <div class="chart-placeholder">
      <!-- 年度产量筛选器 -->
      <div class="filter-group">
        <label>起始年份：<input v-model="startYear" type="number" min="2000" max="2025" /></label>
        <label>结束年份：<input v-model="endYear" type="number" min="2000" max="2025" /></label>
        <label>国家：<input v-model="selectedCountry" type="text" placeholder="输入国家（默认全部）" /></label>
        <button @click="fetchYearlyProduction">更新</button>
      </div>

      <div class="chart-section">
        <h3>年度电影产量趋势</h3>
        <div ref="yearChart" class="chart"></div>
      </div>

      <!-- 月度产量筛选器 -->
      <div class="filter-group">
        <label>年份：<input v-model="selectedMonthYear" type="number" min="2000" max="2025" /></label>
        <label>国家：<input v-model="selectedMonthCountry" type="text" placeholder="输入国家（默认全部）" /></label>
        <button @click="fetchMonthlyProduction">更新</button>
      </div>

      <div class="chart-section">
        <h3>月度电影产量趋势</h3>
        <div ref="monthChart" class="chart"></div>
      </div>

      <!-- 国家产量筛选器 -->
      <div class="filter-group">
        <label>年份：<input v-model="selectedRegionYear" type="number" min="2000" max="2025" /></label>
        <button @click="fetchCountryProduction">更新</button>
      </div>

      <div class="chart-section">
        <h3>国家/地区电影产量对比</h3>
        <div ref="regionChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/api'
// 图表DOM引用
const yearChart = ref<HTMLElement | null>(null)
const monthChart = ref<HTMLElement | null>(null)
const regionChart = ref<HTMLElement | null>(null)

// 接口响应类型定义
interface YearlyProductionData {
  success: boolean
  data: {
    labels: string[]
    datasets: Array<{
      label: string
      data: number[]
    }>
  }
}

interface MonthlyProductionData {
  success: boolean
  data: {
    labels: string[]
    datasets: Array<{
      label: string
      data: number[]
    }>
  }
}

interface CountryProductionData {
  success: boolean
  data: Array<{
    country: string
    count: number
    percentage: number
  }>
}

// 请求参数
const startYear = ref(2018)
const endYear = ref(2023)
const selectedCountry = ref('')
const selectedMonthCountry = ref('')
const selectedMonthYear = ref(2023)
const selectedRegionYear = ref(2023)

// 数据状态
const loading = reactive({
  yearly: false,
  monthly: false,
  regional: false
})

const errorMessage = ref('')

// 图表实例
let yearChartInstance: echarts.ECharts | null = null
let monthChartInstance: echarts.ECharts | null = null
let regionChartInstance: echarts.ECharts | null = null

// 初始化图表
const initCharts = () => {
  if (yearChart.value) {
    yearChartInstance = echarts.init(yearChart.value)
  }
  if (monthChart.value) {
    monthChartInstance = echarts.init(monthChart.value)
  }
  if (regionChart.value) {
    regionChartInstance = echarts.init(regionChart.value)
  }
}

/* 年度产量接口 */
const fetchYearlyProduction = async () => {
  try {
    loading.yearly = true
    errorMessage.value = ''

    const params: any = {
      start_year: startYear.value,
      end_year: endYear.value
    }

    // 只有当用户输入了国家时才添加country参数
    if (selectedCountry.value.trim()) {
      params.country = selectedCountry.value.trim()
    }

    const { data } = await axios.get<YearlyProductionData>(
      `${API_BASE_URL}/api/basic/production/yearly`,
      { params }
    )

    if (data.success && yearChartInstance) {
      const yearLabels = data.data.labels.map(year => `${year}年`)

      // 根据是否输入国家决定显示哪个数据集
      const selectedDataset = selectedCountry.value.trim() === ''
        ? data.data.datasets.find(d => d.label === '总产量')
        : data.data.datasets.find(d => d.label === selectedCountry.value.trim())

      if (!selectedDataset) {
        console.error('未找到匹配的数据集')
        return
      }

      const option = {
        xAxis: {
          type: 'category',
          data: yearLabels,
          axisLabel: {
            interval: 0,
            rotate: yearLabels.length > 5 ? 30 : 0,
            color: '#333',
            fontSize: 12
          },
          axisLine: {
            lineStyle: {
              color: '#6E7079'
            }
          },
          axisTick: {
            alignWithLabel: true
          }
        },
        yAxis: {
          type: 'value',
          name: '产量（部）',
          nameTextStyle: {
            padding: [0, 0, 0, 40]
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#6E7079'
            }
          },
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        series: [{
          name: selectedDataset.label,
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            width: 3,
            color: '#5470C6'
          },
          itemStyle: {
            color: '#5470C6'
          },
          data: selectedDataset.data,
          emphasis: {
            itemStyle: {
              borderColor: '#000',
              borderWidth: 2
            }
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}部'
          }
        }],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'line'
          },
          formatter: (params: any) => {
            return `${params[0].axisValue}<br>${params[0].marker} ${params[0].seriesName}: ${params[0].value}部`
          }
        },
        legend: {
          data: [selectedDataset.label],
          bottom: 10,
          itemWidth: 12,
          itemHeight: 12,
          textStyle: {
            fontSize: 12
          }
        },
        title: {
          text: selectedCountry.value.trim() === ''
            ? `年度电影总产量（${startYear.value}-${endYear.value}）`
            : `${selectedCountry.value.trim()}电影年产量（${startYear.value}-${endYear.value}）`,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          }
        },
        grid: {
          top: '20%',
          bottom: '20%',
          left: '10%',
          right: '10%',
          containLabel: true
        }
      }

      yearChartInstance.clear()
      yearChartInstance.setOption(option, true)
    }
  } catch (error) {
    console.error('年度数据请求错误:', error)
    errorMessage.value = '获取年度数据失败，请重试'
  } finally {
    loading.yearly = false
  }
}

/* 月度产量接口 */
const fetchMonthlyProduction = async () => {
  try {
    loading.monthly = true
    errorMessage.value = ''

    const params: any = {
      year: selectedMonthYear.value,
    }

    // 只有当用户输入了国家时才添加country参数
    if (selectedMonthCountry.value.trim()) {
      params.country = selectedMonthCountry.value.trim()
    }

    const { data } = await axios.get<MonthlyProductionData>(
      'http://localhost:5000/api/basic/production/monthly',
      { params }
    )

    if (data.success && monthChartInstance) {
      const monthLabels = ['1月', '2月', '3月', '4月', '5月', '6月',
        '7月', '8月', '9月', '10月', '11月', '12月']

      // 获取要显示的数据集
      const displayDataset = data.data.datasets.find(d =>
        d.label.includes(selectedMonthYear.value.toString())
      );

      monthChartInstance.setOption({
        xAxis: {
          type: 'category',
          data: monthLabels,
          axisLabel: {
            interval: 0,
            color: '#666',
            fontSize: 12
          },
          axisLine: {
            lineStyle: {
              color: '#ddd'
            }
          },
          axisTick: {
            alignWithLabel: true
          }
        },
        yAxis: {
          type: 'value',
          name: '产量（部）',
          nameTextStyle: {
            padding: [0, 0, 0, 40]
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ddd'
            }
          },
          splitLine: {
            lineStyle: {
              type: 'dashed',
              color: '#eee'
            }
          }
        },
        series: [{
          name: displayDataset?.label || '月度产量',
          type: 'bar',
          barWidth: '60%',
          data: displayDataset?.data || Array(12).fill(0),
          itemStyle: {
            color: '#5470C6',
            borderRadius: [4, 4, 0, 0]
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}部'
          }
        }],
        title: {
          text: `${selectedMonthYear.value}年${selectedMonthCountry.value.trim() ? selectedMonthCountry.value.trim() : ''}月度产量`,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: (params: any) => {
            const [param] = params
            return `${param.axisValue}<br>${param.marker} ${param.seriesName}: ${param.value}部`
          }
        },
        grid: {
          top: '20%',
          bottom: '10%',
          left: '10%',
          right: '10%',
          containLabel: true
        }
      })
    }
  } catch (error) {
    console.error('月度数据请求错误:', error)
    errorMessage.value = '获取月度数据失败，请重试'
  } finally {
    loading.monthly = false
  }
}

/* 国家地区产量接口 */
const fetchCountryProduction = async () => {
  try {
    loading.regional = true
    errorMessage.value = ''

    const params: any = {}
    if (selectedRegionYear.value) {
      params.year = selectedRegionYear.value
    }

    const { data } = await axios.get<CountryProductionData>(
      'http://localhost:5000/api/basic/production/countries',
      { params }
    )

    if (data.success && regionChartInstance) {
      regionChartInstance.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}部 '
        },
        xAxis: {
          type: 'category',
          data: data.data.map(item => item.country),
          axisLabel: {
            interval: 0,
            rotate: 30,
            color: '#333',
            fontSize: 12
          },
          axisLine: {
            lineStyle: {
              color: '#ddd'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: '产量（部）',
          nameTextStyle: {
            padding: [0, 0, 0, 40]
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ddd'
            }
          },
          splitLine: {
            lineStyle: {
              type: 'dashed',
              color: '#eee'
            }
          }
        },
        series: [{
          name: '地区产量',
          type: 'bar',
          barWidth: '40%',
          data: data.data.map(item => ({
            value: item.count,
            name: item.country,
            percentage: item.percentage
          })),
          itemStyle: {
            color: '#5470C6'
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}',
            color: '#333'
          }
        }],
        title: {
          text: `${selectedRegionYear.value || '全部年份'}地区电影产量`,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          }
        },
        grid: {
          top: '15%',
          bottom: '15%',
          left: '10%',
          right: '10%',
          containLabel: true
        }
      })
    }
  } catch (error) {
    console.error('地区数据请求错误:', error)
    errorMessage.value = '获取地区数据失败，请重试'
  } finally {
    loading.regional = false
  }
}

// 初始化加载数据
onMounted(() => {
  initCharts()
  fetchYearlyProduction()
  fetchMonthlyProduction()
  fetchCountryProduction()
})

// 监听参数变化重新获取数据
watch([startYear, endYear, selectedCountry], fetchYearlyProduction)
watch([selectedMonthYear, selectedMonthCountry], fetchMonthlyProduction)
watch(selectedRegionYear, fetchCountryProduction)
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
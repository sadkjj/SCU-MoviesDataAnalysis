import { onMounted } from 'vue';
import * as echarts from 'echarts';
import worldMap from '@/assets/world.json';
import { mapChartRef, chartInstance, fetchData } from './RegionDimension.vue';

// 注册地图数据
onMounted(() => {
if (mapChartRef.value) {
echarts.registerMap('world', worldMap);
chartInstance = echarts.init(mapChartRef.value);
fetchData();
window.addEventListener('resize', () => chartInstance?.resize());
}
});

import { startYear, startMonth, endYear, endMonth } from './MarketTrend.vue';

// 生成模拟数据
export const generateMockData = () => {
const data: Array<{
time: string;
ticketPrice: number;
boxOffice: number;
}> = [];
const start = new Date(startYear.value, startMonth.value - 1);
const end = new Date(endYear.value, endMonth.value - 1);

let current = new Date(start);
while (current <= end) {
const year = current.getFullYear();
const month = current.getMonth() + 1;
const timeLabel = `${year}年${month}月`;

// 生成票价和票房数据
const seasonalFactor = 0.8 + 0.4 * Math.sin((month - 1) * Math.PI / 6);
const basePrice = 35 + (year - 2020) * 2;
const baseBoxOffice = 20000 + (year - 2020) * 5000;

data.push({
time: timeLabel,
ticketPrice: parseFloat((basePrice * seasonalFactor * (0.95 + Math.random() * 0.1).toFixed(1)),
boxOffice, parseInt((baseBoxOffice * seasonalFactor * (0.9 + Math.random() * 0.2)).toFixed(0))),
boxOffice: 0
});

// 移动到下个月
current.setMonth(current.getMonth() + 1);
}

return data;
};

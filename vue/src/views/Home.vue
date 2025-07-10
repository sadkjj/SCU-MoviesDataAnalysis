<template>
  <div class="home-container">
    <!-- 搜索框 -->
    <div class="search-bar">
      <input
        v-model="keyword"
        type="text"
        placeholder="搜索电影名称"
        class="search-input"
      />
      
      <div class="filter-group">
        <label class="filter-label">导演：</label>
        <input v-model="searchDirector" type="text" class="filter-input" placeholder="输入导演名称" />
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-bar">
      <div class="filter-group">
        <label class="filter-label">类型：</label>
        <select v-model="selectedGenre" class="filter-select">
          <option value="">全部类型</option>
          <option value="科幻">科幻</option>
          <option value="奇幻">奇幻</option>
          <option value="历史">历史</option>
          <option value="犯罪">犯罪</option>
          <option value="剧情">剧情</option>
          <option value="悬疑">悬疑</option>
          <option value="古装">古装</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label">最低评分：</label>
        <input v-model.number="minRating" type="number" class="filter-input" min="0" max="10" step="0.1" />
      </div>

      <div class="filter-group">
        <label class="filter-label">年份范围：</label>
        <input v-model.number="startYear" type="number" class="filter-input year-input" min="1900" max="2100" />
        <span style="margin: 0 0.3rem">~</span>
        <input v-model.number="endYear" type="number" class="filter-input year-input" min="1900" max="2100" />
      </div>


      <div class="filter-group">
        <label class="filter-label">排序方式：</label>
        <select v-model="sortField" class="filter-select">
          <option value="title">电影名称</option>
          <option value="release_date">上映日期</option>
          <option value="total_box_office">票房</option>
        </select>
        <select v-model="sortOrder" class="filter-select">
          <option value="asc">升序</option>
          <option value="desc">降序</option>
        </select>
      </div>
    </div>

    <!-- 电影列表 -->
    <div class="movie-list">
      <div v-for="movie in filteredMovies" :key="movie.movie_id" class="movie-card">
        <div class="movie-header">
          <h2 class="movie-title">{{ movie.title }}</h2>
          <div class="movie-subinfo">
            <span>上映：{{ movie.release_date }}</span>
            <span>票房：{{ formatBoxOffice(movie.total_box_office) }} 元</span>
            <span class="stars">
              <template v-for="i in 5">
                <i
                  class="star"
                  :class="{
                    filled: i <= Math.floor(movie.overall_rating / 2),
                    half: i === Math.ceil(movie.overall_rating / 2) && movie.overall_rating % 2 >= 1
                  }"
                ></i>
              </template>
              <span class="rating-number">({{ movie.overall_rating }})</span>
            </span>
          </div>
        </div>

        <div class="movie-body">
          <div class="meta-row"><span class="label">🎬 导演：</span><span class="value">{{ movie.directors.join('、') }}</span></div>
          <div class="meta-row"><span class="label">⭐ 主演：</span><span class="value">{{ movie.main_actors.join('、') }}</span></div>
          <div class="meta-row"><span class="label">📂 类型：</span><span class="value">{{ movie.genres.join('、') }}</span></div>
          <div class="meta-row">
            <span class="label">📖 简介：</span>
            <span class="value">
              <div :class="['movie-summary', expandedSummaries[movie.movie_id] ? 'expanded' : 'collapsed']">
                {{ movie.description || '暂无简介。' }}
              </div>
              <button
                v-if="movie.description && movie.description.length > 60"
                class="toggle-btn"
                @click="toggleSummary(movie.movie_id)"
              >
                {{ expandedSummaries[movie.movie_id] ? '收起' : '展开' }}
              </button>
            </span>
          </div>
          <div v-if="isAdmin" class="admin-controls">
            <button class="delete-btn" @click="handleDelete(movie.movie_id)">🗑 删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="currentPage--">&lt; 上一页</button>
      <span>当前页：{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">下一页 &gt;</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { currentUser } from '@/stores/user'
import { API_BASE_URL } from '@/api'

const years = Array.from({ length: 30 }, (_, i) => 1995 + i)
const keyword = ref('')
const selectedGenre = ref('')
const minRating = ref(0)
const startYear = ref(2000)
const endYear = ref(new Date().getFullYear())
const currentPage = ref(1)
const pageSize = 5
const sortField = ref('release_date')
const sortOrder = ref('desc')

const searchDirector = ref('') // 确保这个变量已经定义

const isAdmin = computed(() => currentUser.value?.role_type === 1)

const movieList = ref<Movie[]>([])
const totalMovies = ref(0)

const fetchMovies = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize,
      title: keyword.value,
      genre: selectedGenre.value,
      min_rating: minRating.value,
      start_year: startYear.value,
      end_year: endYear.value,
      sort_field: sortField.value,
      sort_order: sortOrder.value,
      director: searchDirector.value // 添加 director 参数
    }
    const response = await axios.get(`${API_BASE_URL}/api/user/movies`, { params })

    if (response.data.success) {
      const { total, items } = response.data.data
      movieList.value = items
      totalMovies.value = total
    } else {
      console.error('获取失败：', response.data.message)
    }
  } catch (error) {
    console.error('请求出错：', error)
  }
}

const fetchUserAuth = async () => {
  try {
    const userId = currentUser.value?.user_id
    if (!userId) return

    const response = await axios.get(`${API_BASE_URL}/api/user/auth/${userId}`)
    if (response.data.success) {
      const { user_id, role_type } = response.data.data
      currentUser.value = { user_id, role_type }
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
    } else {
      console.error('获取用户权限失败：', response.data.message)
    }
  } catch (error) {
    console.error('请求用户权限出错：', error)
  }
}

const expandedSummaries = ref<Record<number, boolean>>({})
const toggleSummary = (id: number) => {
  expandedSummaries.value[id] = !expandedSummaries.value[id]
}

const formatBoxOffice = (value: number): string => {
  if (!value || isNaN(value)) return '0.0'
  return value.toFixed(1)
}

const handleDelete = async (movieId: number) => {
  if (!confirm('确认删除这部电影吗？')) return
  try {
    const res = await axios.delete(`http://localhost:5000/api/admin/movie/${movieId}`)
    if (res.data.success) {
      fetchMovies()
    } else {
      alert('删除失败：' + res.data.message)
    }
  } catch (err) {
    console.error(err)
    alert('请求失败，请稍后重试')
  }
}

const totalPages = computed(() => Math.ceil(totalMovies.value / pageSize))
const filteredMovies = computed(() => movieList.value)

onMounted(() => {
  fetchMovies()
  fetchUserAuth()
  window.addEventListener('resize', () => {
    // 可以在这里添加图表的resize逻辑
  })
})

watch([keyword, selectedGenre, minRating, startYear, endYear, currentPage, sortField, sortOrder, searchDirector], fetchMovies) // 添加 searchDirector 到监听列表
</script>

<style scoped>
.admin-controls {
  text-align: right;
  margin-top: 1rem;
}
.delete-btn {
  background-color: #ef4444;
  color: white;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.delete-btn:hover {
  background-color: #dc2626;
}

/* 动画定义 */
@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 主体布局 */
.home-container {
  padding: 2rem;
  background-color: #f3f4f68f;
  min-height: 100vh;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: fadeUp 0.6s ease both;
}

/* 搜索框 */
.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

/* 统一所有搜索框样式 */
.search-input, .filter-select, .filter-input {
  width: 60%;
  padding: 0.8rem 1.2rem;
  font-size: 1rem;
  border: none;
  border-radius: 0.8rem;
  background: linear-gradient(
    to right,
    rgba(235, 245, 255, 0.9),
    rgba(220, 238, 255, 0.9)
  );
  box-shadow: 
    inset 0 1px 3px rgba(255, 255, 255, 0.8),
    0 2px 8px rgba(100, 150, 255, 0.15);
  color: #2c5282;
  transition: all 0.3s ease;
}

.search-input::placeholder,
.filter-select::placeholder,
.filter-input::placeholder {
  color: #90cdf4;
  opacity: 0.8;
}

.search-input:focus,
.filter-select:focus,
.filter-input:focus {
  outline: none;
  background: linear-gradient(
    to right,
    rgba(220, 238, 255, 0.95),
    rgba(200, 230, 255, 0.95)
  );
  box-shadow: 
    inset 0 1px 3px rgba(255, 255, 255, 0.9),
    0 0 0 3px rgba(144, 205, 244, 0.4),
    0 4px 12px rgba(100, 150, 255, 0.2);
  border: 1px solid #90cdf4;
}

.search-input:hover,
.filter-select:hover,
.filter-input:hover {
  transform: translateY(-1px);
  box-shadow: 
    inset 0 1px 3px rgba(255, 255, 255, 0.9),
    0 4px 12px rgba(100, 150, 255, 0.25);
}

/* 调整特定输入框宽度 */
.filter-select,
.filter-input {
  min-width: 140px;
  width: auto;
}

.year-input {
  width: 80px;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.filter-label {
  font-weight: 500;
  color: #444;
  min-width: 70px;
  text-align: right;
}

/* 卡片列表 */
.movie-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* 修改卡片样式 - 浅蓝色背景，无悬停效果 */
.movie-card {
  background-color: #e6f0ff; /* 浅蓝色背景 */
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: none; /* 移除所有过渡效果 */
  animation: fadeUp 0.5s ease both;
}

/* 移除卡片悬停效果 */
.movie-card:hover {
  transform: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background-color: #e6f0ff; /* 保持与正常状态相同的背景色 */
}

/* 卡片内容 */
.movie-header {
  margin-bottom: 1rem;
}

.movie-title {
  font-size: 1.6rem;
  font-weight: bold;
  color: #2c3e50;
}

.movie-subinfo {
  font-size: 0.95rem;
  color: #666;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.3rem;
}

.movie-body {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  font-size: 0.95rem;
  color: #444;
  line-height: 1.6;
}

.meta-row .label {
  font-weight: 600;
  min-width: 60px;
  color: #333;
}

.meta-row .value {
  flex: 1;
}

/* 星级评分 */
.stars {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 1rem;
  color: #fbbf24;
}

.star {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  background-color: #e5e7eb;
  mask: url('data:image/svg+xml;utf8,<svg fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.97a1 1 0 00.95.69h4.175c.969 0 1.371 1.24.588 1.81l-3.38 2.455a1 1 0 00-.364 1.118l1.286 3.97c.3.921-.755 1.688-1.538 1.118l-3.38-2.455a1 1 0 00-1.175 0l-3.38 2.455c-.783.57-1.838-.197-1.538-1.118l1.286-3.97a1 1 0 00-.364-1.118L2.05 9.397c-.783-.57-.38-1.81.588-1.81h4.175a1 1 0 00.95-.69l1.286-3.97z"/></svg>') center/contain no-repeat;
}

.star.filled {
  background-color: #fbbf24;
}

.star.half {
  background: linear-gradient(to right, #fbbf24 50%, #e5e7eb 50%);
}

.rating-number {
  font-size: 0.85rem;
  color: #666;
  margin-left: 4px;
}

/* 简介动画 */
.movie-summary {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #444;
  transition: all 0.4s ease;
  overflow: hidden;
}

.movie-summary.collapsed {
  max-height: 3.2em;
  -webkit-line-clamp: 2;
  display: -webkit-box;
  -webkit-box-orient: vertical;
}

.movie-summary.expanded {
  max-height: 1000px;
  transition: max-height 0.6s ease-in;
}

.toggle-btn {
  margin-top: 4px;
  background: none;
  border: none;
  color: #409eff;
  font-size: 0.85rem;
  cursor: pointer;
  padding: 0;
}

/* 分页按钮动画 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination button {
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.pagination button:active {
  transform: scale(0.95);
}

.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.pagination span {
  font-size: 0.9rem;
  color: #444;
}
</style>
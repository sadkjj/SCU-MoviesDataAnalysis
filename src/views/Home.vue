<template>
    <div class="home-container">
      <!-- 搜索框 -->
      <div class="search-bar">
        <input
          v-model="keyword"
          type="text"
          placeholder="搜索电影名称、导演、演员..."
          class="search-input"
        />
      </div>
  
      <!-- 筛选区域 -->
      <!-- 筛选区域（带文字标签） -->
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
    <input
      v-model.number="minRating"
      type="number"
      class="filter-input"
      min="0"
      max="10"
      step="0.1"
    />
  </div>

  <div class="filter-group">
    <label class="filter-label">年份范围：</label>
    <input
      v-model.number="startYear"
      type="number"
      class="filter-input year-input"
      min="1900"
      max="2100"
    />
    <span style="margin: 0 0.3rem">~</span>
    <input
      v-model.number="endYear"
      type="number"
      class="filter-input year-input"
      min="1900"
      max="2100"
    />
  </div>
</div>

      <!-- 电影列表 -->
      <div class="movie-list">
        <div v-for="movie in filteredMovies" :key="movie.title" class="movie-card">
          <div class="movie-meta">
            <h2 class="movie-title">{{ movie.title }}</h2>
            <span>导演：{{ movie.director }}</span>
            <span>主演：{{ movie.actors.join('、') }}</span>
            <span>类型：{{ movie.genre }}</span>
            <span>年份：{{ movie.releaseYear }}</span>
            <span>评分：{{ movie.rating }}</span>
          </div>
          <p class="movie-description">简介：{{ movie.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from 'vue'
  
  const keyword = ref('')
  const selectedGenre = ref('')
  const minRating = ref(0)
  const startYear = ref(2000)
  const endYear = ref(new Date().getFullYear())
  
  const movieList = ref([
    {
      title: '流浪地球 2',
      director: '郭帆',
      actors: ['吴京', '刘德华', '李雪健'],
      genre: '科幻',
      releaseYear: 2023,
      rating: 8.4,
      description: '人类面对太阳危机，启动“移山计划”与“月球引爆”，展现家园守护的壮丽史诗。',
    },
    {
      title: '封神第一部',
      director: '乌尔善',
      actors: ['费翔', '李雪健', '黄渤'],
      genre: '奇幻/历史',
      releaseYear: 2023,
      rating: 8.0,
      description: '改编自《封神演义》，讲述姜子牙伐纣助周，众神归位的宏大神话史诗。',
    },
    {
      title: '孤注一掷',
      director: '申奥',
      actors: ['张艺兴', '金晨'],
      genre: '犯罪/剧情',
      releaseYear: 2023,
      rating: 7.2,
      description: '揭示诈骗黑产全链条，以真实案例为蓝本，展现跨国犯罪惊险全过程。',
    },
    {
      title: '满江红',
      director: '张艺谋',
      actors: ['沈腾', '易烊千玺'],
      genre: '悬疑/古装',
      releaseYear: 2023,
      rating: 7.8,
      description: '南宋时期，秦桧议和案中疑云重重，展现爱国情怀与智勇交锋。',
    },
  ])
  
  const filteredMovies = computed(() =>
    movieList.value.filter((movie) => {
      const matchesKeyword = [movie.title, movie.director, ...movie.actors]
        .join(',')
        .toLowerCase()
        .includes(keyword.value.toLowerCase())
      
      const matchesGenre =
      !selectedGenre.value || movie.genre.split('/').includes(selectedGenre.value)

      const matchesRating = movie.rating >= minRating.value
      const matchesYear =
      movie.releaseYear >= startYear.value &&
      movie.releaseYear <= endYear.value

      return matchesKeyword && matchesGenre && matchesRating && matchesYear
  })
)
  </script>
  
  <style scoped>
  .home-container {
    padding: 2rem;
    background-color: #e6e6e61b;
    min-height: 100vh;
    border-radius: 10px;
  }
  
  /* 搜索框样式 */
  .search-bar {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
  }
  
  .search-input {
    width: 60%;
    padding: 0.8rem 1.2rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 999px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 5px rgba(59, 130, 246, 0.2);
  }
  
  /* 筛选栏样式 */
  .filter-bar {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .filter-select,
  .filter-input {
    padding: 0.6rem 1rem;
    font-size: 0.95rem;
    border-radius: 0.5rem;
    border: 1px solid #ccc;
    min-width: 140px;
    transition: border 0.2s ease;
  }
  
  .filter-select:focus,
  .filter-input:focus {
    outline: none;
    border-color: #3b82f6;
  }
  .filter-bar {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: nowrap;
}

.filter-label {
  font-weight: 500;
  color: #444;
  min-width: 70px;
  text-align: right;
}

.year-input {
  width: 80px;
}

  /* 电影卡片区域 */
  .movie-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .movie-card {
    background-color: #ffffff9b;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.265);
    transition: transform 0.2s ease;

  }
  
  .movie-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 0 5px rgba(109, 109, 109, 0.274);
    background-color: #ffffff47;


  }
  
  .movie-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 1rem;
  }
  
  .movie-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #333;
  }
  
  .movie-description {
    color: #555;
    line-height: 1.6;
  }
  </style>
  
<template>
    <nav class="navbar">
      <h2 class="title">🎬 电影分析平台</h2>
      <ul class="nav-list">
        <li v-for="item in navItems" :key="item.path">
          <RouterLink
            :to="item.path"
            class="nav-link"
            :class="{ active: isActive(item.path) }"
          >
            {{ item.label }}
          </RouterLink>
        </li>
      </ul>

      <!-- 用户区域 -->
    <div class="user-nav">
        <RouterLink v-if="!currentUser" to="/login" class="nav-link">
            登录 / 注册
        </RouterLink>

        <div v-else class="user-info">
            <RouterLink to="/user" class="user-link">
                    👤   {{ currentUser.username }}
            </RouterLink>
            <button class="logout-button" @click="logout">退出</button>
        </div>
    </div>

    </nav>
  </template>
  
  <script setup lang="ts">
  import { useRoute } from 'vue-router'
  import { currentUser } from '@/stores/user'
  import { useRouter } from 'vue-router'

  const route = useRoute()
  const router=useRouter()

  const navItems = [
    { path: '/', label: '首页' },
    { path: '/basic', label: '基础数据分析' },
    { path: '/content', label: '内容特征分析' },
    { path: '/team', label: '创作团队分析' },
    { path: '/space-time', label: '时空维度分析' },
    { path: '/market', label: '观众与市场分析' },
  ]
  const logout = () => {
  currentUser.value = null
  localStorage.removeItem('currentUser')
  router.push('/login')
}
  function isActive(path: string): boolean {
    return route.path === path
  }
  </script>
  
  <style scoped>
  .navbar {
    height: 100%;
    width: 100%;
    background-color: #1e1e2f;
    color: #ffffff;
    padding: 2rem 1.5rem;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
  }
  
  .title {
    font-size: 1.6rem;
    font-weight: 600;
    margin-bottom: 2rem;
    letter-spacing: 0.5px;
    text-align: center;
  }
  
  .nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
  }
  
  .nav-link {
    display: block;
    padding: 0.75rem 1rem;
    margin-bottom: 1.3rem;
    border-radius: 0.5rem;
    color: #ccc;
    text-decoration: none;
    font-size: 1rem;
    transition: all 0.2s ease;
  }
  
  .nav-link:hover {
    background-color: #2a2a40;
    color: #ffffff;
  }
  
  .nav-link.active {
    background-color: #2d2d44;
    color: #00e5ff;
    border-left: 4px solid #3b82f6;
    padding-left: calc(1rem - 4px); /* 左边条占位补偿 */
    font-size: 1.2rem;
  }

  .user-nav {
  margin-top: auto;
  padding: 1rem;
  font-size: 0.95rem;
}
.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.logout-button {
  background: transparent;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 0.85rem;
  padding: 0rem;
  margin-left: auto;
  margin-bottom: 2rem;
}
.logout-button:hover {
  color: #f87171;
}
.user-link {
  color: #00e5ff;
  font-weight: 500;
  text-decoration: none;
  font-size: 1rem;
  padding: 0.3rem 0;
  transition: color 0.2s;
}
.user-link:hover {
  color: #3b82f6;
}

  </style>
  
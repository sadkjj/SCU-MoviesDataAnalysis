<template>
  <div class="auth-container">
    <h2>{{ isAdmin ? '管理员登录' : '用户登录' }}</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="text" placeholder="用户名" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit">登录</button>
    </form>

    <div class="switch">
      <p v-if="!isAdmin">
        没有账号？<router-link to="/register">注册</router-link>
      </p>
      <p>
        <button class="switch-btn" @click="toggleMode">
          👉 切换为{{ isAdmin ? '用户' : '管理员' }}登录
        </button>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { currentUser } from '@/stores/user'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

const username = ref('')
const password = ref('')
const isAdmin = ref(false)
const router = useRouter()

// 切换用户 / 管理员登录模式
const toggleMode = () => {
  isAdmin.value = !isAdmin.value
}

const handleLogin = async () => {
  try {
    const endpoint = isAdmin.value
      ? `${API_BASE_URL}/api/admin/login`
      : `${API_BASE_URL}/api/user/login`

    const response = await axios.post(endpoint, {
      username: username.value,
      password: password.value
    })

    if (response.data.success) {
      currentUser.value = {
        user_id: response.data.user_id,
        role_type:response.data.role_type
      }
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
      router.push(isAdmin.value ? '/admin' : '/user') 
    } else {
      alert(response.data.message || '登录失败，请重试')
    }
  } catch (err) {
    console.error('登录请求出错:', err)
    alert('账号未注册或用户名密码不正确')
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 8rem auto;
  background: #ffffff;
  padding: 2.5rem;
  border-radius: 1.25rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  text-align: center;
}

input {
  display: block;
  width: 100%;
  margin-bottom: 1.5rem;
  padding: 0.875rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #3b82f6;
  outline: none;
}

button {
  width: 100%;
  padding: 0.875rem;
  background: #3b82f6;
  color: #ffffff;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background: #2c5282;
}

.switch {
  margin-top: 1.5rem;
  font-size: 0.9375rem;
}

.switch-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  background-color: #facc15;
  color: #333;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.switch-btn:hover {
  background-color: #fbbf24;
}

.switch a {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.3s;
}

.switch a:hover {
  color: #2c5282;
}
</style>

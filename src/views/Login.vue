<template>
    <div class="auth-container">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <input v-model="username" type="text" placeholder="用户名" required />
        <input v-model="password" type="password" placeholder="密码" required />
        <button type="submit">登录</button>
        <p class="switch">
          没有账号？<router-link to="/register">注册</router-link>
        </p>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { currentUser } from '@/stores/user'
  import axios from 'axios'
  
  const username = ref('')
  const password = ref('')
  const router = useRouter()
  
  const handleLogin = async () => {
    try {
      // 使用 axios 发送 POST 请求到后端登录接口
      const response = await axios.post('/api/login', {
        user_id: username.value,  // 修改请求参数为 user_id
        password: password.value
      })
      
      // 假设后端返回用户信息，你可以将其存储在 currentUser 中
      currentUser.value = response.data.user
      
      // 将用户信息存储到 localStorage 中
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
      
      // 登录成功后跳转到用户页面
      router.push('/user')
    } catch (error) {
      // 处理登录失败的情况
      console.error('登录失败:', error)
      alert('用户名或密码错误，请重试。')
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

.switch a {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.3s;
}

.switch a:hover {
  color: #2c5282;
}
</style>

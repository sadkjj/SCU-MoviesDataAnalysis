<template>
  <div class="auth-container">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" type="text" placeholder="用户名" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit">注册</button>
      <p class="switch">
        已有账号？<router-link to="/login">登录</router-link>
      </p>
    </form>
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
const router = useRouter()

const handleRegister = async () => {
  try {
    // 使用 axios 发送 POST 请求到后端注册接口
    const response = await axios.post(
      `${API_BASE_URL}/api/user/register`, 
      {
        username: username.value,
        password: password.value
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )

    // 检查后端返回的 success 字段
    if (response.data.success) {
      // 注册成功后，保存用户信息并跳转
      currentUser.value = {
        user_id: response.data.user_id      };
      console.log(response);
      
      // 将用户信息存储到 localStorage 中
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
        alert('注册成功！')
      // 注册成功后跳转到用户页面
      router.push('/Login')
    } else {
      // 注册失败，显示错误信息
      alert(response.data.message)
    }
  } catch (error) {
    console.error('注册失败:', error)
    
    // 根据错误类型显示不同提示
    if (axios.isAxiosError(error) && error.response) {
      // 如果是axios错误且有响应
      alert(error.response.data.message || '注册失败，请重试')
    } else {
      alert('网络错误或服务器不可用')
    }
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
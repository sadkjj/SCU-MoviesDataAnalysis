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
  
  const username = ref('')
  const password = ref('')
  const router = useRouter()
  
  const handleRegister = () => {
    currentUser.value = { username: username.value }
    localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
    router.push('/user')
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
  
  
<<<<<<< HEAD
<template>
    <div>
      <h1>用户管理页面</h1>
    </div>
  </template>
  
  <script setup lang="ts">
  // 这里先留空，后续可加逻辑
  </script>
  
  <style scoped>
  
  </style>
  
=======
<template>
  <div class="user-admin">
    <h2>👤 用户信息</h2>

    <div class="user-card" v-if="userData">
      <div class="user-item"><strong>用户名：</strong>{{ userData.username }}</div>
      <div class="user-item"><strong>真实姓名：</strong>{{ userData.real_name }}</div>
      <div class="user-item"><strong>手机号：</strong>{{ userData.phone }}</div>
      <div class="user-item"><strong>邮箱：</strong>{{ userData.email }}</div>
      <button class="edit-btn" @click="openEditDialog">✏️ 修改信息</button>
    </div>

    <div v-else class="loading">正在加载用户信息...</div>

    <!-- 修改信息对话框 -->
    <div class="dialog-overlay" v-if="showDialog">
      <div class="dialog">
        <h3>修改个人信息</h3>
        <form @submit.prevent="submitEdit">
          <label>用户名 <input v-model="editForm.username" /></label>
          <label>真实姓名 <input v-model="editForm.real_name" /></label>
          <label>手机号 <input v-model="editForm.phone" /></label>
          <label>邮箱 <input v-model="editForm.email" /></label>
          <div class="dialog-buttons">
            <button type="submit">保存</button>
            <button type="button" @click="closeEditDialog">取消</button>
          </div>
        </form>
        <p v-if="updateMessage" class="update-msg">{{ updateMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, reactive, onMounted } from 'vue'
  import axios from 'axios';
  import { currentUser } from '@/stores/user'


  interface User {
    user_id: number
    username: string
    real_name: string
    phone: string
    email: string
    role_type: number
    create_time: string
  }

  const userData = ref<User | null>(null)
  const showDialog = ref(false)
  const updateMessage = ref('')
  const editForm = reactive({
    username: '',
    real_name: '',
    phone: '',
    email: ''
  })

  
  const fetchUserData = async () => {
  const userId = currentUser.value;
  console.log(userId);
  
  if (!userId) {
    console.error('user_id not found in localStorage');
    return;
  }

  try {
    // 使用 axios 发送 GET 请求到后端获取用户信息接口
    const response = await axios.get(`http://127.0.0.1:4523/m1/6680275-6389502-default/api/user/${userId}`);
    

    console.log(response);
    
    if (response.data.success) {
      userData.value = response.data.data;
    } else {
      console.error('Failed to fetch user data:', response.data.message);
    }
  } catch (error) {
    console.error('Failed to fetch user data:', error);
  }
};

onMounted(() => {
  fetchUserData();
});
  const openEditDialog = () => {
    if (!userData.value) return
    Object.assign(editForm, {
      username: userData.value.username,
      real_name: userData.value.real_name,
      phone: userData.value.phone,
      email: userData.value.email
    })
    updateMessage.value = ''
    showDialog.value = true
  }

  const closeEditDialog = () => {
    showDialog.value = false
  }

  const submitEdit = async () => {
    const requestPayload = {
      username: editForm.username,
      real_name: editForm.real_name,
      phone: editForm.phone,
      email: editForm.email
    }

    // 模拟请求
    const response = {
      success: true,
      message: '信息更新成功'
    }

    if (response.success) {
      if (userData.value) {
        Object.assign(userData.value, requestPayload)
      }
      updateMessage.value = response.message
      setTimeout(() => {
        showDialog.value = false
      }, 1000)
    }
  }

  const roleLabel = (roleType: number) => {
    switch (roleType) {
      case 1: return '管理员'
      case 2: return '普通用户'
      case 3: return '游客'
      default: return '未知'
    }
  }
</script>

<style scoped>
  .user-admin {
    padding: 2rem;
  }
  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .user-card {
    background-color: #f9fafb;
    padding: 1.5rem 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    max-width: 500px;
  }
  .user-item {
    margin: 0.6rem 0;
    font-size: 1rem;
    color: #333;
  }
  .edit-btn {
    margin-top: 1.2rem;
    padding: 0.6rem 1.2rem;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.6rem;
    cursor: pointer;
  }
  .edit-btn:hover {
    background-color: #2563eb;
  }
  .loading {
    font-size: 1rem;
    color: #888;
  }
  .dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .dialog {
    background-color: white;
    padding: 2rem;
    border-radius: 1rem;
    width: 350px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  }
  .dialog h3 {
    margin-bottom: 1rem;
  }
  .dialog label {
    display: block;
    margin-bottom: 1rem;
    font-size: 0.95rem;
  }
  .dialog input {
    width: 100%;
    padding: 0.5rem;
    margin-top: 0.3rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
  }
  .dialog-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1rem;
  }
  .dialog-buttons button {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
  }
  .dialog-buttons button[type="submit"] {
    background-color: #10b981;
    color: white;
  }
  .dialog-buttons button[type="button"] {
    background-color: #e5e7eb;
  }
  .update-msg {
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #10b981;
  }
</style>
>>>>>>> 2169fedfedc3d443e3192294224aa2ddb9a5d482

<template> 
  <div class="user-admin">
    <h2>👤 用户信息</h2>

    <div class="user-card" v-if="userData">
      <!-- 👤 用户头像 -->
      <img :src="avatarUrl" class="avatar" alt="用户头像" />

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
          <label>
            用户名
            <input v-model="editForm.username" />
          </label>
          <label>
            真实姓名
            <input v-model="editForm.real_name" />
          </label>
          <label>
            手机号
            <input v-model="editForm.phone" />
          </label>
          <label>
            邮箱
            <input v-model="editForm.email" />
          </label>
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
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'
import { currentUser } from '@/stores/user'
import { API_BASE_URL } from '@/api'
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
  const userId = currentUser.value?.user_id
  console.log(userId)

  if (!userId) {
    console.error('user_id not found in localStorage')
    return
  }

  try {
    const response = await axios.get(`${API_BASE_URL}/api/user/${userId}`)
    console.log(response)

    if (response.data.success) {
      userData.value = response.data.data
    } else {
      console.error('Failed to fetch user data:', response.data.message)
    }
  } catch (error) {
    console.error('Failed to fetch user data:', error)
  }
}

onMounted(() => {
  fetchUserData()
})

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

  try {
    const response = await axios.put(
      `${API_BASE_URL}/api/user/${userData.value?.user_id}`,
      requestPayload
    )
    console.log(response)

    if (response.data.success) {
      if (userData.value) {
        Object.assign(userData.value, requestPayload)
      }
      updateMessage.value = response.data.message
      setTimeout(() => {
        showDialog.value = false
      }, 1000)
    } else {
      updateMessage.value = response.data.message || '信息更新失败'
    }
  } catch (error) {
    console.error('Failed to update user data:', error)
    updateMessage.value = '网络错误或更新异常，请稍后再试'
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

const avatarUrl = computed(() => {
  const name = userData.value?.username || 'guest'
  return `https://api.dicebear.com/7.x/thumbs/svg?seed=${encodeURIComponent(name)}`
})
</script>

<style scoped>
.user-admin {
  padding: 4rem 2rem;
  background-color: #f3f4f6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h2 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-card {
  background-color: #ffffff;
  padding: 2.5rem 3rem;
  border-radius: 1.25rem;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 700px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem 2rem;
  font-size: 1.1rem;
  position: relative;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #3b82f6;
  margin: 0 auto 1rem auto;
  grid-column: span 2;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-item {
  color: #374151;
  line-height: 1.6;
}

.edit-btn {
  grid-column: span 2;
  justify-self: center;
  padding: 0.75rem 2rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-btn:hover {
  background-color: #2563eb;
}

.loading {
  font-size: 1.2rem;
  color: #6b7280;
  margin-top: 2rem;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.dialog {
  background-color: #ffffff;
  padding: 2.5rem 3rem;
  border-radius: 1rem;
  width: 420px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.dialog h3 {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.dialog label {
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
  color: #374151;
}

.dialog input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  margin-top: 0.4rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.dialog input:focus {
  border-color: #3b82f6;
  outline: none;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.dialog-buttons button {
  padding: 0.6rem 1.4rem;
  font-size: 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}

.dialog-buttons button[type="submit"] {
  background-color: #10b981;
  color: white;
}

.dialog-buttons button[type="button"] {
  background-color: #f3f4f6;
  color: #6b7280;
}

.dialog-buttons button:hover {
  opacity: 0.9;
}

.update-msg {
  text-align: center;
  color: #10b981;
  font-weight: 500;
  margin-top: 1rem;
}
</style>

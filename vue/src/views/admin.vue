<template>
  <div class="admin-user-container">
    <h2>👥 用户管理</h2>

    <!-- 操作工具栏 -->
    <div class="admin-toolbar">
      <button class="create-button" @click="openCreateDialog">+ 创建用户</button>
      
      <!-- 筛选与排序 -->
      <div class="admin-filters">
        <input v-model="search" placeholder="搜索用户名/真实姓名/邮箱..." />
        <select v-model="sortField">
          <option value="create_time">注册时间</option>
          <option value="update_time">更新时间</option>
          <option value="username">用户名</option>
        </select>
        <select v-model="sortOrder">
          <option value="asc">升序</option>
          <option value="desc">降序</option>
        </select>
      </div>
    </div>

    <!-- 用户表格 -->
    <table class="user-table">
      <thead>
        <tr>
          <th>用户名</th>
          <th>真实姓名</th>
          <th>手机号</th>
          <th>邮箱</th>
          <th>身份</th>
          <th>注册时间</th>
          <th>更新时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in userList" :key="user.user_id">
          <td>{{ user.username }}</td>
          <td>{{ user.real_name }}</td>
          <td>{{ user.phone }}</td>
          <td>{{ user.email }}</td>
          <td>{{ roleLabel(user.role_type) }}</td>
          <td>{{ formatDate(user.create_time) }}</td>
          <td>{{ formatDate(user.update_time) }}</td>
          <td>
            <button @click="openEditDialog(user)">编辑</button>
            <button class="danger" @click="deleteUser(user.user_id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分页 -->
    <div class="pagination">
      <button :disabled="page === 1" @click="page--">上一页</button>
      <span>第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
      <button :disabled="page === totalPages" @click="page++">下一页</button>
    </div>

    <!-- 创建用户弹窗 -->
    <div class="dialog-overlay" v-if="showCreateDialog">
      <div class="dialog">
        <h3>创建新用户</h3>
        <form @submit.prevent="submitCreate">
          <label>用户名<input v-model="createForm.username" required /></label>
          <label>密码<input v-model="createForm.password" type="password" required /></label>
          <label>真实姓名<input v-model="createForm.real_name" /></label>
          <label>手机号<input v-model="createForm.phone" /></label>
          <label>邮箱<input v-model="createForm.email" type="email" /></label>
          <label>身份
            <select v-model="createForm.role_type">
              <option :value="1">管理员</option>
              <option :value="2">普通用户</option>
            </select>
          </label>
          <div class="dialog-buttons">
            <button type="submit">创建</button>
            <button type="button" @click="closeCreateDialog">取消</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 编辑用户弹窗 -->
    <div class="dialog-overlay" v-if="showEditDialog">
      <div class="dialog">
        <h3>编辑用户信息</h3>
        <form @submit.prevent="submitEdit">
          <label>用户名<input v-model="editForm.username" required /></label>
          <label>真实姓名<input v-model="editForm.real_name" /></label>
          <label>手机号<input v-model="editForm.phone" /></label>
          <label>邮箱<input v-model="editForm.email" type="email" /></label>
          <label>身份
            <select v-model="editForm.role_type">
              <option :value=1>管理员</option>
              <option :value=2>普通用户</option>
            </select>
          </label>
          <div class="dialog-buttons">
            <button type="submit">保存</button>
            <button type="button" @click="closeEditDialog">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, reactive, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api'

const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const sortField = ref('create_time')
const sortOrder = ref('desc')
const search = ref('')
const userList = ref([])

// 获取用户列表
const fetchUsers = async () => {
  const params = {
    page: page.value,
    page_size: pageSize.value,
    sort_field: sortField.value,
    sort_order: sortOrder.value,
    search: search.value
  }
  try {
    const res = await axios.get(`http://localhost:5000/api/admin/users`, { params })
    if (res.data.success) {
      userList.value = res.data.data.items
      total.value = res.data.data.total
      console.log(res);
      
    }
  } catch (err) {
    console.error('获取用户失败：', err)
    //console.log(res);
  }
}

watch([page, sortField, sortOrder, search], fetchUsers, { immediate: true })

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const roleLabel = (role) => {
  return role === 1 ? '管理员' : '普通用户'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

// 创建用户逻辑
const showCreateDialog = ref(false)
const createForm = reactive({
  username: '',
  password: '',
  real_name: null,
  phone: null,
  email: null,
  role_type: 2
})

const openCreateDialog = () => {
  showCreateDialog.value = true
}

const closeCreateDialog = () => {
  showCreateDialog.value = false
  Object.assign(createForm, {
    username: '',
    password: '',
    real_name: null,
    phone: null,
    email: null,
    role_type: 2
  })
}

const submitCreate = async () => {
  try {
    const res = await axios.post(
      `${API_BASE_URL}/api/admin/user`,
      createForm
    )
    
    if (res.data.success) {
      alert(`用户 ${res.data.data.username} 创建成功！`)
      fetchUsers()
      closeCreateDialog()
    }
  } catch (error) {
    console.error('创建用户失败：', err)
    alert('创建用户失败：' + (err.response?.data?.message || err.message))
  }
}

// 编辑用户逻辑
const showEditDialog = ref(false)
const editForm = reactive({ 
  user_id: null, 
  username: '', 
  real_name: null, 
  phone: null, 
  email: null, 
  role_type: 2 
})

// const openEditDialog = (user) => {
//   Object.assign(editForm, user)
//   showEditDialog.value = true
// }


const openEditDialog = (user) => {
  editForm.user_id = user.user_id
  editForm.username = user.username
  editForm.real_name = user.real_name
  editForm.phone = user.phone
  editForm.email = user.email
  editForm.role_type = user.role_type
  showEditDialog.value = true
}

const closeEditDialog = () => {
  showEditDialog.value = false
}

const submitEdit = async () => {
  try {
    console.log(editForm);
    const res = await axios.put(
      `${API_BASE_URL}/api/admin/user/${editForm.user_id}`,
      editForm
    )
    if (res.data.success) {
      console.log(res);
      fetchUsers()
      closeEditDialog()
    }
  } catch (err) {
    console.error('更新失败：', err)
  }
}

// 删除用户
const deleteUser = async (id) => {
  if (!confirm('确定要删除该用户吗？')) return
  try {
    const res = await axios.delete(
      `http://localhost:5000/api/admin/user/${id}`
    )
    if (res.data.success) {
      fetchUsers()
    }
  } catch (err) {
    console.error('删除失败：', err)
  }
}
</script>

<style scoped>
.admin-user-container {
  padding: 2rem;
  background: #f9fafb;
  min-height: 100vh;
}

.admin-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.create-button {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.create-button:hover {
  background-color: #2563eb;
}

.admin-filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.admin-filters input,
.admin-filters select {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-radius: 1rem;
  overflow: hidden;
}

.user-table th,
.user-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #f3f4f6;
}

.user-table th {
  background-color: #f1f5f9;
  font-weight: 600;
}

.user-table button {
  padding: 0.3rem 0.75rem;
  margin-right: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.user-table button.danger {
  background-color: #ef4444;
  color: white;
}

.pagination {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: 400px;
  max-width: 90vw;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.1);
}

.dialog h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.dialog label {
  display: block;
  margin-bottom: 1rem;
  color: #374151;
}

.dialog input,
.dialog select {
  width: 100%;
  margin-top: 0.3rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.dialog-buttons button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.dialog-buttons button[type="submit"] {
  background-color: #22c55e;
  color: white;
}

.dialog-buttons button[type="button"] {
  background-color: #e5e7eb;
  color: #6b7280;
}
</style>
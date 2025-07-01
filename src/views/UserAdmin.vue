<template>
    <div class="user-admin">
      <h2>用户管理</h2>
  
      <!-- 普通用户 -->
      <UserProfile v-if="currentUser?.role_type !== 1" :user="currentUser" />
  
      <!-- 管理员视图 -->
      <div v-else>
        <table class="user-table">
          <thead>
            <tr>
              <th>用户名</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>手机号</th>
              <th>角色</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in userList" :key="user.user_id">
              <td>{{ user.username }}</td>
              <td>{{ user.real_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.phone }}</td>
              <td>{{ roleLabel(user.role_type) }}</td>
              <td>{{ user.create_time }}</td>
              <td><button @click="openEdit(user)">修改</button></td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- 修改弹窗 -->
      <UserEditDialog
        v-if="showDialog"
        :user="selectedUser"
        @close="showDialog = false"
        @update="handleUpdate"
      />
    </div>
  </template>
  
<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import UserProfile from '@/components/admin/UserProfile.vue'
  import UserEditDialog from '@/components/admin/UserEditDialog.vue'
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
  
  const userList = ref<User[]>([])
  const showDialog = ref(false)
  const selectedUser = ref<User | null>(null)
  
  // 模拟后端请求所有用户
  const fetchUserList = () => {
    // 实际开发中请替换为 axios 请求
    const response = {
      success: true,
      data: [
        {
          user_id: 1,
          username: 'admin',
          real_name: '管理员',
          phone: '13800000000',
          email: 'admin@example.com',
          role_type: 1,
          create_time: '2023-01-01 10:00:00'
        },
        {
          user_id: 2,
          username: 'user1',
          real_name: '张三',
          phone: '13900000000',
          email: 'zhang@example.com',
          role_type: 2,
          create_time: '2023-02-01 14:20:00'
        }
      ]
    }
  
    if (response.success) {
      userList.value = response.data
    }
  }
  
  onMounted(() => {
    if (currentUser.value?.role_type === 1) {
      fetchUserList()
    }
  })
  
  const openEdit = (user: User) => {
    selectedUser.value = { ...user }
    showDialog.value = true
  }
  
  const handleUpdate = (updatedUser: User) => {
    const index = userList.value.findIndex(u => u.user_id === updatedUser.user_id)
    if (index !== -1) userList.value[index] = updatedUser
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
  .user-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    background-color: white;
  }
  .user-table th,
  .user-table td {
    padding: 0.75rem 1rem;
    border: 1px solid #ddd;
    text-align: center;
  }
  .user-table th {
    background-color: #f3f4f6;
  }
  button {
    padding: 0.4rem 0.8rem;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.4rem;
    cursor: pointer;
  }
  button:hover {
    background-color: #2563eb;
  }
</style>
  
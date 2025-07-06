// src/stores/user.ts
import { ref } from 'vue'

export const currentUser = ref<{ user_id: number, role_type: number } | null>(null)

// 启动时从 localStorage 恢复
const saved = localStorage.getItem('currentUser')
if (saved) {
  currentUser.value = JSON.parse(saved)
}

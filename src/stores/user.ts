<<<<<<< HEAD
// src/store/user.ts
import { ref } from 'vue'

export const currentUser = ref<{ user_id: string } | null>(null)
// 定义用户类型接口

// 启动时从 localStorage 恢复
const saved = localStorage.getItem('currentUser')
if (saved) {
  currentUser.value = JSON.parse(saved)
}
=======
// src/store/user.ts
import { ref } from 'vue'

export const currentUser = ref<{ user_id: string } | null>(null)

// 启动时从 localStorage 恢复
const saved = localStorage.getItem('currentUser')
if (saved) {
  currentUser.value = JSON.parse(saved)
}
>>>>>>> 2169fedfedc3d443e3192294224aa2ddb9a5d482

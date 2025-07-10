// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

import Home from '@/views/Home.vue'
import BasicAnalysis from '@/views/BasicAnalysis.vue'
import ContentAnalysis from '@/views/ContentAnalysis.vue'
import TeamAnalysis from '@/views/TeamAnalysis.vue'
import SpatioTemporalAnalysis from '@/views/SpatioTemporalAnalysis.vue'
import AudienceMarketAnalysis from '@/views/AudienceMarketAnalysis.vue'
import UserAdmin from '@/views/User.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import admin from '@/views/admin.vue'
import AiChat from '../views/AiChat.vue'

// 添加类型注解
const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'Home', component: Home },
  { path: '/basic', name: 'BasicAnalysis', component: BasicAnalysis },
  { path: '/content', name: 'ContentAnalysis', component: ContentAnalysis },
  { path: '/team', name: 'TeamAnalysis', component: TeamAnalysis },
  { path: '/space-time', name: 'SpatioTemporalAnalysis', component: SpatioTemporalAnalysis },
  { path: '/market', name: 'AudienceMarketAnalysis', component: AudienceMarketAnalysis },
  { path: '/user', name: 'UserAdmin', component: UserAdmin },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path:'/admin', component:admin },
  { path:'/AiChat', component:AiChat },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

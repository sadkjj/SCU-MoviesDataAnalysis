<template>
  <div class="ai-chat-container">
    <header class="chat-header">
      <h1>🤖 AI 聊天助手</h1>
      <p class="subtitle">随时随地，智能陪伴 ✨</p>
    </header>

    <div ref="chatWindow" class="chat-window">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="message-content">
          <span class="emoji" v-if="msg.role === 'user'"></span>
          <span class="emoji" v-else>💬</span>
          {{ msg.content }}
        </div>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="说点什么吧...（按回车发送）"
        autocomplete="off"
      />
      <button @click="sendMessage" aria-label="发送消息">
        🚀 发送
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api';

const messages = ref<{ role: string; content: string }[]>([])
const userInput = ref('')
const chatWindow = ref<HTMLElement | null>(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatWindow.value) {
      chatWindow.value.scrollTop = chatWindow.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  const content = userInput.value.trim()
  if (!content) return

  messages.value.push({ role: 'user', content })
  userInput.value = ''
  scrollToBottom()

  try {
    const res = await axios.get(
      `${API_BASE_URL}/dialog`,
      {
        params: {
          message: content,
        },
      }
    )
    const reply = res.data.message || '🤔 机器人无言以对...'
    messages.value.push({ role: 'bot', content: reply })
    scrollToBottom()
  } catch (error) {
    messages.value.push({
      role: 'bot',
      content: '❌ 请求失败，请稍后重试。',
    })
    scrollToBottom()
    console.error(error)
  }
}

watch(messages, () => {
  scrollToBottom()
})

onMounted(() => {
  // 先放个欢迎消息
  messages.value.push({
    role: 'bot',
    content: '你好！我是你的AI聊天助手，开始聊天吧！😊',
  })
  scrollToBottom()
})
</script>

<style scoped>
.ai-chat-container {
  max-width: 800px;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  height: 700px;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.3);
  background: linear-gradient(135deg, #6b8dd6c3 0%, #a0c0ffba 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #222;
}

.chat-header {
  background: linear-gradient(90deg, #40a0ffc5, #66b0ffe5);
  padding: 16px 24px;
  color: white;
  text-align: center;
  box-shadow: 0 4px 8px rgb(64 158 255 / 0.4);
  user-select: none;
}

.chat-header h1 {
  margin: 0;
  font-weight: 700;
  font-size: 1.8rem;
}

.subtitle {
  font-size: 0.9rem;
  font-style: italic;
  opacity: 0.85;
  margin-top: 4px;
}

.chat-window {
  flex: 1;
  padding: 16px 24px;
  background: #f7f9ff;
  overflow-y: auto;
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 聊天气泡 */
.message {
  max-width: 75%;
  padding: 12px 18px;
  border-radius: 20px;
  position: relative;
  word-wrap: break-word;
  font-size: 1rem;
  line-height: 1.4;
  box-shadow: 0 2px 6px rgb(0 0 0 / 0.1);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.message.user {
  background: #409eff;
  color: #fff;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
  animation: slideInRight 0.3s ease forwards;
}

.message.bot {
  background: #e0e7ff;
  color: #2c3e50;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  animation: slideInLeft 0.3s ease forwards;
}

.emoji {
  font-size: 1.4rem;
  user-select: none;
}

/* 输入区域 */
.input-area {
  display: flex;
  padding: 16px 24px;
  background: #409eff;
  gap: 12px;
}

input[type='text'] {
  flex: 1;
  padding: 12px 16px;
  border-radius: 9999px;
  border: none;
  font-size: 1.1rem;
  outline: none;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 0 0 transparent;
}

input[type='text']:focus {
  box-shadow: 0 0 10px #7abaff;
}

button {
  background: #2563eb;
  border: none;
  border-radius: 9999px;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  padding: 0 24px;
  cursor: pointer;
  user-select: none;
  transition: background 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

button:hover {
  background: #1e40af;
  box-shadow: 0 0 12px #1e40afaa;
}

/* 动画 */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 响应式 */
@media (max-width: 640px) {
  .ai-chat-container {
    height: 500px;
    margin: 1rem;
  }

  .chat-header h1 {
    font-size: 1.4rem;
  }

  .message {
    max-width: 90%;
    font-size: 0.9rem;
  }
}
</style>

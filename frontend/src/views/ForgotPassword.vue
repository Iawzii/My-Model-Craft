<template>
  <div class="flex flex-col">
    <section>
      <div class="container mx-auto px-8 py-4 max-w-6xl">
        <nav class="text-1xl text-gray-600 flex items-center gap-2">
          <router-link to="/" class="hover:underline">主页</router-link>
          <span class="text-gray-400">></span>
          <span class="text-gray-900">找回 / 重置密码</span>
        </nav>
      </div>
    </section>
    <section>
      <div class="container mx-auto px-8 py-10">
        <div class="max-w-5xl mx-auto grid gap-8 lg:grid-cols-2">
          <div
            class="bg-white rounded-2xl border p-6 sm:p-8 shadow transition-all"
            :class="activePanel === 'send' ? 'border-blue-200 shadow-xl' : 'border-gray-100'"
          >
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold text-gray-900">步骤一：发送验证码</h2>
              <span class="text-sm text-gray-400">Step 1</span>
            </div>
            <p class="text-sm text-gray-600 mb-6">输入注册邮箱，我们会发送验证码。验证码有效期有限，请及时查收邮件。</p>
            <div v-if="sendError" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg">{{ sendError }}</div>
            <div v-if="sendSuccess" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-600 rounded-lg">{{ sendSuccess }}</div>
            <form @submit.prevent="handleSend" class="space-y-4">
              <input
                type="email"
                v-model="email"
                class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="请输入注册邮箱"
              />
              <button type="submit" :disabled="sendLoading" class="w-full py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:bg-gray-300">
                {{ sendLoading ? '发送中...' : '发送验证码' }}
              </button>
            </form>
            <p class="text-xs text-gray-400 mt-4">提示：若未收到邮件，可检查垃圾邮箱或稍后再试。</p>
          </div>

          <div
            class="bg-white rounded-2xl border p-6 sm:p-8 shadow transition-all"
            :class="activePanel === 'reset' ? 'border-blue-200 shadow-xl' : 'border-gray-100'"
          >
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold text-gray-900">步骤二：重置密码</h2>
              <span class="text-sm text-gray-400">Step 2</span>
            </div>
            <p class="text-sm text-gray-600 mb-6">填写邮箱、验证码与新密码完成重置。收到验证码后即可直接在此完成操作。</p>
            <div v-if="resetError" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg">{{ resetError }}</div>
            <div v-if="resetSuccess" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-600 rounded-lg">{{ resetSuccess }}</div>
            <form @submit.prevent="handleReset" class="space-y-4">
              <input
                type="email"
                v-model="email"
                class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="请输入注册邮箱"
              />
              <input
                type="text"
                v-model="code"
                maxlength="6"
                class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500 tracking-widest"
                placeholder="请输入 6 位验证码"
              />
              <input
                type="password"
                v-model="newPassword"
                class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="请输入新的密码"
              />
              <input
                type="password"
                v-model="confirmPassword"
                class="w-full p-3 border rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="再次输入新的密码"
              />
              <button type="submit" :disabled="resetLoading" class="w-full py-3 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:bg-gray-300">
                {{ resetLoading ? '重置中...' : '确认重置' }}
              </button>
            </form>
            <div class="mt-4 text-xs text-gray-400 flex items-center justify-between">
              <span>已经收到验证码？直接在此完成重置。</span>
              <button type="button" class="text-blue-600 hover:underline" @click="activePanel = 'reset'">切换至步骤二</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const code = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const sendLoading = ref(false)
const resetLoading = ref(false)
const sendError = ref('')
const sendSuccess = ref('')
const resetError = ref('')
const resetSuccess = ref('')
const activePanel = ref('send')
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const handleSend = async () => {
  sendError.value = ''
  sendSuccess.value = ''

  if (!email.value || !emailRegex.test(email.value)) {
    sendError.value = '请输入有效的邮箱地址'
    return
  }

  sendLoading.value = true
  const result = await authStore.forgotPassword(email.value)
  sendLoading.value = false

  if (result.success) {
    sendSuccess.value = result.message
    activePanel.value = 'reset'
  } else {
    sendError.value = result.message
  }
}

const handleReset = async () => {
  resetError.value = ''
  resetSuccess.value = ''

  if (!email.value || !emailRegex.test(email.value)) {
    resetError.value = '请输入有效的邮箱地址'
    return
  }
  if (!code.value || code.value.length !== 6) {
    resetError.value = '请输入 6 位验证码'
    return
  }
  if (!newPassword.value || newPassword.value.length < 6) {
    resetError.value = '新密码至少 6 位'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    resetError.value = '两次输入的密码不一致'
    return
  }

  resetLoading.value = true
  const result = await authStore.resetPassword({
    email: email.value,
    code: code.value,
    newPassword: newPassword.value
  })
  resetLoading.value = false

  if (result.success) {
    resetSuccess.value = result.message
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } else {
    resetError.value = result.message
  }
}
</script>

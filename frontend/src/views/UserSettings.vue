<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <section>
      <div class="container mx-auto px-12 py-4 max-w-6xl">
        <nav class="text-1xl text-gray-600">
          <router-link to="/" class="hover:underline">主页</router-link>
          <span class="mx-2">></span>
          <span class="text-gray-900">账号设置</span>
        </nav>
      </div>
    </section>
    <section>
      <div class="container mx-auto px-12 py-4 max-w-6xl">
        <!-- 标题区域 -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">账户设置</h1>
          <p class="text-gray-600">您可以在此处设置您的账户信息</p>
        </div>
        <!--以下为分别设计的卡片区域-->
        <div class="space-y-6">
          <!-- 头像设置卡片 -->
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">头像设置</h2>
            <p>这是头像设置</p>
            <p class="mb-2">你可以点击头像以上传头像</p>
            <div class="flex items-center gap-4">
              <div class="flex-1">
                <p class="text-gray-600">头像不是必须的，但我们推荐你上传自己的头像</p>
              </div>
              <label class="cursor-pointer">
                <input
                  type="file"
                  ref="avatarInput"
                  @change="handleAvatarChange"
                  accept="image/*"
                  class="hidden"
                />
                <div class="w-20 h-20 rounded-full bg-blue-500 flex items-center justify-center text-white text-xl font-semibold hover:bg-blue-600 transition-colors">
                  <span v-if="!avatarPreview">{{ avatarInitial }}</span>
                  <img
                    v-else
                    :src="avatarPreview"
                    alt="Avatar"
                    class="w-full h-full rounded-full object-cover"
                  />
                </div>
              </label>
            </div>
            <p v-if="avatarMessage" class="mt-3 text-sm" :class="avatarMessageClass">{{ avatarMessage }}</p>
          </div>
          <!-- 用户名设置卡片 逻辑未实现-->
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">用户名设置</h2>
            <p>这是用户名设置</p>
            <p class="mb-2">你的用户名必须唯一</p>
            <div class="space-y-3">
              <input
                v-model="username"
                type="text"
                placeholder="用户名"
                maxlength="17"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <div class="flex items-center justify-between">
                <p class="text-xs text-gray-500">
                  用户名长度最大为17,字符要求：汉字、字母、数字、下划线
                </p>
                <button
                  @click="saveUsername"
                  :disabled="savingUsername || username === originalUsername"
                  class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  保存
                </button>
              </div>
              <p v-if="usernameMessage" class="text-sm" :class="usernameMessageClass">{{ usernameMessage }}</p>
            </div>
          </div>
          <!-- 简介设置卡片 -->
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">简介设置</h2>
            <p>在此更新你的个人简介</p>
            <p class="mb-2">简介可以为空</p>
            <div class="space-y-3">
              <textarea
                v-model="bio"
                rows="3"
                placeholder="个性签名 / 简介"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              ></textarea>
              <div class="flex items-center justify-between">
                <p class="text-xs text-gray-500">
                  简短介绍有助于好友了解你
                </p>
                <button
                  @click="saveBio"
                  :disabled="savingBio"
                  class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  保存
                </button>
              </div>
              <p v-if="bioMessage" class="text-sm" :class="bioMessageClass">{{ bioMessage }}</p>
            </div>
          </div>
          <!-- 邮箱设置卡片 -->
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">邮箱设置</h2>
            <p>这是邮箱设置</p>
            <p class="mb-2">你的邮箱必须唯一</p>
            <div class="space-y-3">
              <input
                v-model="email"
                type="email"
                placeholder="邮箱"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                v-model="confirmEmail"
                type="email"
                placeholder="再次输入邮箱"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <div class="flex items-center justify-between">
                <p class="text-xs text-gray-500">
                  确认邮箱输入无误后保存
                </p>
                <button
                  @click="saveEmail"
                  :disabled="savingEmail"
                  class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  保存
                </button>
              </div>
              <p v-if="emailMessage" class="text-sm" :class="emailMessageClass">{{ emailMessage }}</p>
            </div>
          </div>
          <!-- 密码设置卡片 逻辑未实现-->
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">密码设置</h2>
            <p>这是密码设置</p>
            <p class="mb-2">你需要输入旧密码以更改新密码</p>
            <div class="space-y-3">
              <input
                v-model="formerPassword"
                type="text"
                placeholder="旧密码"
                maxlength="17"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                v-model="newPassword"
                type="text"
                placeholder="新密码"
                maxlength="17"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <div class="flex items-center justify-between">
                <p class="text-xs text-gray-500">
                  密码最长17位，可以选择性的包含!#$%^&*()_-+=\/ 等特殊字符, 至少包含数字和英语字母
                </p>
                <button
                  @click="savePassword"
                  :disabled="savingPassword"
                  class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  保存
                </button>
              </div>
              <p v-if="passwordMessage" class="text-sm" :class="passwordMessageClass">{{ passwordMessage }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const DEFAULT_AVATAR = 'https://i.pravatar.cc/150'

const avatarInput = ref(null)
const avatarPreview = ref(null)
const avatarMessage = ref('')
const avatarSaving = ref(false)

const username = ref('')
const originalUsername = ref('')
const savingUsername = ref(false)
const usernameMessage = ref('')

const bio = ref('')
const savingBio = ref(false)
const bioMessage = ref('')

const email = ref('')
const confirmEmail = ref('')
const savingEmail = ref(false)
const emailMessage = ref('')

const formerPassword = ref('')
const newPassword = ref('')
const savingPassword = ref(false)
const passwordMessage = ref('')

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const avatarInitial = computed(() => {
  const name = authStore.username || ''
  return name.charAt(0).toUpperCase() || 'U'
})

const avatarMessageClass = computed(() =>
  avatarMessage.value.includes('成功') ? 'text-green-600' : 'text-red-600'
)

const usernameMessageClass = computed(() =>
  usernameMessage.value.includes('成功') ? 'text-green-600' : 'text-red-600'
)

const bioMessageClass = computed(() =>
  bioMessage.value.includes('成功') ? 'text-green-600' : 'text-red-600'
)

const emailMessageClass = computed(() =>
  emailMessage.value.includes('成功') ? 'text-green-600' : 'text-red-600'
)

const passwordMessageClass = computed(() =>
  passwordMessage.value.includes('成功') ? 'text-green-600' : 'text-red-600'
)

const syncState = () => {
  const user = authStore.user
  username.value = user?.username || ''
  originalUsername.value = username.value
  bio.value = user?.bio || ''
  email.value = user?.email || ''
  confirmEmail.value = user?.email || ''
  avatarPreview.value = user?.avatarUrl && user.avatarUrl !== DEFAULT_AVATAR ? user.avatarUrl : null
}

onMounted(() => {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  syncState()
})

watch(
  () => authStore.user,
  () => {
    syncState()
  }
)

const readFileAsDataUrl = (file) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })

const handleAvatarChange = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return
  avatarMessage.value = ''
  avatarSaving.value = true
  try {
    const base64 = await readFileAsDataUrl(file)
    avatarPreview.value = base64
    const result = await authStore.updateAvatar(base64)
    avatarMessage.value = result.message
  } catch (error) {
    avatarMessage.value = error.message || '头像更新失败'
  } finally {
    avatarSaving.value = false
  }
}

const saveUsername = async () => {
  usernameMessage.value = ''
  if (!username.value.trim()) {
    usernameMessage.value = '用户名不能为空'
    return
  }
  if (username.value.trim() === originalUsername.value) {
    usernameMessage.value = '用户名未变化'
    return
  }
  savingUsername.value = true
  const result = await authStore.updateUsername(username.value.trim())
  savingUsername.value = false
  usernameMessage.value = result.message
  if (result.success) {
    originalUsername.value = username.value.trim()
  }
}

const saveBio = async () => {
  bioMessage.value = ''
  savingBio.value = true
  const result = await authStore.updateBio(bio.value || null)
  savingBio.value = false
  bioMessage.value = result.message
}

const saveEmail = async () => {
  emailMessage.value = ''
  if (!email.value || !emailRegex.test(email.value)) {
    emailMessage.value = '请输入合法的邮箱地址'
    return
  }
  if (email.value !== confirmEmail.value) {
    emailMessage.value = '两次输入的邮箱不一致'
    return
  }
  savingEmail.value = true
  const result = await authStore.updateEmail(email.value.trim())
  savingEmail.value = false
  emailMessage.value = result.message
  if (result.success) {
    confirmEmail.value = email.value.trim()
  }
}

const savePassword = async () => {
  passwordMessage.value = ''
  if (!formerPassword.value || !newPassword.value) {
    passwordMessage.value = '请填写完整的密码信息'
    return
  }
  if (formerPassword.value === newPassword.value) {
    passwordMessage.value = '新密码不能与旧密码相同'
    return
  }
  if (newPassword.value.length < 6) {
    passwordMessage.value = '新密码至少6位'
    return
  }
  savingPassword.value = true
  const result = await authStore.changePassword(formerPassword.value, newPassword.value)
  savingPassword.value = false
  passwordMessage.value = result.message
  if (result.success) {
    formerPassword.value = ''
    newPassword.value = ''
  }
}
</script>
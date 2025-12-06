<template>
  <div class="flex flex-col min-h-[60vh]">
    <section class="bg-gray-50 border-b border-gray-100">
      <div class="container mx-auto px-8 py-4 max-w-6xl">
        <nav class="text-base text-gray-600 flex items-center gap-2">
          <router-link to="/" class="hover:underline">主页</router-link>
          <span class="text-gray-400">></span>
          <span class="text-gray-900">{{ breadcrumbName }}的用户主页</span>
        </nav>
      </div>
    </section>

    <section class="flex-1">
      <div class="container mx-auto px-8 py-6 max-w-6xl">
        <div v-if="isLoading" class="bg-white rounded-2xl shadow p-10 text-center text-gray-500">
          正在加载用户信息...
        </div>

        <div v-else-if="error" class="bg-white rounded-2xl shadow p-10 text-center space-y-4">
          <p class="text-gray-600">{{ error }}</p>
          <div class="flex justify-center gap-4">
            <button
              class="px-5 py-2 rounded-xl border border-gray-200 text-gray-700 hover:bg-gray-50"
              @click="loadProfile"
            >
              重试
            </button>
            <router-link
              v-if="shouldPromptLogin"
              to="/login"
              class="px-5 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700"
            >
              去登录
            </router-link>
          </div>
        </div>

        <div v-else class="grid gap-8 lg:grid-cols-[320px,1fr]">
          <!-- 左侧信息卡 -->
          <div class="bg-white rounded-2xl shadow-md p-8 space-y-5">
            <div class="flex flex-col items-center text-center space-y-3">
              <div class="w-28 h-28 rounded-full bg-blue-500 text-white text-3xl font-semibold flex items-center justify-center">
                <span v-if="!avatarUrl">{{ userInitial }}</span>
                <img v-else :src="avatarUrl" alt="用户头像" class="w-full h-full rounded-full object-cover" />
              </div>
              <div>
                <h1 class="text-2xl font-semibold text-gray-900">{{ profile?.username }}</h1>
                <p class="text-sm text-gray-500 mt-1" v-if="profile?.bio">{{ profile.bio }}</p>
                <p class="text-sm text-gray-400 mt-1" v-else>这个用户还没有填写简介</p>
              </div>
            </div>

            <div class="text-center text-sm text-gray-500">
              <div class="flex flex-col space-y-2">
                <div
                  class="relative flex justify-center"
                  @mouseleave="closeConnectionPanel('followers')"
                  @mouseenter="handleConnectionHover('followers')"
                >
                  <button
                    type="button"
                    class="px-3 py-1 rounded-full border border-transparent hover:border-blue-200 hover:text-blue-600 transition-colors"
                    @click="toggleConnectionPanel('followers')"
                  >
                    {{ profile?.followersCount ?? 0 }} 人关注 TA
                  </button>
                  <div
                    v-if="activeConnectionType === 'followers'"
                    class="absolute top-full left-1/2 -translate-x-1/2 mt-3 z-20"
                  >
                    <UserConnectionsPopover
                      title="关注 TA 的用户"
                      :users="connectionDetails.followers"
                      :loading="connectionLoading.followers"
                      empty-text="还没有粉丝"
                    />
                  </div>
                </div>

                <div
                  class="relative flex justify-center"
                  @mouseleave="closeConnectionPanel('following')"
                  @mouseenter="handleConnectionHover('following')"
                >
                  <button
                    type="button"
                    class="px-3 py-1 rounded-full border border-transparent hover:border-blue-200 hover:text-blue-600 transition-colors"
                    @click="toggleConnectionPanel('following')"
                  >
                    {{ profile?.followingCount ?? 0 }} 正在关注
                  </button>
                  <div
                    v-if="activeConnectionType === 'following'"
                    class="absolute top-full left-1/2 -translate-x-1/2 mt-3 z-20"
                  >
                    <UserConnectionsPopover
                      title="TA 关注的用户"
                      :users="connectionDetails.following"
                      :loading="connectionLoading.following"
                      empty-text="还没有关注任何人"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="text-sm text-gray-500 flex items-center justify-center">
              {{ joinedAtText }}
            </div>

            <div class="space-y-3">
              <template v-if="isOwnProfile">
                <router-link
                  to="/settings/user"
                  class="w-full flex items-center justify-center gap-2 px-4 py-2 border border-blue-200 text-blue-600 rounded-xl hover:bg-blue-50 transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
                  编辑信息
                </router-link>
                <button
                  class="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
                  @click="handleStartCreate"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  开始创作
                </button>
              </template>
              <template v-else>
                <button
                  class="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-xl transition-colors"
                  :class="isFollowing ? 'bg-gray-100 text-gray-600 hover:bg-gray-200' : 'bg-blue-600 text-white hover:bg-blue-700'"
                  :disabled="isFollowProcessing"
                  @click="handleFollowToggle"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M18 9l-6 6-3-3"
                    />
                  </svg>
                  {{ isFollowing ? '已关注' : '关注用户' }}
                </button>
              </template>
            </div>
          </div>

          <!-- 右侧内容 -->
          <div class="space-y-6">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div
                v-for="stat in quickStats"
                :key="stat.key"
                class="bg-white rounded-2xl shadow-md p-5 flex flex-col gap-2"
              >
                <div class="flex items-center justify-between text-sm text-gray-500">
                  <span>{{ stat.label }}</span>
                  <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" :d="stat.iconPath" />
                  </svg>
                </div>
                <div class="text-2xl font-semibold text-gray-900">{{ stat.value }}</div>
              </div>
            </div>

            <div class="bg-white rounded-2xl shadow-md">
              <div class="flex border-b border-gray-100 text-sm font-medium text-gray-500">
                <button
                  v-for="tab in tabs"
                  :key="tab.value"
                  class="flex-1 py-4 text-center transition-all"
                  :class="activeTab === tab.value ? 'text-blue-600 border-b-2 border-blue-500 bg-blue-50/30' : 'hover:text-gray-900'"
                  @click="activeTab = tab.value"
                >
                  {{ tab.label }}
                </button>
              </div>

              <div v-if="activeTab === 'models'" class="p-8">
                <div v-if="userModels.length" class="grid gap-6 md:grid-cols-2">
                  <ModelCard
                    v-for="model in userModels"
                    :key="model.id"
                    :model="model"
                    @click="handleModelClick"
                  />
                </div>
                <div
                  v-else
                  class="flex flex-col items-center justify-center text-center text-sm text-gray-500 space-y-4 py-10"
                >
                  <div class="w-24 h-24 rounded-full bg-blue-50 flex items-center justify-center text-4xl text-blue-400">
                    :(
                  </div>
                  <p>暂时还没有发布过模型，期待新的作品！</p>
                </div>
              </div>

              <div v-else-if="activeTab === 'comments'" class="p-12 flex flex-col items-center text-center text-sm text-gray-500 space-y-4">
                <div class="w-24 h-24 rounded-full bg-blue-50 flex items-center justify-center text-4xl text-blue-400">
                  :)
                </div>
                <p>评论功能即将上线，敬请期待。</p>
              </div>

              <div v-else class="p-12 flex flex-col items-center text-center text-sm text-gray-500 space-y-4">
                <div class="w-24 h-24 rounded-full bg-blue-50 flex items-center justify-center text-4xl text-blue-400">
                  ★
                </div>
                <p>收藏列表还是空空的，快去挑选喜欢的作品吧～</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ModelCard from '@/components/ModelCard.vue'
import UserConnectionsPopover from '@/components/UserConnectionsPopover.vue'
import { usersApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useModelsStore } from '@/stores/models'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const modelsStore = useModelsStore()

const profile = ref(null)
const userModels = ref([])
const isLoading = ref(true)
const error = ref('')
const activeTab = ref('models')
const isFollowProcessing = ref(false)
const activeConnectionType = ref('')
const connectionDetails = reactive({
  followers: [],
  following: []
})
const connectionLoading = reactive({
  followers: false,
  following: false
})

const tabs = [
  { label: '发布模型', value: 'models' },
  { label: '评论', value: 'comments' },
  { label: '收藏夹', value: 'favorites' }
]

const avatarUrl = computed(() => profile.value?.avatarUrl || null)
const breadcrumbName = computed(() => profile.value?.username || '用户')
const userInitial = computed(() => {
  const name = profile.value?.username || 'U'
  return name.charAt(0).toUpperCase()
})
const joinedAtText = computed(() => {
  const createdAt = profile.value?.createdAt
  if (!createdAt) return '加入时间未知'
  const date = new Date(createdAt)
  if (Number.isNaN(date.getTime())) return '加入时间未知'
  return `加入于 ${date.toLocaleDateString()}`
})
const isOwnProfile = computed(() => profile.value?.isSelf ?? (profile.value?.id && profile.value?.id === authStore.user?.id))
const isFollowing = computed(() => profile.value?.isFollowing ?? false)
const shouldPromptLogin = computed(() => !route.params.id && !authStore.isLoggedIn)

const quickStats = computed(() => [
  { key: 'models', label: '模型', value: profile.value?.modelCount ?? 0, iconPath: 'M12 6l7 4-7 4-7-4 7-4zm0 8v4m-4 0h8' },
  { key: 'followers', label: '粉丝', value: profile.value?.followersCount ?? 0, iconPath: 'M8 10h8m-8 4h5m-1 5l-4 4v-4H5a2 2 0 01-2-2V5a2 2 0 012-2h14a2 2 0 012 2v12a2 2 0 01-2 2h-3l-3 4v-4' },
  { key: 'following', label: '关注', value: profile.value?.followingCount ?? 0, iconPath: 'M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8.5z' },
  { key: 'favorites', label: '收藏', value: profile.value?.collectCount ?? 0, iconPath: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.967a1 1 0 00.95.69h4.178c.969 0 1.371 1.24.588 1.81l-3.383 2.46a1 1 0 00-.364 1.118l1.287 3.966c.3.922-.755 1.688-1.54 1.118l-3.383-2.46a1 1 0 00-1.175 0l-3.383 2.46c-.784.57-1.838-.196-1.539-1.118l1.287-3.966a1 1 0 00-.364-1.118L2.547 9.394c-.783-.57-.38-1.81.588-1.81h4.178a1 1 0 00.95-.69l1.286-3.967z' }
])

const resetConnectionState = () => {
  activeConnectionType.value = ''
  connectionDetails.followers = []
  connectionDetails.following = []
}

const ensureConnectionDetails = async (type) => {
  if (!profile.value) {
    connectionDetails[type] = []
    return
  }
  const ids = type === 'followers' ? profile.value.followers : profile.value.following
  if (!ids || !ids.length) {
    connectionDetails[type] = []
    return
  }

  const cachedIds = connectionDetails[type].map((user) => user.id)
  const sameLength = cachedIds.length === ids.length
  const sameOrder = sameLength && cachedIds.every((id, index) => id === ids[index])
  if (sameOrder && !connectionLoading[type]) {
    return
  }

  connectionLoading[type] = true
  try {
    const { data } = await usersApi.lookup(ids)
    connectionDetails[type] = data
  } catch (error) {
    console.warn('Failed to load user connections', error)
  } finally {
    connectionLoading[type] = false
  }
}

const handleConnectionHover = (type) => {
  ensureConnectionDetails(type)
}

const toggleConnectionPanel = async (type) => {
  if (activeConnectionType.value === type) {
    activeConnectionType.value = ''
    return
  }
  await ensureConnectionDetails(type)
  activeConnectionType.value = type
}

const closeConnectionPanel = (type) => {
  if (activeConnectionType.value === type) {
    activeConnectionType.value = ''
  }
}

const fetchUserModels = async (authorId) => {
  try {
    userModels.value = await modelsStore.fetchAuthorModels(authorId, 8)
  } catch (err) {
    console.warn('Failed to load user models', err)
    userModels.value = []
  }
}

const loadProfile = async () => {
  const targetId = route.params.id || authStore.user?.id || null
  if (!targetId) {
    profile.value = null
    userModels.value = []
    error.value = '请先登录后再查看个人主页'
    isLoading.value = false
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    const { data } = await usersApi.getById(targetId)
    profile.value = data
    activeTab.value = 'models'
    await fetchUserModels(data.id)
  } catch (err) {
    error.value = err.message || '加载用户信息失败'
    profile.value = null
    userModels.value = []
  } finally {
    isLoading.value = false
  }
}

watch(
  () => [route.params.id, authStore.user?.id],
  () => {
    resetConnectionState()
    loadProfile()
  },
  { immediate: true }
)

watch(
  () => profile.value?.id,
  () => {
    resetConnectionState()
  }
)

const handleFollowToggle = async () => {
  if (!profile.value) return
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }

  isFollowProcessing.value = true
  try {
    const apiCall = isFollowing.value ? usersApi.unfollow : usersApi.follow
    const { data } = await apiCall(profile.value.id)
    profile.value = data
  } catch (err) {
    error.value = err.message || '操作失败，请稍后重试'
  } finally {
    isFollowProcessing.value = false
  }
}

const handleModelClick = (modelId) => {
  if (!modelId) return
  router.push(`/model/${modelId}`)
}

const handleStartCreate = () => {
  router.push('/upload')
}
</script>
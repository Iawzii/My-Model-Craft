<template>
  <div class="bg-gray-50 min-h-screen pb-16">
    <section class="bg-white shadow-sm">
      <div class="max-w-6xl mx-auto px-6 py-10 grid gap-10 lg:grid-cols-[1.6fr,1fr]">
        <div>
          <div class="rounded-3xl overflow-hidden bg-gray-900">
            <img
              :src="currentModel.thumbnailUrl || fallbackThumbnail"
              :alt="currentModel.title"
              class="w-full h-[360px] object-cover"
            />
          </div>
          <div class="flex flex-wrap gap-3 mt-5">
            <button
              class="px-6 py-3 rounded-full bg-blue-600 text-white font-semibold shadow"
              :disabled="!modelRenderable"
              @click="handleDownload"
            >
              下载模型
            </button>
            <button class="px-6 py-3 rounded-full border border-gray-300 text-gray-700 hover:border-blue-500">
              收藏 ({{ currentModel.collectCount || 0 }})
            </button>
            <button class="px-6 py-3 rounded-full border border-gray-300 text-gray-700 hover:border-blue-500">
              点赞 ({{ currentModel.likeCount || 0 }})
            </button>
          </div>
        </div>
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <span class="px-3 py-1 rounded-full bg-purple-100 text-purple-700 text-xs font-semibold">
              {{ currentModel.category || '未分类' }}
            </span>
            <span class="text-xs text-gray-500">{{ formattedCreatedAt }}</span>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 leading-tight">
            {{ currentModel.title || '正在加载模型...' }}
          </h1>
          <p class="text-gray-600 leading-relaxed">{{ currentModel.description || '作者尚未填写介绍。' }}</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tag in currentModel.tags"
              :key="tag"
              class="px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs"
            >
              #{{ tag }}
            </span>
            <span v-if="!currentModel.tags?.length" class="text-sm text-gray-400">暂无标签</span>
          </div>
          <div class="grid grid-cols-3 gap-4 bg-gray-50 rounded-2xl p-4">
            <div>
              <p class="text-xs text-gray-500">浏览</p>
              <p class="text-xl font-semibold text-gray-900">{{ stats.views }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">收藏</p>
              <p class="text-xl font-semibold text-gray-900">{{ currentModel.collectCount || 0 }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">点赞</p>
              <p class="text-xl font-semibold text-gray-900">{{ currentModel.likeCount || 0 }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="max-w-6xl mx-auto px-6 mt-8">
      <div class="bg-white rounded-3xl shadow-sm">
        <div class="flex border-b border-gray-100 text-sm font-medium text-gray-500">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            class="flex-1 py-4 text-center transition-all"
            :class="currentTab === tab.value ? 'text-blue-600 border-b-2 border-blue-500 bg-blue-50/30' : 'hover:text-gray-900'"
            @click="currentTab = tab.value"
          >
            {{ tab.label }}
          </button>
        </div>
        <div class="p-8">
          <div v-if="currentTab === 'info'" class="space-y-6">
            <p class="text-gray-700 leading-relaxed whitespace-pre-line">
              {{ currentModel.description || '作者尚未提供详细介绍。' }}
            </p>
            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <div
                v-for="(preview, index) in previewImages"
                :key="preview + index"
                class="rounded-2xl overflow-hidden h-48 bg-gray-100"
              >
                <img :src="preview" class="w-full h-full object-cover" :alt="`preview-${index}`" />
              </div>
              <div v-if="!previewImages.length" class="h-48 rounded-2xl border border-dashed border-gray-200 flex items-center justify-center text-gray-400">
                暂无截图
              </div>
            </div>
            <div class="rounded-2xl border border-blue-100 bg-blue-50/60 p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h3 class="text-lg font-semibold text-gray-900">模拟渲染入口</h3>
                <p class="text-sm text-gray-600">开启浏览器端 Three.js 渲染，预览模型材质与细节。</p>
              </div>
              <div class="flex gap-3">
                <button
                  class="px-5 py-2 rounded-full bg-blue-600 text-white font-semibold disabled:bg-gray-300"
                  :disabled="!modelRenderable"
                  @click="handleRenderEntry"
                >
                  {{ isRendering ? '已开启' : '立即模拟' }}
                </button>
                <button
                  v-if="isRendering"
                  class="px-5 py-2 rounded-full border border-gray-300 text-gray-700"
                  @click="stopRender"
                >
                  停止渲染
                </button>
              </div>
            </div>
          </div>

          <div v-else-if="currentTab === 'discussion'" class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div>
              <h2 class="text-2xl font-semibold text-gray-900">讨论版</h2>
              <p class="text-sm text-gray-500">与其他创作者交流模型制作心得，功能即将上线。</p>
            </div>
            <button
              class="px-6 py-3 rounded-full bg-gray-200 text-gray-500 cursor-not-allowed"
              @click="openDiscussion"
            >
              讨论区开发中
            </button>
          </div>

          <div v-else class="grid gap-8 lg:grid-cols-[320px,1fr]">
            <div class="space-y-4">
              <div class="flex items-center gap-4">
                <img :src="authorAvatar" alt="author" class="w-20 h-20 rounded-full object-cover bg-gray-200" />
                <div>
                  <p class="text-xl font-semibold text-gray-900">{{ authorName }}</p>
                  <p class="text-sm text-gray-500">{{ authorBio }}</p>
                </div>
              </div>
              <div class="flex flex-col gap-3">
                <button
                  class="px-4 py-2 rounded-full bg-blue-600 text-white font-semibold disabled:bg-gray-300"
                  @click="handleFollow"
                >
                  {{ isFollowing ? '已关注' : '关注作者' }}
                </button>
                <button class="px-4 py-2 rounded-full border border-gray-300 text-gray-700" @click="goToAuthor">
                  查看作者主页
                </button>
              </div>
            </div>
            <div>
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">作者最近提交</h3>
                  <p class="text-sm text-gray-500">发现更多来自 {{ authorName }} 的作品</p>
                </div>
              </div>
              <div v-if="authorModels.length" class="grid gap-4 sm:grid-cols-2">
                <ModelCard
                  v-for="item in authorModels"
                  :key="item.id"
                  :model="item"
                  @click="handleModelCardClick(item.id)"
                />
              </div>
              <div v-else class="h-40 rounded-2xl border border-dashed border-gray-200 flex items-center justify-center text-gray-400">
                暂无更多作品
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="isRendering && modelRenderable" ref="renderSectionRef" class="max-w-6xl mx-auto px-6 mt-6">
      <div class="bg-white rounded-3xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">实时渲染</h3>
        <div class="h-[420px] rounded-2xl overflow-hidden bg-black">
          <ModelViewer :model-url="currentModel.fileUrl" class="w-full h-full" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ModelViewer from '@/components/ModelViewer.vue'
import ModelCard from '@/components/ModelCard.vue'
import { useModelsStore } from '@/stores/models'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const modelsStore = useModelsStore()
const authStore = useAuthStore()

const fallbackThumbnail = 'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=1200&q=80'
const defaultModel = {
  title: '',
  description: '',
  tags: [],
  category: '',
  thumbnailUrl: '',
  previewUrls: [],
  likeCount: 0,
  collectCount: 0,
  createdAt: null,
  fileUrl: ''
}

const model = ref(null)
const authorModels = ref([])
const isRendering = ref(false)
const isFollowing = ref(false)
const renderSectionRef = ref(null)
const currentTab = ref('info')

const loadModelDetail = async () => {
  const id = route.params.id
  if (!id) return
  try {
    const data = await modelsStore.fetchModelById(id)
    model.value = data
    isFollowing.value = false
    if (data?.authorId) {
      const list = await modelsStore.fetchAuthorModels(data.authorId, 4)
      authorModels.value = list.filter((item) => item.id !== data.id)
    } else {
      authorModels.value = []
    }
  } catch (error) {
    console.error('Failed to load model detail', error)
  }
}

onMounted(loadModelDetail)
watch(
  () => route.params.id,
  () => {
    isRendering.value = false
    loadModelDetail()
  }
)

const currentModel = computed(() => model.value ?? defaultModel)
const previewImages = computed(() => {
  const list = currentModel.value.previewUrls?.filter(Boolean) || []
  if (list.length) return list
  return currentModel.value.thumbnailUrl ? [currentModel.value.thumbnailUrl] : []
})
const formattedCreatedAt = computed(() => {
  if (!currentModel.value.createdAt) return '刚刚发布'
  try {
    return new Date(currentModel.value.createdAt).toLocaleString()
  } catch (error) {
    return '时间未知'
  }
})
const stats = computed(() => ({ views: (currentModel.value.viewCount || 0) + 200 }))
const modelRenderable = computed(() => Boolean(currentModel.value.fileUrl))
const authorName = computed(() => currentModel.value.author?.username || currentModel.value.authorName || '匿名作者')
const authorBio = computed(() => currentModel.value.author?.bio || '这位作者还没有填写个人介绍。')
const authorAvatar = computed(() => currentModel.value.author?.avatarUrl || fallbackThumbnail)

const handleRenderEntry = async () => {
  if (!modelRenderable.value) return
  isRendering.value = true
  await nextTick()
  renderSectionRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const stopRender = () => {
  isRendering.value = false
}

const handleDownload = () => {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  window.open(currentModel.value.fileUrl, '_blank')
}

const handleFollow = () => {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  isFollowing.value = !isFollowing.value
}

const openDiscussion = () => {
  console.info('讨论版功能开发中')
}

const goToAuthor = () => {
  router.push(`/user/${currentModel.value.authorId}`)
}

const handleModelCardClick = (id) => {
  if (!id) return
  router.push(`/model/${id}`)
}

const tabs = [
  { label: '游戏信息', value: 'info' },
  { label: '讨论版', value: 'discussion' },
  { label: '作者信息', value: 'author' }
]
</script>

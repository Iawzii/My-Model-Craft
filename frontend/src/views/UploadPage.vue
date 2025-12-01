<template>
  <div class="min-h-screen bg-gray-50 py-10">
    <div class="container mx-auto px-6 lg:px-12 max-w-6xl">
      <div class="flex items-center justify-between mb-8">
        <nav class="text-sm text-gray-500 space-x-2">
          <router-link to="/" class="hover:underline">主页</router-link>
          <span>/</span>
          <span>上传模型</span>
        </nav>
        <router-link
          to="/user"
          class="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-2"
        >
          返回个人中心
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>

      <div class="bg-white rounded-3xl shadow-sm border border-gray-100 p-8 space-y-10">
        <!-- 基本信息 -->
        <section>
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-semibold text-gray-900">基本信息</h2>
              <p class="text-sm text-gray-500">填写模型展示所需的标题、简介与标签</p>
            </div>
            <span class="text-sm text-gray-400">* 为必填项</span>
          </div>
          <div class="mt-6 space-y-6">
            <div>
              <label class="flex items-center justify-between text-sm font-medium text-gray-700">
                <span>标题 *</span>
                <span class="text-gray-400">{{ form.title.length }}/50</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                maxlength="50"
                placeholder="请输入模型标题"
                class="mt-2 w-full rounded-2xl border border-gray-200 px-4 py-3 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="flex items-center justify-between text-sm font-medium text-gray-700">
                <span>说明 *</span>
                <span class="text-gray-400">{{ form.description.length }}/1200</span>
              </label>
              <textarea
                v-model="form.description"
                rows="6"
                maxlength="1200"
                placeholder="介绍你的模型亮点、使用说明或版权信息"
                class="mt-2 w-full rounded-2xl border border-gray-200 px-4 py-3 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              ></textarea>
            </div>
            <div class="grid gap-6 md:grid-cols-2">
              <div>
                <label class="text-sm font-medium text-gray-700">格式 *</label>
                <select
                  v-model="form.format"
                  class="mt-2 w-full rounded-2xl border border-gray-200 px-4 py-3 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="" disabled>请选择</option>
                  <option v-for="item in formatOptions" :key="item" :value="item">
                    {{ item }}
                  </option>
                </select>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-700">分类 *</label>
                <select
                  v-model="form.category"
                  class="mt-2 w-full rounded-2xl border border-gray-200 px-4 py-3 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="" disabled>请选择</option>
                  <option v-for="item in categoryOptions" :key="item" :value="item">
                    {{ item }}
                  </option>
                </select>
              </div>
            </div>
            <div>
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">添加标签 *</label>
                <span class="text-xs text-gray-400">最多 20 个标签，还可添加 {{ remainingTags }} 个</span>
              </div>
              <div class="mt-2 flex flex-wrap gap-2">
                <input
                  v-model="tagInput"
                  @keydown.enter.prevent="handleTagEnter"
                  placeholder="输入后按 Enter 创建标签"
                  class="flex-1 min-w-[200px] rounded-2xl border border-gray-200 px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  type="button"
                  class="px-4 py-2 rounded-2xl border border-blue-500 text-blue-600 hover:bg-blue-50"
                  @click="addTag(tagInput)"
                >
                  添加标签
                </button>
              </div>
              <div v-if="form.tags.length" class="mt-3 flex flex-wrap gap-2">
                <span
                  v-for="(tag, index) in form.tags"
                  :key="`${tag}-${index}`"
                  class="inline-flex items-center gap-2 rounded-full bg-blue-50 px-3 py-1 text-sm text-blue-700"
                >
                  {{ tag }}
                  <button type="button" class="text-xs" @click="removeTag(index)">×</button>
                </span>
              </div>
              <div class="mt-4">
                <p class="text-sm text-gray-500 mb-2">推荐标签：</p>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="tag in recommendedTags"
                    :key="tag"
                    type="button"
                    class="rounded-full border px-3 py-1 text-sm"
                    :class="form.tags.includes(tag) ? 'border-blue-500 bg-blue-50 text-blue-600' : 'border-gray-200 text-gray-600 hover:border-blue-500'
                      "
                    @click="addTag(tag)"
                  >
                    {{ tag }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 上传区域 -->
        <section>
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-xl font-semibold text-gray-900">上传内容</h2>
              <p class="text-sm text-gray-500">请按顺序上传模型文件、封面与预览图</p>
            </div>
            <span class="text-xs text-gray-400">仅支持 .glb</span>
          </div>
          <div class="grid gap-6 md:grid-cols-3">
            <div class="rounded-2xl border border-gray-100 p-5 shadow-sm flex flex-col">
              <h3 class="text-base font-semibold text-gray-900">上传模型 *</h3>
              <p class="text-xs text-gray-500 mt-1">推荐包含纹理的 .glb，单文件 &lt; 200MB</p>
              <label class="mt-4 inline-flex items-center justify-center rounded-2xl border border-dashed border-blue-300 bg-blue-50/60 px-4 py-3 text-blue-600 cursor-pointer hover:bg-blue-100">
                <input type="file" class="hidden" accept=".glb" @change="handleModelUpload" />
                {{ uploading.model ? '上传中...' : '选择或拖拽模型文件' }}
              </label>
              <p v-if="uploads.model.filename" class="mt-3 text-sm text-gray-600">已选择：{{ uploads.model.filename }}</p>
              <p
                v-if="uploadAlerts.model.text"
                class="mt-2 text-sm"
                :class="uploadAlerts.model.type === 'success' ? 'text-green-600' : 'text-red-500'"
              >
                {{ uploadAlerts.model.text }}
              </p>
            </div>

            <div class="rounded-2xl border border-gray-100 p-5 shadow-sm flex flex-col">
              <h3 class="text-base font-semibold text-gray-900">上传封面 *</h3>
              <p class="text-xs text-gray-500 mt-1">1280×800，支持 jpg/png/webp，&lt; 5MB</p>
              <label class="mt-4 inline-flex items-center justify-center rounded-2xl border border-dashed border-amber-300 bg-amber-50/60 px-4 py-3 text-amber-600 cursor-pointer hover:bg-amber-100">
                <input type="file" class="hidden" accept="image/*" @change="handleThumbnailUpload" />
                {{ uploading.thumbnail ? '上传中...' : '上传封面' }}
              </label>
              <p v-if="uploads.thumbnail.filename" class="mt-3 text-sm text-gray-600">已选择：{{ uploads.thumbnail.filename }}</p>
              <p
                v-if="uploadAlerts.thumbnail.text"
                class="mt-2 text-sm"
                :class="uploadAlerts.thumbnail.type === 'success' ? 'text-green-600' : 'text-red-500'"
              >
                {{ uploadAlerts.thumbnail.text }}
              </p>
            </div>

            <div class="rounded-2xl border border-gray-100 p-5 shadow-sm flex flex-col">
              <h3 class="text-base font-semibold text-gray-900">上传预览图</h3>
              <p class="text-xs text-gray-500 mt-1">1920×1080，最多 6 张，单张 &lt; 5MB</p>
              <label class="mt-4 inline-flex items-center justify-center rounded-2xl border border-dashed border-purple-300 bg-purple-50/60 px-4 py-3 text-purple-600 cursor-pointer hover:bg-purple-100">
                <input type="file" class="hidden" accept="image/*" multiple @change="handlePreviewUpload" />
                {{ uploading.previews ? '上传中...' : '上传预览图' }}
              </label>
              <p v-if="uploads.previews.length" class="mt-3 text-sm text-gray-600">
                已上传 {{ uploads.previews.length }} 张预览图
              </p>
              <ul v-if="uploads.previews.length" class="mt-2 space-y-1 text-xs text-gray-500 max-h-24 overflow-auto">
                <li v-for="item in uploads.previews" :key="item.url">{{ item.filename }}</li>
              </ul>
              <p
                v-if="uploadAlerts.previews.text"
                class="mt-2 text-sm"
                :class="uploadAlerts.previews.type === 'success' ? 'text-green-600' : 'text-red-500'"
              >
                {{ uploadAlerts.previews.text }}
              </p>
            </div>
          </div>
        </section>

        <!-- 提交 -->
        <section>
          <div class="rounded-3xl border border-gray-100 bg-gray-50 p-6 md:flex md:items-center md:justify-between gap-6">
            <div class="space-y-2">
              <h3 class="text-lg font-semibold text-gray-900">发布模型</h3>
              <p class="text-sm text-gray-500">
                请确保已上传模型文件、封面，并填写必要信息。发布后可在个人主页查看。
              </p>
              <ul class="text-sm text-gray-500 list-disc list-inside space-y-1">
                <li>需登录账号并遵守平台规范</li>
                <li>标题、说明、分类、标签与模型文件为必填项</li>
                <li>上传内容成功后再点击提交发布</li>
              </ul>
              <p
                v-if="submitFeedback.text"
                class="text-sm"
                :class="submitFeedback.type === 'success' ? 'text-green-600' : 'text-red-500'"
              >
                {{ submitFeedback.text }}
              </p>
            </div>
            <div class="mt-6 md:mt-0 md:text-right space-y-3">
              <button
                type="button"
                class="w-full md:w-auto rounded-2xl border border-gray-300 px-6 py-3 text-gray-700 hover:bg-white"
                @click="handleReset"
                :disabled="uploading.submit"
              >
                重置表单
              </button>
              <button
                type="button"
                class="w-full md:w-auto rounded-2xl bg-blue-600 px-8 py-3 text-white font-semibold shadow hover:bg-blue-700 disabled:bg-gray-300"
                :disabled="!canSubmit || uploading.submit"
                @click="handleSubmit"
              >
                {{ uploading.submit ? '提交中...' : '提交发布' }}
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { modelsApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formatOptions = ['GLB (.glb)']
const categoryOptions = ['人物', '场景', '材质', '配件', '建筑', '其他']
const recommendedTags = ['MMD', '模型配布', 'Blender', '原神', '改模配布', 'TDA', '场景', '场景配布', 'Vup', '崩坏3']
const maxTags = 20

const form = reactive({
  title: '',
  description: '',
  format: '',
  category: '',
  tags: []
})

const tagInput = ref('')

const uploads = reactive({
  model: { url: '', path: '', filename: '' },
  thumbnail: { url: '', path: '', filename: '' },
  previews: []
})

const uploadAlerts = reactive({
  model: { type: '', text: '' },
  thumbnail: { type: '', text: '' },
  previews: { type: '', text: '' }
})

const uploading = reactive({
  model: false,
  thumbnail: false,
  previews: false,
  submit: false
})

const submitFeedback = reactive({ type: '', text: '' })

const remainingTags = computed(() => Math.max(0, maxTags - form.tags.length))
const previewUrls = computed(() => uploads.previews.map((item) => item.url))
const canSubmit = computed(() =>
  Boolean(
    form.title.trim() &&
      form.description.trim() &&
      form.format &&
      form.category &&
      form.tags.length &&
      uploads.model.url &&
      uploads.thumbnail.url
  )
)

onMounted(() => {
  if (!authStore.isLoggedIn) {
    router.push('/login')
  }
})

const setAlert = (key, type, text) => {
  uploadAlerts[key].type = type
  uploadAlerts[key].text = text
}

const addTag = (value) => {
  const tag = (value || '').trim()
  if (!tag || form.tags.includes(tag) || form.tags.length >= maxTags) {
    tagInput.value = ''
    return
  }
  form.tags.push(tag)
  tagInput.value = ''
}

const removeTag = (index) => {
  form.tags.splice(index, 1)
}

const handleTagEnter = () => {
  addTag(tagInput.value)
}

const resetAlert = (key) => {
  setAlert(key, '', '')
}

const resetForm = () => {
  form.title = ''
  form.description = ''
  form.format = ''
  form.category = ''
  form.tags = []
  tagInput.value = ''
  uploads.model = { url: '', path: '', filename: '' }
  uploads.thumbnail = { url: '', path: '', filename: '' }
  uploads.previews = []
  Object.keys(uploadAlerts).forEach((key) => resetAlert(key))
}

const clearSubmitFeedback = () => {
  submitFeedback.type = ''
  submitFeedback.text = ''
}

const handleReset = () => {
  clearSubmitFeedback()
  resetForm()
}

const handleModelUpload = async (event) => {
  const file = event.target.files?.[0]
  event.target.value = ''
  if (!file) return
  uploading.model = true
  resetAlert('model')
  try {
    const { data } = await modelsApi.uploadModelFile(file)
    uploads.model = { url: data.url, path: data.path, filename: file.name }
    setAlert('model', 'success', '模型文件上传成功')
  } catch (error) {
    setAlert('model', 'error', error.message || '模型上传失败')
  } finally {
    uploading.model = false
  }
}

const handleThumbnailUpload = async (event) => {
  const file = event.target.files?.[0]
  event.target.value = ''
  if (!file) return
  uploading.thumbnail = true
  resetAlert('thumbnail')
  try {
    const { data } = await modelsApi.uploadThumbnail(file)
    uploads.thumbnail = { url: data.url, path: data.path, filename: file.name }
    setAlert('thumbnail', 'success', '封面上传成功')
  } catch (error) {
    setAlert('thumbnail', 'error', error.message || '封面上传失败')
  } finally {
    uploading.thumbnail = false
  }
}

const handlePreviewUpload = async (event) => {
  const files = Array.from(event.target.files || [])
  event.target.value = ''
  if (!files.length) return
  uploading.previews = true
  resetAlert('previews')
  try {
    const { data } = await modelsApi.uploadPreviews(files)
    uploads.previews = data.urls.map((url, index) => ({
      url,
      filename: files[index]?.name || `预览图 ${index + 1}`
    }))
    setAlert('previews', 'success', '预览图上传成功')
  } catch (error) {
    setAlert('previews', 'error', error.message || '预览图上传失败')
  } finally {
    uploading.previews = false
  }
}

const handleSubmit = async () => {
  submitFeedback.type = ''
  submitFeedback.text = ''
  if (!canSubmit.value) {
    submitFeedback.type = 'error'
    submitFeedback.text = '请先完成必填项并上传必要文件'
    return
  }
  uploading.submit = true
  try {
    const payload = {
      title: form.title.trim(),
      description: form.description.trim(),
      category: form.category,
      tags: [...form.tags],
      fileUrl: uploads.model.url,
      thumbnailUrl: uploads.thumbnail.url,
      previewUrls: previewUrls.value
    }
    await modelsApi.create(payload)
    submitFeedback.type = 'success'
    submitFeedback.text = '模型发布成功，已同步到个人主页！'
    resetForm()
  } catch (error) {
    submitFeedback.type = 'error'
    submitFeedback.text = error.message || '提交失败，请稍后重试'
  } finally {
    uploading.submit = false
  }
}
</script>

<style scoped>
.container {
  max-width: 1100px;
}
</style>

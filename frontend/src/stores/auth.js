import { defineStore } from 'pinia'
import router from '@/router'
import { authApi, usersApi } from '@/api'

const parseUser = () => {
  try {
    const stored = localStorage.getItem('user')
    return stored ? JSON.parse(stored) : null
  } catch (error) {
    console.warn('Failed to parse stored user', error)
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: parseUser(),
    token: localStorage.getItem('token'),
    isLoggedIn: !!localStorage.getItem('token'),
    isHydratingUser: false
  }),

  getters: {
    username: (state) => state.user?.username || '',
    avatarUrl: (state) => state.user?.avatarUrl || null,
    email: (state) => state.user?.email || '',
    userid: (state) => state.user?.id || state.user?._id || ''
  },

  actions: {
    setSession(token, user) {
      this.token = token
      this.user = user
      this.isLoggedIn = !!token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
      }
    },

    async fetchCurrentUser(force = false) {
      if (!this.token) {
        return null
      }
      if (this.isHydratingUser) {
        return this.user
      }
      if (this.user && !force) {
        return this.user
      }

      this.isHydratingUser = true
      try {
        const { data } = await usersApi.getMe()
        this.setSession(this.token, data)
        return data
      } catch (error) {
        console.warn('Failed to fetch current user profile', error)
        if (error?.original?.response?.status === 401) {
          this.logoutAccount()
        }
        throw error
      } finally {
        this.isHydratingUser = false
      }
    },

    async sendVerificationCode(email) {
      try {
        await authApi.sendCode(email)
        return { success: true, message: '验证码发送成功' }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async registerAccount({ username, email, password, code, avatarUrl, bio }) {
      try {
        await authApi.register({ username, email, password, code, avatarUrl, bio })
        return { success: true, message: '注册成功，请登录' }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async loginAccount(identifier, password) {
      try {
        const { data } = await authApi.login({ identifier, password })
        if (data?.access_token) {
          this.setSession(data.access_token, data.user)
          try {
            await this.fetchCurrentUser(true)
          } catch (error) {
            console.warn('Using login payload as fallback user info')
          }
          return { success: true, message: '登录成功' }
        }
        return { success: false, message: '登录失败，请稍后重试' }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async logoutAccount() {
      this.setSession(null, null)
      router.push('/login')
    },

    async updateProfile(updates) {
      try {
        const { data } = await authApi.updateProfile(updates)
        this.setSession(this.token, data)
        await this.fetchCurrentUser(true).catch(() => {})
        return { success: true, message: '资料更新成功', data }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async updateUsername(username) {
      try {
        const { data } = await authApi.updateUsername({ username })
        this.setSession(this.token, data)
        await this.fetchCurrentUser(true).catch(() => {})
        return { success: true, message: '用户名更新成功', data }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async updateEmail(email) {
      try {
        const { data } = await authApi.updateEmail({ email })
        this.setSession(this.token, data)
        await this.fetchCurrentUser(true).catch(() => {})
        return { success: true, message: '邮箱更新成功', data }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async uploadAvatarFile(file) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        const { data } = await authApi.uploadAvatar(formData)
        return { success: true, data }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async updateAvatar(avatarUrl) {
      try {
        const { data } = await authApi.updateAvatar({ avatarUrl })
        this.setSession(this.token, data)
        await this.fetchCurrentUser(true).catch(() => {})
        return { success: true, message: '头像更新成功', data }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async updateBio(bio) {
      try {
        const { data } = await authApi.updateBio({ bio })
        this.setSession(this.token, data)
        await this.fetchCurrentUser(true).catch(() => {})
        return { success: true, message: '简介更新成功', data }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async changePassword(currentPassword, newPassword) {
      try {
        await authApi.changePassword({ currentPassword, newPassword })
        return { success: true, message: '密码修改成功' }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async forgotPassword(email) {
      try {
        await authApi.forgotPassword(email)
        return { success: true, message: '验证码已发送至邮箱' }
      } catch (error) {
        return { success: false, message: error.message }
      }
    },

    async resetPassword({ email, code, newPassword }) {
      try {
        await authApi.resetPassword({ email, code, newPassword })
        return { success: true, message: '密码重置成功' }
      } catch (error) {
        return { success: false, message: error.message }
      }
    }
  }
})


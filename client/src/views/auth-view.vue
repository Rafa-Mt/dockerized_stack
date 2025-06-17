<template>
  <div class="w-full h-full flex flex-col gap-4 items-center justify-center bg-gray-100">
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-sm p-8 flex flex-col items-center">
      <h2 class="text-2xl font-bold mb-6">Login</h2>
      <form @submit.prevent="onLogin" class="w-full flex flex-col gap-4">
        <input v-model="loginForm.username" type="text" placeholder="Username" required
          class="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <input v-model="loginForm.password" type="password" placeholder="Password" required
          class="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <button type="submit" class="w-full py-2 mt-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          :disabled="loginMutating">
          Login
        </button>
      </form>
    </div>

    <p class="text-xl font-bold"> Or </p>

    <div class="bg-white rounded-xl shadow-2xl w-full max-w-sm p-8 flex flex-col items-center">
      <h2 class="text-2xl font-bold mb-6">Register</h2>
      <form @submit.prevent="onRegister" class="w-full flex flex-col gap-4">
        <input v-model="registerForm.email" type="email" placeholder="Email" required
          class="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="registerMutating" />
        <input v-model="registerForm.username" type="text" placeholder="Username" required
          class="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="registerMutating" />
        <input v-model="registerForm.password" type="password" placeholder="Password" required
          class="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="registerMutating" />
        <button type="submit" class="w-full py-2 mt-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          :disabled="registerMutating">
          Register
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useSuperMutation } from '../lib/network/superFetch'
import { loginEndpoint } from '../lib/network/enpoints/login'
import type { LoginTypes } from '../lib/network/enpoints/login'

import { registerEndpoint } from '../lib/network/enpoints/register'
import type { RegisterTypes } from '../lib/network/enpoints/register'
import { authState } from '../lib/auth/authState'

const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  email: '',
  username: '',
  password: ''
})

const { mutate: login, mutating: loginMutating } = useSuperMutation<LoginTypes["Request"], LoginTypes["Response"]>({
  ...loginEndpoint,
  onSuccess: (data) => {
    alert(`Login successful! Welcome, ${data.username}`)
    // Update auth state with user data
    authState.user = {
      username: data.username,
    }
    authState.isAuthenticated = true
  },
  onError: (error) => {
    alert(`Login failed: ${error.message}`)
    // Handle error, e.g., show error message
  }
})

const { mutate: register, mutating: registerMutating } = useSuperMutation<RegisterTypes["Request"], RegisterTypes["Response"]>({
  ...registerEndpoint,
  onSuccess: (_data) => {
    alert(`Registration successful! Welcome ${registerForm.username}!`)
    authState.user = {
      username: registerForm.username,
    }
    authState.isAuthenticated = true
  },
  onError: (error) => {
    alert(`Registration failed: ${error.message}`)
    // Handle error, e.g., show error message
  }
})


function onLogin() {

  if (!loginForm.username || !loginForm.password) {
    alert('Please fill in all fields')
    return
  }

  // login({
  //   username: loginForm.username,
  //   password: loginForm.password
  // })
  authState.user = {
    username: loginForm.username,
  }
  authState.isAuthenticated = true
  
  

}

function onRegister() {
  if (!registerForm.email || !registerForm.username || !registerForm.password) {
    alert('Please fill in all fields')
    return
  }

  register({
    email: registerForm.email,
    username: registerForm.username,
    password: registerForm.password
  })
}
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
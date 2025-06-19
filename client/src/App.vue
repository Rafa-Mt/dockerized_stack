<script setup lang="ts">
import AuthView from './views/auth-view.vue';
import { authState } from './lib/auth/authState';
</script>

<template>
  <div class="w-screen h-screen flex items-center justify-center bg-gray-100">
    
    <AuthView v-if="!authState.isAuthenticated" />
    <div v-else class="text-center">
      <h1 class="text-3xl font-bold mb-4">Welcome Back!</h1>
      <p class="text-lg">You are already logged in.</p>
      <p class="text-sm text-gray-500 mt-2">Feel free to explore the application.</p>
    </div>
  </div>
</template>

<style scoped>
</style>

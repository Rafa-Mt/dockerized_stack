<script setup lang="ts">
import AuthView from './views/auth-view.vue';
import PostsView from './views/posts-view.vue';
import { authState } from './lib/auth/authState';
</script>

<template>
  <div class="w-screen flex items-start justify-center bg-gray-100 p-4">
    
    <AuthView v-if="!authState.isAuthenticated" />
    <PostsView v-else />
    
  </div>
</template>

<style scoped>
</style>

<script setup lang="ts">
import type { Post } from '../lib/posts/types';
import Avatar from "vue-boring-avatars";

defineProps<{
  post: Post;
}>();
</script>

<template>
  <div class="w-full max-w-sm bg-white rounded-lg shadow-lg p-6">
    <div class="flex items-center mb-4">
      <Avatar class="rounded-full" :name="post.author_username" :size="40" variant="beam" />
      <span class="ml-3 font-semibold text-gray-800 text-xl">{{ post.author_username }}</span>
    </div>


    <h2 class="text-xl font-semibold mb-2">{{ post.title }}</h2>
    <p class="text-gray-700 mb-4">{{ post.content }}</p>
    <div class="flex items-center justify-between text-gray-500 text-sm">
      <span>{{ new Date(post.created_at).toLocaleDateString() }}

        {{ new Date(post.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
      </span>
    </div>
  </div>
</template>
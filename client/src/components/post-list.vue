<script setup lang="ts">
import type { Post as PostType } from '../lib/posts/types';
import Post from "./post.vue";

defineProps<{
  posts: PostType[];
  loading?: boolean;
  error: string | null;
}>();



</script>


<template>
  <div class="w-full flex flex-col items-center justify-start gap-4">
    <h2 class="text-4xl font-bold mb-4 ">Posts</h2>


      <Post v-for="post in posts" :key="post.id" :post="post" v-if="posts.length > 0" />
    <p v-if="loading" class="text-gray-500">Loading posts...</p>
    <p v-if="error" class="text-red-500">Error loading posts: {{ error }}</p>
    <p v-if="!loading && !error && posts.length === 0" class="text-gray-500">No posts found.</p>
  </div>

</template>

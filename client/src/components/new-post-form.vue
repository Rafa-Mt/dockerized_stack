<template>
  <div class="w-full h-full flex flex-col gap-4 items-center justify-center">
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-sm p-8 flex flex-col items-center">
      <h2 class="text-2xl font-bold mb-6">New post</h2>
      <form class="w-full flex flex-col gap-4" @submit.prevent="handleSubmit">
        <input v-model="title" type="text" placeholder="Title" required minlength="5" maxlength="50"
          class="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <textarea v-model="content" placeholder="Content" required minlength="8" maxlength="250"
          class="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
        <button type="submit" :disabled="props.mutating"
          class="w-full py-2 mt-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-60">
          {{ props.mutating ? "Posting..." : "Post" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  createPost: (
    { title, content }: { title: string; content: string }
  ) => void;
  mutating?: boolean;
}>();

const title = ref("");
const content = ref("");

function handleSubmit() {
  props.createPost({ title: title.value, content: content.value });
  title.value = "";
  content.value = "";
}
</script>
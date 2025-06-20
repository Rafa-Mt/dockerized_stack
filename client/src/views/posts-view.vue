<script setup lang="ts">
import { authState } from '../lib/auth/authState';
import NewPostForm from '../components/new-post-form.vue';
import PostList from '../components/post-list.vue';
import { getPostsEndpoint, type GetPostTypes } from '../lib/network/enpoints/get-posts';
import { postPostsEndpoint, type PostPostTypes } from '../lib/network/enpoints/post-posts';
import { useSuperQuery, useSuperMutation } from '../lib/network/superFetch';


const { data: postsResult, loading, error, refetch }
  = useSuperQuery<GetPostTypes['Response']>(
    { ...getPostsEndpoint,
      options: {
        ...getPostsEndpoint.options,
        headers: {
          ...getPostsEndpoint.options?.headers,
          'Authorization': `Bearer ${authState.user?.token ?? localStorage.getItem('token')}`
        }
      }

     }
  );

const { mutate: createPost, mutating } = useSuperMutation<PostPostTypes['Request'], PostPostTypes['Response']>(
  {
    ...postPostsEndpoint,
    options: {
      ...postPostsEndpoint.options,
      headers: {
        ...postPostsEndpoint.options?.headers,
        'Authorization': `Bearer ${authState.user?.token ?? localStorage.getItem('token')}`
      }
    },
    onSuccess: refetch,
  }
);

const logout = () => {
  authState.isAuthenticated = false;
  authState.user = null;
  localStorage.removeItem('token');
}
</script>


<template>

  <div class="w-full flex flex-col items-start justify-center gap-8">
    <button
      class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
      @click="logout"
    >
      Logout
    </button>
    <NewPostForm :create-post="createPost" :mutating="mutating" />
    <PostList :posts="postsResult?.data ?? []" :loading="loading" :error="error" />
  </div>
</template>
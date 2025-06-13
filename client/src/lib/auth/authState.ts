import type { Auth } from "./types";

import { reactive } from "vue";

export const authState = reactive<Auth>({
  isAuthenticated: false,
  user: null,
});

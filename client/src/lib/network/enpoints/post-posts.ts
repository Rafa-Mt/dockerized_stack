import type { Endpoint } from "./types";
import { API_BASE_URL } from "./constants";
import type { Post } from "../../posts/types";

export const postPostsEndpoint: Endpoint = {
  url: `${API_BASE_URL}/posts/`,
  options: {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  },
};

export interface PostPostTypes {
  Request: {
    title: string;
    content: string;
  };
  Response: {
    message: string;
    data: Post[];
  };
}
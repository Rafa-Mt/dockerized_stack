import type { Endpoint } from "./types";
import { API_BASE_URL } from "./constants";
import type { Post } from "../../posts/types";

export const getPostsEndpoint: Endpoint = {
  url: `${API_BASE_URL}/posts/`,
  options: {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  },
};

export interface GetPostTypes {
  Request: {};
  Response: {
    message: string;
    data: Post[];
  };
}
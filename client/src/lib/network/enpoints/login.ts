import type { Endpoint } from "./types";
import { API_BASE_URL } from "./constants";

export const loginEndpoint: Endpoint = {
  url: `${API_BASE_URL}/auth/login`,
  options: {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  },
};

export interface LoginTypes {
  Request: {
    username: string;
    password: string;
  };
  Response: {
    message: string;
    token: string;
    data: {
      id: string;
      username: string;
      email: string;
    };
  };
}

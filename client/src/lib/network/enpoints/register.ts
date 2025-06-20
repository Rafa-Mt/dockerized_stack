import type { Endpoint } from "./types";
import { API_BASE_URL } from "./constants";

export const registerEndpoint: Endpoint = {
  url: `${API_BASE_URL}/auth/register`,
  options: {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  },
};

export interface RegisterTypes {
  Request: {
    email: string;
    username: string;
    password: string;
  };
  Response: {
    message: string;
    data: {
      id: string;
      username: string;
      email: string;
    };
    token: string; 
  };
}
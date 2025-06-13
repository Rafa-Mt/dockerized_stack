import type { Endpoint } from "./types";

export const loginEndpoint: Endpoint = {
  url: "/auth/login",
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
  }
  Response: {
    message: string;
    username: string;
  };
}
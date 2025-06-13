import type { Endpoint } from "./types";

export const registerEndpoint: Endpoint = {
  url: "/auth/register",
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
  };
}
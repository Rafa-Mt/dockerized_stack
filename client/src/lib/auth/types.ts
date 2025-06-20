export interface User {
  username: string;
  email: string;
  id: string;
  token?: string; // Optional token for authenticated requests
}

export interface Auth {
  isAuthenticated: boolean;
  user: User | null;
}
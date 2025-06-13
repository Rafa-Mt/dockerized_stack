export interface User {
  username: string;
}

export interface Auth {
  isAuthenticated: boolean;
  user: User | null;
}
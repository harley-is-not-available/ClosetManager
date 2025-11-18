export const LoadingStatus = {
  idle: "idle",
  loading: "loading",
  success: "success",
  error: "error",
  unloaded: "unloaded",
} as const;

export type LoadingStatusKey = "idle" | "loading" | "success" | "error" | "unloaded";

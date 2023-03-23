import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    open: true,
    proxy:
      process.env.PROXY_PORT !== undefined
        ? {
            "/api": `http://127.0.0.1:${Number(process.env.PROXY_PORT)}`,
          }
        : undefined,
  },
  optimizeDeps: {
    esbuildOptions: {
      target: "esnext",
    },
  },
  build: {
    target: "es2020",
  },
  plugins: [svelte()],
});

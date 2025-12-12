import type { Config } from "@react-router/dev/config";

export default {
  // Config options...
  // Server-side render by default, to enable SPA mode set this to `false`
  future: {
    v8_middleware: true
  },
  ssr: false,
} satisfies Config;

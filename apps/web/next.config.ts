import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Docker 빌드 최적화 (standalone 모드)
  output: "standalone",

  // 이미지 최적화
  images: {
    formats: ["image/avif", "image/webp"],
    minimumCacheTTL: 60,
  },

  // 압축 활성화
  compress: true,

  // 보안 헤더
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "origin-when-cross-origin" },
        ],
      },
    ];
  },

  // API 프록시 (개발 환경용)
  async rewrites() {
    const apiUrl = process.env.API_URL || "http://localhost:8000";
    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;

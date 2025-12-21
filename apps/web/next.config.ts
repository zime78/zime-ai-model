import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static Export for packaging
  output: "export",
  trailingSlash: true,

  // Image optimization

  // Image optimization
  images: {
    unoptimized: true, // Required for export
    formats: ["image/avif", "image/webp"],
    minimumCacheTTL: 60,
  },

  // Compression
  compress: true,
};

export default nextConfig;

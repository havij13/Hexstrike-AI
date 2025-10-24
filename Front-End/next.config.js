/** @type {import('next').NextConfig} */
const { i18n } = require('./next-i18next.config')

const nextConfig = {
  experimental: {
    appDir: true,
  },
  i18n,
  images: {
    domains: ['localhost', 'hexstrike-ai-v6-0.onrender.com'],
  },
  env: {
    HEXSTRIKE_API_URL: process.env.HEXSTRIKE_API_URL || 'https://hexstrike-ai-v6-0.onrender.com',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.HEXSTRIKE_API_URL || 'https://hexstrike-ai-v6-0.onrender.com'}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig

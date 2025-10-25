/** @type {import('next').NextConfig} */

const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
    domains: ['localhost', 'hexstrike-ai-v6-0.onrender.com'],
  },
  env: {
    HEXSTRIKE_API_URL: process.env.HEXSTRIKE_API_URL || 'https://hexstrike-ai-v6-0.onrender.com',
  },
}

module.exports = nextConfig

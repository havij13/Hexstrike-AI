# Deployment Guide

## Netlify Deployment

### Prerequisites
- Node.js 18+
- npm or yarn

### Build Configuration
The project is configured for static export to Netlify:

```toml
# netlify.toml
[build]
  publish = "out"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"
```

### Environment Variables
Set these in your Netlify dashboard:

```
NEXT_PUBLIC_HEXSTRIKE_API_URL=https://hexstrike-ai-v6-0.onrender.com
```

### Build Process
1. Install dependencies: `npm install`
2. Build the project: `npm run build`
3. Deploy to Netlify

### Troubleshooting

#### Common Issues:
1. **Missing Tailwind plugins**: Removed `@tailwindcss/forms` and `@tailwindcss/typography` dependencies
2. **Next.js config issues**: Updated to use `output: 'export'` for static hosting
3. **i18n configuration**: Removed i18n config for compatibility

#### Build Commands:
```bash
# Install dependencies
npm install

# Build for production
npm run build

# Start development server
npm run dev
```

### Features
- Static export compatible
- Optimized for Netlify hosting
- Cyberpunk-themed UI
- Real-time API integration
- Responsive design

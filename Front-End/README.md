# HexStrike AI Dashboard

A modern, cyberpunk-styled dashboard for the HexStrike AI penetration testing framework.

## Features

- **Real-time Monitoring**: Live system metrics and process monitoring
- **AI Intelligence**: Target analysis and tool selection
- **Security Tools**: Direct access to nmap, gobuster, and other tools
- **Process Management**: Monitor active scans and operations
- **Cyberpunk UI**: Modern, neon-themed interface with animations
- **Internationalization**: Multi-language support (EN, ZH, JA, KO)

## Technology Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom cyberpunk theme
- **State Management**: React Query for API state
- **Icons**: Lucide React
- **Animations**: Framer Motion

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- HexStrike AI server running

### Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Set environment variables:
```bash
cp .env.example .env.local
```

3. Update the API URL in `.env.local`:
```
NEXT_PUBLIC_HEXSTRIKE_API_URL=https://hexstrike-ai-v6-0.onrender.com
```

4. Run the development server:
```bash
npm run dev
# or
yarn dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── globals.css     # Global styles
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── providers.tsx   # Context providers
├── components/         # React components
│   ├── Dashboard.tsx   # Main dashboard
│   ├── Header.tsx      # Top navigation
│   ├── Sidebar.tsx     # Side navigation
│   └── ...             # Other components
├── lib/               # Utilities and configurations
│   └── api.ts         # API client
├── types/             # TypeScript type definitions
│   └── api.ts         # API response types
└── utils/             # Helper functions
```

## API Integration

The dashboard connects to the HexStrike AI server via REST API. All API calls are handled through the `apiClient` in `src/lib/api.ts`.

### Available Endpoints

- **Health Check**: `/health`
- **Telemetry**: `/api/telemetry`
- **Process Management**: `/api/processes/*`
- **AI Intelligence**: `/api/intelligence/*`
- **Security Tools**: `/api/tools/*`
- **Cache Management**: `/api/cache/*`

## Customization

### Themes

The cyberpunk theme is defined in `tailwind.config.js`. You can customize:

- Colors: Modify the `cyber` and `neon` color palettes
- Animations: Adjust the custom keyframes and animations
- Typography: Change font families and sizes

### Components

All components are modular and can be customized independently. Each component has its own styling and can be easily modified.

## Deployment

### Netlify

1. Build the project:
```bash
npm run build
```

2. Deploy to Netlify with the following settings:
   - Build command: `npm run build`
   - Publish directory: `out`
   - Environment variables: Set `NEXT_PUBLIC_HEXSTRIKE_API_URL`

### Vercel

1. Connect your repository to Vercel
2. Set environment variables in the Vercel dashboard
3. Deploy automatically on push

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Code Style

- Use TypeScript for all components
- Follow the existing component structure
- Use Tailwind CSS for styling
- Implement proper error handling
- Add loading states for async operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the HexStrike AI framework.

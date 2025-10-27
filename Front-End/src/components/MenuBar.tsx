import React, { useState } from 'react';
import Link from 'next/link';
import { Menu, X, ChevronDown, ChevronUp, Home, Globe, Shield, Key, Cpu, Cloud, Zap, Search } from 'lucide-react';

interface MenuCategory {
  label: string;
  icon: React.ReactNode;
  links: { label: string; href: string }[];
}

const menuData: MenuCategory[] = [
  {
    label: 'Home',
    icon: <Home size={18} />,
    links: [
      { label: 'Dashboard', href: '/' },
    ]
  },
  {
    label: 'Network Reconnaissance',
    icon: <Globe size={18} />,
    links: [
      { label: 'Nmap', href: '/tools/network/nmap' },
      { label: 'Rustscan', href: '/tools/network/rustscan' },
      { label: 'Masscan', href: '/tools/network/masscan' },
      { label: 'Amass', href: '/tools/network/amass' },
      { label: 'Subfinder', href: '/tools/network/subfinder' },
      { label: 'Fierce', href: '/tools/network/fierce' },
      { label: 'DNSenum', href: '/tools/network/dnsenum' },
      { label: 'AutoRecon', href: '/tools/network/autorecon' },
      { label: 'Enum4linux', href: '/tools/network/enum4linux' },
      { label: 'Responder', href: '/tools/network/responder' },
      { label: 'RPCClient', href: '/tools/network/rpcclient' },
      { label: 'NBtscan', href: '/tools/network/nbtscan' },
      { label: 'ARP-Scan', href: '/tools/network/arp-scan' },
      { label: 'SMBmap', href: '/tools/network/smbmap' },
      { label: 'Enum4linux-ng', href: '/tools/network/enum4linux-ng' },
      { label: 'Nmap-Advanced', href: '/tools/network/nmap-advanced' }
    ],
  },
  {
    label: 'Web Security',
    icon: <Shield size={18} />,
    links: [
      { label: 'Gobuster', href: '/tools/web/gobuster' },
      { label: 'Feroxbuster', href: '/tools/web/feroxbuster' },
      { label: 'Nuclei', href: '/tools/web/nuclei' },
      { label: 'FFuf', href: '/tools/web/ffuf' },
      { label: 'Nikto', href: '/tools/web/nikto' },
      { label: 'SQLMap', href: '/tools/web/sqlmap' },
      { label: 'WPScan', href: '/tools/web/wpscan' },
      { label: 'Dalfox', href: '/tools/web/dalfox' },
      { label: 'Dirb', href: '/tools/web/dirb' },
      { label: 'Dirsearch', href: '/tools/web/dirsearch' },
      { label: 'Katana', href: '/tools/web/katana' },
      { label: 'GAU', href: '/tools/web/gau' },
      { label: 'Waybackurls', href: '/tools/web/waybackurls' },
      { label: 'Arjun', href: '/tools/web/arjun' },
      { label: 'ParamSpider', href: '/tools/web/paramspider' },
      { label: 'HTTPx', href: '/tools/web/httpx' },
      { label: 'Anew', href: '/tools/web/anew' },
      { label: 'QSReplace', href: '/tools/web/qsreplace' },
      { label: 'Uro', href: '/tools/web/uro' },
      { label: 'Jaeles', href: '/tools/web/jaeles' },
      { label: 'Hakrawler', href: '/tools/web/hakrawler' },
      { label: 'DotDotPwn', href: '/tools/web/dotdotpwn' },
      { label: 'XSSer', href: '/tools/web/xsser' },
      { label: 'WFuzz', href: '/tools/web/wfuzz' },
      { label: 'WafW00f', href: '/tools/web/wafw00f' },
      { label: 'Burpsuite-Alternative', href: '/tools/web/burpsuite-alternative' },
      { label: 'ZAP', href: '/tools/web/zap' },
      { label: 'HTTP-Framework', href: '/tools/web/http-framework' },
      { label: 'Browser-Agent', href: '/tools/web/browser-agent' },
      { label: 'API-Fuzzer', href: '/tools/web/api-fuzzer' },
      { label: 'GraphQL-Scanner', href: '/tools/web/graphql-scanner' },
      { label: 'JWT-Analyzer', href: '/tools/web/jwt-analyzer' },
      { label: 'API-Schema-Analyzer', href: '/tools/web/api-schema-analyzer' },
      { label: 'X8', href: '/tools/web/x8' }
    ]
  },
  {
    label: 'Authentication & Password',
    icon: <Key size={18} />,
    links: [
      { label: 'Hydra', href: '/tools/auth/hydra' },
      { label: 'John', href: '/tools/auth/john' },
      { label: 'Hashcat', href: '/tools/auth/hashcat' },
      { label: 'Medusa', href: '/tools/auth/medusa' },
      { label: 'NetExec', href: '/tools/auth/netexec' }
    ]
  },
  {
    label: 'Binary Analysis',
    icon: <Cpu size={18} />,
    links: [
      { label: 'Ghidra', href: '/tools/binary/ghidra' },
      { label: 'Radare2', href: '/tools/binary/radare2' },
      { label: 'GDB', href: '/tools/binary/gdb' },
      { label: 'Binwalk', href: '/tools/binary/binwalk' },
      { label: 'Checksec', href: '/tools/binary/checksec' },
      { label: 'ROPGadget', href: '/tools/binary/ropgadget' },
      { label: 'XXD', href: '/tools/binary/xxd' },
      { label: 'Strings', href: '/tools/binary/strings' },
      { label: 'Objdump', href: '/tools/binary/objdump' },
      { label: 'Pwntools', href: '/tools/binary/pwntools' },
      { label: 'One-Gadget', href: '/tools/binary/one-gadget' },
      { label: 'Libc-Database', href: '/tools/binary/libc-database' },
      { label: 'GDB-PEDA', href: '/tools/binary/gdb-peda' },
      { label: 'Angr', href: '/tools/binary/angr' },
      { label: 'Ropper', href: '/tools/binary/ropper' },
      { label: 'PwnInit', href: '/tools/binary/pwninit' }
    ]
  },
  {
    label: 'Exploitation',
    icon: <Zap size={18} />,
    links: [
      { label: 'Metasploit', href: '/tools/exploitation/metasploit' },
      { label: 'MSFVenom', href: '/tools/exploitation/msfvenom' }
    ]
  },
  {
    label: 'Forensics',
    icon: <Search size={18} />,
    links: [
      { label: 'Volatility', href: '/tools/forensics/volatility' },
      { label: 'Volatility3', href: '/tools/forensics/volatility3' },
      { label: 'Foremost', href: '/tools/forensics/foremost' },
      { label: 'StegHide', href: '/tools/forensics/steghide' },
      { label: 'ExifTool', href: '/tools/forensics/exiftool' },
      { label: 'HashPump', href: '/tools/forensics/hashpump' }
    ]
  },
  {
    label: 'Cloud Security',
    icon: <Cloud size={18} />,
    links: [
      { label: 'Prowler', href: '/tools/cloud/prowler' },
      { label: 'Trivy', href: '/tools/cloud/trivy' },
      { label: 'Kube-Hunter', href: '/tools/cloud/kube-hunter' },
      { label: 'Scout-Suite', href: '/tools/cloud/scout-suite' },
      { label: 'CloudMapper', href: '/tools/cloud/cloudmapper' },
      { label: 'Pacu', href: '/tools/cloud/pacu' },
      { label: 'Kube-Bench', href: '/tools/cloud/kube-bench' },
      { label: 'Docker-Bench-Security', href: '/tools/cloud/docker-bench-security' },
      { label: 'Clair', href: '/tools/cloud/clair' },
      { label: 'Falco', href: '/tools/cloud/falco' },
      { label: 'Checkov', href: '/tools/cloud/checkov' },
      { label: 'Terrascan', href: '/tools/cloud/terrascan' }
    ]
  }
];

export const MenuBar: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState<number | null>(null);

  // Responsive handlers
  const handleToggle = () => setOpen(!open);
  const handleCategoryClick = (i: number) => setExpanded(expanded === i ? null : i);

  return (
    <>
      {/* Mobile Menu Toggle */}
      <div className="md:hidden fixed z-50 left-4 top-4">
        <button
          aria-label={open ? "Close menu" : "Open menu"}
          className="text-neon-blue bg-cyber-dark rounded-lg p-2 focus:outline-none shadow-lg border-2 border-cyber-light"
          onClick={handleToggle}
        >
          {open ? <X size={26} /> : <Menu size={26} />}
        </button>
      </div>
      {/* Actual Menu */}
      <aside
        className={`
          fixed z-40 bg-gradient-to-b from-cyber-dark to-cyber-base/90 text-cyber-light 
          shadow-2xl border-r-2 border-cyber-primary
          h-screen top-0 transition-all duration-300
          flex flex-col
          w-72
          max-w-[90vw]
          px-3 py-6
          font-mono
          ${open ? 'translate-x-0' : '-translate-x-full'}
          md:translate-x-0 md:static md:w-56 md:h-auto md:shadow-none md:border-r
        `}
        style={{ minHeight: "100vh" }}
      >
        <div className="mb-6 flex items-center space-x-2 pl-1">
          <span className="font-cyber text-neon-blue text-2xl neon-glow select-none">HexStrike&nbsp;AI</span>
        </div>
        <nav>
          <ul className="space-y-1">
            {menuData.map((cat, i) => (
              <li key={cat.label}>
                <button
                  className={`w-full flex items-center px-2 py-2 rounded-lg text-cyber-light hover:text-neon-pink hover:bg-cyber-lighter transition-all
                    ${expanded === i ? 'bg-cyber-blue/10' : ''}
                  `}
                  onClick={() => handleCategoryClick(i)}
                  aria-expanded={expanded === i}
                  aria-controls={`menu-cat-${i}`}
                  tabIndex={0}
                  style={{ fontWeight: expanded === i ? 'bold' as any : 'normal' }}
                  >
                  <span className="mr-3">{cat.icon}</span>
                  <span className="flex-1 text-left">{cat.label}</span>
                  <span>
                    {cat.links.length > 1 ? (
                      expanded === i ? <ChevronUp size={18} /> : <ChevronDown size={18} />
                    ) : null}
                  </span>
                </button>
                {/* Collapsed/Expanded Links */}
                <ul
                  id={`menu-cat-${i}`}
                  className={`
                    transition-all duration-200 ml-8 border-l border-cyber-blue/40
                    ${expanded === i ? 'max-h-[800px] py-2 opacity-100 visible' : 'max-h-0 overflow-hidden opacity-0'}
                  `}
                >
                  {cat.links.map(link => (
                    <li key={link.href}>
                      <Link
                        href={link.href}
                        className="block px-2 py-1 rounded text-cyber-light hover:text-neon-blue hover:bg-cyber-lighter transition-all"
                        onClick={() => setOpen(false)}
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </nav>
        <div className="flex-1" />
        <div className="pt-10 text-xs text-cyber-light/70 px-1">
          &copy; {new Date().getFullYear()} HexStrike AI
        </div>
      </aside>
      {/* Overlay for mobile */}
      {open && (
        <div
          className="fixed inset-0 z-30 bg-black bg-opacity-50 md:hidden"
          onClick={handleToggle}
          aria-label="Close menu overlay"
        />
      )}
      {/* Add margin for page content */}
      <style jsx global>{`
        @media (min-width: 768px) {
          body {
            margin-left: 14rem;
          }
        }
      `}</style>
    </>
  );
};


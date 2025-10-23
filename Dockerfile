FROM kalilinux/kali-last-release:latest

# 設定環境變數
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    HEXSTRIKE_PORT=8888 \
    HEXSTRIKE_HOST=0.0.0.0

# 更新系統並安裝核心安全工具包
RUN apt-get update && apt-get upgrade -y && apt-get install -y --fix-missing \
    # 網路掃描與偵察工具
    nmap \
    amass \
    subfinder \
    fierce \
    dnsenum \
    theharvester \
    enum4linux-ng \
    # Web 應用程式安全測試工具
    gobuster \
    feroxbuster \
    ffuf \
    dirb \
    dirsearch \
    nuclei \
    nikto \
    sqlmap \
    wpscan \
    arjun \
    httpx-toolkit \
    wafw00f \
    # 密碼破解與認證工具
    hydra \
    john \
    hashcat \
    medusa \
    evil-winrm \
    # 二進制分析與逆向工程工具
    radare2 \
    ghidra \
    binwalk \
    gdb \
    gdb-peda \
    checksec \
    binutils \
    # 取證與 CTF 工具
    foremost \
    steghide \
    exiftool \
    autopsy \
    sleuthkit \
    # Python 與瀏覽器自動化
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    chromium \
    chromium-driver \
    # 系統工具
    git \
    curl \
    wget \
    unzip \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安裝額外的 Go 基礎工具（部分工具需要）
RUN apt-get update && apt-get install -y golang-go && apt-get clean

# 安裝 pwntools 相關工具
RUN apt-get update && apt-get install -y \
    python3-pwntools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製 Python 依賴檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel --break-system-packages && \
    pip3 install --no-cache-dir -r requirements.txt --break-system-packages --ignore-installed

# 複製專案檔案
COPY hexstrike_server.py hexstrike_mcp.py ./
COPY assets/ ./assets/

# 建立日誌目錄
RUN mkdir -p /app/logs

# 複製並設定啟動腳本
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 暴露 API 端口
EXPOSE 8888

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8888/health || exit 1

# 使用非 root 用戶運行（安全考量）
RUN useradd -m -u 1000 hexstrike && \
    chown -R hexstrike:hexstrike /app
USER hexstrike

# 啟動服務
ENTRYPOINT ["/docker-entrypoint.sh"]




#!/bin/bash
# HexStrike AI v6.0 - Docker 部署測試腳本

set -e

HEXSTRIKE_URL="${HEXSTRIKE_URL:-http://localhost:8888}"

echo "============================================================================"
echo "🧪 HexStrike AI Docker 部署測試"
echo "============================================================================"
echo "測試目標: $HEXSTRIKE_URL"
echo "時間: $(date)"
echo "============================================================================"
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 測試計數器
TESTS_PASSED=0
TESTS_FAILED=0

# 測試函數
test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local expected_status="${3:-200}"
    
    echo -n "Testing $name... "
    
    if response=$(curl -s -o /dev/null -w "%{http_code}" "$HEXSTRIKE_URL$endpoint" 2>&1); then
        if [ "$response" = "$expected_status" ]; then
            echo -e "${GREEN}✅ PASS${NC} (HTTP $response)"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}❌ FAIL${NC} (Expected HTTP $expected_status, got $response)"
            ((TESTS_FAILED++))
        fi
    else
        echo -e "${RED}❌ FAIL${NC} (Connection error)"
        ((TESTS_FAILED++))
    fi
}

# 測試 JSON 回應
test_json_response() {
    local name="$1"
    local endpoint="$2"
    local json_key="$3"
    
    echo -n "Testing $name... "
    
    if response=$(curl -s "$HEXSTRIKE_URL$endpoint" 2>&1); then
        if echo "$response" | grep -q "\"$json_key\""; then
            echo -e "${GREEN}✅ PASS${NC} (Found key: $json_key)"
            ((TESTS_PASSED++))
            
            # 顯示回應摘要
            if command -v jq &> /dev/null; then
                echo "   Response: $(echo "$response" | jq -c .)"
            fi
        else
            echo -e "${RED}❌ FAIL${NC} (Key '$json_key' not found)"
            echo "   Response: $response"
            ((TESTS_FAILED++))
        fi
    else
        echo -e "${RED}❌ FAIL${NC} (Connection error)"
        ((TESTS_FAILED++))
    fi
}

echo "開始測試 HexStrike AI API..."
echo ""

# 1. 測試健康檢查端點
test_json_response "Health Check" "/health" "status"

# 2. 測試基礎端點可達性
test_endpoint "Telemetry Endpoint" "/api/telemetry"

# 3. 測試快取統計
test_endpoint "Cache Stats" "/api/cache/stats"

# 4. 測試處理程序列表
test_endpoint "Process List" "/api/processes/list"

# 5. 測試根端點 (可能返回 404 或其他)
echo -n "Testing Root Endpoint... "
if curl -s "$HEXSTRIKE_URL/" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Server Responding${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠️  No response (this may be normal)${NC}"
fi

echo ""
echo "============================================================================"
echo "測試結果總結"
echo "============================================================================"
echo -e "${GREEN}✅ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Failed: $TESTS_FAILED${NC}"
echo "============================================================================"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有測試通過！HexStrike AI 運行正常。${NC}"
    exit 0
else
    echo -e "${RED}⚠️  部分測試失敗。請檢查伺服器日誌。${NC}"
    echo ""
    echo "除錯建議："
    echo "  1. 檢查容器是否運行: docker ps"
    echo "  2. 查看日誌: docker logs hexstrike"
    echo "  3. 確認 port mapping: docker port hexstrike"
    exit 1
fi


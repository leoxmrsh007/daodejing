#!/bin/bash
# 道德经自动部署脚本
# 自动完成Git推送和Vercel部署

set -e

echo "🚀 开始自动部署流程..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Git 状态
echo -e "${YELLOW}📋 检查 Git 状态...${NC}"
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}📝 发现未提交的更改，正在提交...${NC}"
    git add -A
    git commit -m "deploy: 自动部署到 daodejing0.online - $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${GREEN}✅ 代码已提交${NC}"
else
    echo -e "${GREEN}✅ 没有未提交的更改${NC}"
fi

# 推送到 GitHub
echo -e "${YELLOW}📤 推送到 GitHub...${NC}"
if git push origin main; then
    echo -e "${GREEN}✅ 代码已推送到 GitHub${NC}"
else
    echo -e "${RED}❌ 推送失败，请检查网络连接或Git配置${NC}"
    echo -e "${YELLOW}💡 提示: 如果是认证问题，请运行: gh auth login${NC}"
    exit 1
fi

# 检查 Vercel CLI
echo -e "${YELLOW}🔍 检查 Vercel CLI...${NC}"
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}📦 安装 Vercel CLI...${NC}"
    npm install -g vercel
fi
echo -e "${GREEN}✅ Vercel CLI 已就绪${NC}"

# 检查 Vercel 登录状态
echo -e "${YELLOW}🔐 检查 Vercel 登录状态...${NC}"
if ! vercel whoami &> /dev/null; then
    echo -e "${YELLOW}🔑 需要登录 Vercel...${NC}"
    echo -e "${YELLOW}   请在浏览器中完成登录${NC}"
    vercel login
fi
echo -e "${GREEN}✅ Vercel 已登录${NC}"

# 部署到 Vercel
echo -e "${YELLOW}🚀 部署到 Vercel...${NC}"
if vercel --prod; then
    echo -e "${GREEN}✅ 部署成功!${NC}"
else
    echo -e "${RED}❌ 部署失败${NC}"
    exit 1
fi

# 配置自定义域名
echo -e "${YELLOW}🌐 配置自定义域名: www.daodejing0.online${NC}"
vercel domains add www.daodejing0.online || echo -e "${YELLOW}⚠️  域名可能已配置或需要手动设置${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 部署流程完成!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}下一步操作:${NC}"
echo -e "1. 访问 Vercel Dashboard: https://vercel.com/dashboard"
echo -e "2. 在项目设置中添加域名: www.daodejing0.online"
echo -e "3. 在域名提供商处添加 DNS 记录:"
echo -e "   - CNAME: www -> cname.vercel-dns.com"
echo -e "   - A: @ -> 76.76.21.21"
echo ""
echo -e "${GREEN}网站地址:${NC}"
echo -e "   https://www.daodejing0.online"
echo ""

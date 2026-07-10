#!/bin/bash
set -e

echo "=========================================="
echo "  F5 设备管理平台 - Ubuntu 24.04 一键部署脚本"
echo "=========================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

info "检查系统版本..."
if ! cat /etc/os-release | grep -q "Ubuntu 24.04"; then
    warn "检测到非 Ubuntu 24.04 系统，脚本可能无法正常运行"
fi

info "检查 Docker 是否已安装..."
if ! command -v docker &> /dev/null; then
    error "Docker 未安装，请先安装 Docker"
    exit 1
else
    info "Docker 版本: $(docker --version)"
    success "Docker 已安装"
fi

info "检测 Docker Compose 命令..."
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
    info "使用 Docker Compose V1: $(docker-compose --version)"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
    info "使用 Docker Compose V2: $(docker compose version)"
else
    error "Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi
success "Docker Compose 已安装"

info "检查 Docker 服务状态..."
if ! systemctl is-active --quiet docker; then
    info "启动 Docker 服务..."
    systemctl start docker
    systemctl enable docker
fi
success "Docker 服务运行正常"

DEPLOY_DIR=$(dirname "$(readlink -f "$0")")/..
DEPLOY_DIR=$(realpath "$DEPLOY_DIR")
info "项目根目录: $DEPLOY_DIR"

if [ ! -f "$DEPLOY_DIR/deploy/docker-compose.yml" ]; then
    error "未找到项目文件，请确保脚本在项目的 deploy 目录下运行"
    exit 1
fi

info "配置环境变量..."

read -p "请输入 SECRET_KEY（用于 JWT 签名，建议使用长随机字符串）: " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(openssl rand -hex 32)
    info "未输入，自动生成 SECRET_KEY: $SECRET_KEY"
fi

read -p "请输入 MySQL 密码: " MYSQL_PASSWORD
if [ -z "$MYSQL_PASSWORD" ]; then
    MYSQL_PASSWORD="root"
    warn "未输入，使用默认密码: root"
fi

info "生成 .env 文件..."
cd $DEPLOY_DIR/deploy

cat > .env << EOF
SECRET_KEY=$SECRET_KEY
MYSQL_ROOT_PASSWORD=$MYSQL_PASSWORD
DATABASE_URL=mysql+pymysql://root:$MYSQL_PASSWORD@mysql:3306/f5_platform
EOF

info "检查是否有失败的构建缓存..."
if $COMPOSE_CMD ps 2>/dev/null | grep -q "deploy-frontend\|deploy-backend"; then
    info "检测到已有容器，尝试停止并清理..."
    $COMPOSE_CMD down --remove-orphans 2>/dev/null || true
fi

info "清理失败的构建缓存..."
docker builder prune -f 2>/dev/null || true

info "启动服务..."
$COMPOSE_CMD up -d --build

info "等待服务启动..."
sleep 30

info "检查服务状态..."
$COMPOSE_CMD ps

info "验证服务..."

FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
if [ "$FRONTEND_STATUS" = "200" ]; then
    success "前端服务正常"
else
    warn "前端服务可能未就绪，HTTP状态码: $FRONTEND_STATUS"
    warn "请等待几秒后重新检查，首次启动需要构建镜像和初始化数据库"
fi

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "访问地址:"
echo "  前端: http://$(curl -s ifconfig.me)"
echo ""
echo "管理命令:"
echo "  查看日志: $COMPOSE_CMD logs -f"
echo "  停止服务: $COMPOSE_CMD down"
echo "  重启服务: $COMPOSE_CMD restart"
echo "  更新部署: cd $DEPLOY_DIR && git pull && $COMPOSE_CMD up -d --build"
echo ""
echo "防火墙配置建议（UFW）:"
echo "  sudo ufw allow 80/tcp"
echo "  sudo ufw allow 443/tcp"
echo "  sudo ufw enable"
echo ""
echo "注意事项:"
echo "  1. 首次启动需要等待数据库初始化完成，可能需要1-2分钟"
echo "  2. 生产环境请配置防火墙规则，只开放必要端口"
echo "  3. 建议配置 HTTPS（可使用 Nginx 或 Let's Encrypt）"
echo "  4. 默认管理员账号：admin / admin"
echo "=========================================="
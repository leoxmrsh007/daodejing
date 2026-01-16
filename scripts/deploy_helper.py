#!/usr/bin/env python3
"""
通用部署配置生成器
支持 Flask、静态站点等多种项目类型
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ProjectType:
    FLASK = "flask"
    DJANGO = "django"
    STATIC = "static"
    NEXT_JS = "nextjs"
    VITE = "vite"
    UNKNOWN = "unknown"


class DeployConfigGenerator:
    """部署配置生成器"""

    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir).resolve()
        self.project_type = ProjectType.UNKNOWN
        self.config = {}

    def detect_project_type(self) -> str:
        """检测项目类型"""
        py_files = list(self.project_dir.glob("*.py"))
        has_flask = any(
            "flask" in f.read_text(encoding="utf-8", errors="ignore").lower()
            for f in py_files[:20]  # 限制检查文件数量
        )
        has_app_py = (self.project_dir / "app.py").exists()
        has_wsgi_py = (self.project_dir / "wsgi.py").exists()
        has_manage_py = (self.project_dir / "manage.py").exists()
        has_index_html = (self.project_dir / "index.html").exists()
        has_dist = (self.project_dir / "dist").exists()
        has_next_config = (self.project_dir / "next.config.js").exists()
        has_vite_config = (self.project_dir / "vite.config.js").exists()

        if has_manage_py and (self.project_dir / "settings.py").exists():
            self.project_type = ProjectType.DJANGO
        elif has_app_py and has_flask:
            self.project_type = ProjectType.FLASK
        elif has_wsgi_py and has_flask:
            self.project_type = ProjectType.FLASK
        elif has_next_config:
            self.project_type = ProjectType.NEXT_JS
        elif has_vite_config:
            self.project_type = ProjectType.VITE
        elif has_index_html or has_dist:
            self.project_type = ProjectType.STATIC

        return self.project_type

    def generate_vercel_config(self) -> Dict:
        """生成 Vercel 配置"""
        ptype = self.detect_project_type()

        if ptype == ProjectType.FLASK:
            return {
                "version": 2,
                "builds": [
                    {
                        "src": "app.py" if (self.project_dir / "app.py").exists() else "wsgi.py",
                        "use": "@vercel/python"
                    }
                ],
                "rewrites": [
                    {
                        "source": "/(.*)",
                        "destination": "/app.py" if (self.project_dir / "app.py").exists() else "/wsgi.py"
                    }
                ],
                "headers": [
                    {
                        "source": "/static/(.*)",
                        "headers": [
                            {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
                        ]
                    }
                ]
            }

        elif ptype == ProjectType.DJANGO:
            return {
                "version": 2,
                "builds": [
                    {
                        "src": "manage.py",
                        "use": "@vercel/python"
                    }
                ],
                "routes": [
                    {
                        "src": "/static/(.*)",
                        "dest": "/static/$1"
                    },
                    {
                        "src": "/media/(.*)",
                        "dest": "/media/$1"
                    },
                    {
                        "src": "/(.*)",
                        "dest": "/manage.py"
                    }
                ]
            }

        elif ptype == ProjectType.STATIC:
            # 检查是否有 dist 目录
            if (self.project_dir / "dist").exists():
                return {
                    "version": 2,
                    "public": True,
                    "rewrites": [
                        {
                            "source": "/(.*)",
                            "destination": "/dist/$1"
                        }
                    ]
                }
            return {
                "version": 2,
                "public": True
            }

        elif ptype == ProjectType.NEXT_JS:
            return {
                "version": 2,
                "buildCommand": "npm run build",
                "outputDirectory": ".next"
            }

        elif ptype == ProjectType.VITE:
            return {
                "version": 2,
                "buildCommand": "npm run build",
                "outputDirectory": "dist"
            }

        return {"version": 2}

    def generate_requirements_txt(self) -> Optional[str]:
        """生成 requirements.txt 内容"""
        ptype = self.detect_project_type()

        if ptype == ProjectType.FLASK:
            return "flask>=2.3.0\ncors>=1.0.1\nrequests>=2.31.0\n"

        elif ptype == ProjectType.DJANGO:
            return "django>=4.2.0\nwhitenoise>=6.5.0\ngunicorn>=21.0.0\n"

        return None

    def generate_netlify_toml(self) -> Optional[str]:
        """生成 netlify.toml 内容"""
        ptype = self.detect_project_type()

        if ptype == ProjectType.FLASK:
            return '''[build]
  command = "pip install -r requirements.txt"

[build.environment]
  PYTHON_VERSION = "3.9"

[[redirects]]
  from = "/*"
  to = "/app.py"
  status = 200
'''

        elif ptype == ProjectType.STATIC:
            return '''[build]
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
'''

        return None

    def write_config_files(self, dry_run: bool = False) -> List[str]:
        """写入配置文件，返回写入的文件列表"""
        written = []

        # 生成 vercel.json
        vercel_config = self.generate_vercel_config()
        vercel_path = self.project_dir / "vercel.json"

        if not dry_run:
            with open(vercel_path, "w", encoding="utf-8") as f:
                json.dump(vercel_config, f, indent=2, ensure_ascii=False)
            written.append("vercel.json")
        else:
            print(f"[DRY RUN] Would write vercel.json:")
            print(json.dumps(vercel_config, indent=2, ensure_ascii=False))

        # 生成 requirements.txt
        requirements = self.generate_requirements_txt()
        if requirements:
            req_path = self.project_dir / "requirements.txt"
            if not dry_run:
                with open(req_path, "w", encoding="utf-8") as f:
                    f.write(requirements)
                written.append("requirements.txt")
            else:
                print(f"[DRY RUN] Would write requirements.txt:")
                print(requirements)

        # 生成 netlify.toml
        netlify_config = self.generate_netlify_toml()
        if netlify_config:
            netlify_path = self.project_dir / "netlify.toml"
            if not dry_run:
                with open(netlify_path, "w", encoding="utf-8") as f:
                    f.write(netlify_config)
                written.append("netlify.toml")
            else:
                print(f"[DRY RUN] Would write netlify.toml:")
                print(netlify_config)

        return written

    def get_deployment_instructions(self) -> str:
        """获取部署指导"""
        ptype = self.detect_project_type()
        instructions = [f"## 检测到的项目类型: {ptype}\n"]

        if ptype == ProjectType.FLASK:
            instructions.append("""
### Vercel 部署

1. 安装 Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. 登录并部署:
   ```bash
   vercel login
   vercel prod
   ```

3. 配置自定义域名（可选）:
   ```bash
   vercel alias set <deployment-url> your-domain.com
   ```
""")
            instructions.append("""
### GitHub 自动部署

1. 推送代码到 GitHub
2. 在 Vercel Dashboard 导入仓库
3. Vercel 自动检测 Python 并部署
""")
            instructions.append("""
### 环境变量建议

- `FLASK_ENV=production`
- `SECRET_KEY` (生成: `python -c "import secrets; print(secrets.token_hex(32))"`)

""")

        elif ptype == ProjectType.DJANGO:
            instructions.append("""
### Vercel 部署 (Django)

1. 确保已安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 配置 Vercel (需要 vercel.json)
   ```bash
   vercel prod
   ```

3. 注意 Django 需要额外的:
   - ALLOWED_HOSTS 配置
   - 静态文件处理 (whitenoise)
""")
            instructions.append("""
### 推荐的 Django 生产配置

```python
# settings.py
ALLOWED_HOSTS = ['*']  # 生产环境应限制为具体域名

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... 其他 middleware
]
```

""")

        elif ptype == ProjectType.STATIC:
            instructions.append("""
### 静态站点部署选项

#### Vercel
```bash
vercel --prod
```

#### Netlify
```bash
# 拖拽 dist/ 目录到 https://app.netlify.com/drop
# 或使用 CLI
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

#### GitHub Pages
```bash
git checkout -b gh-pages
cp -r dist/* .
git add . && git commit -m "Deploy"
git push origin gh-pages
```

""")

        elif ptype == ProjectType.NEXT_JS:
            instructions.append("""
### Next.js 部署

#### Vercel (推荐)
```bash
vercel --prod
```

#### 其他平台
```bash
npm run build
# 上传 .next 目录
```

""")

        elif ptype == ProjectType.VITE:
            instructions.append("""
### Vite 项目部署

#### Vercel
```bash
npm run build
vercel --prod
```

#### Netlify
```bash
npm run build
netlify deploy --prod --dir=dist
```

""")

        else:
            instructions.append("""
### 未知项目类型

请手动配置部署。支持的类型:
- Flask (app.py + flask 导入)
- Django (manage.py)
- 静态站点 (index.html 或 dist/)
- Next.js (next.config.js)
- Vite (vite.config.js)

""")

        return "".join(instructions)

    def check_issues(self) -> List[str]:
        """检查项目配置问题"""
        issues = []
        ptype = self.detect_project_type()

        # 检查 common issues
        if ptype == ProjectType.FLASK:
            if not (self.project_dir / "requirements.txt").exists():
                issues.append("缺少 requirements.txt 文件")
            if not (self.project_dir / "app.py").exists() and not (self.project_dir / "wsgi.py").exists():
                issues.append("Flask 项目缺少 app.py 或 wsgi.py 入口文件")

        elif ptype == ProjectType.STATIC:
            if (self.project_dir / "dist").exists():
                if not (self.project_dir / "dist" / "index.html").exists():
                    issues.append("dist/ 目录存在但缺少 index.html")

        # 检查 vercel.json 问题
        if (self.project_dir / "vercel.json").exists():
            try:
                with open(self.project_dir / "vercel.json", encoding="utf-8") as f:
                    config = json.load(f)
                    if "rewrites" in config and not config["rewrites"]:
                        issues.append("vercel.json 中 rewrites 为空，可能导致路由问题")
            except json.JSONDecodeError:
                issues.append("vercel.json 不是有效的 JSON 格式")

        return issues


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Web 项目部署配置生成器")
    parser.add_argument("--dir", "-d", default=".", help="项目目录 (默认: 当前目录)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="不写入文件，只显示")
    parser.add_argument("--type", "-t", action="store_true", help="只检测项目类型")
    parser.add_argument("--instructions", "-i", action="store_true", help="显示部署指导")
    parser.add_argument("--check", "-c", action="store_true", help="检查配置问题")
    parser.add_argument("--write", "-w", action="store_true", help="写入配置文件")

    args = parser.parse_args()

    generator = DeployConfigGenerator(args.dir)

    if args.type:
        print(f"项目类型: {generator.detect_project_type()}")
        return

    if args.instructions:
        print(generator.get_deployment_instructions())
        return

    if args.check:
        issues = generator.check_issues()
        if issues:
            print("发现的问题:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("未发现配置问题")
        return

    if args.write:
        written = generator.write_config_files(dry_run=args.dry_run)
        if args.dry_run:
            print("\n[DRY RUN] 未写入任何文件")
        else:
            print(f"已写入文件: {', '.join(written)}")
        return

    # 默认：显示摘要
    ptype = generator.detect_project_type()
    print(f"项目类型: {ptype}")

    issues = generator.check_issues()
    if issues:
        print("\n发现的问题:")
        for issue in issues:
            print(f"  - {issue}")

    print("\n要生成配置文件，运行:")
    print(f"  python {__file__} --write --dir {args.dir}")


if __name__ == "__main__":
    main()

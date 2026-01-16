# Deploy Skill

通用 Web 项目部署辅助技能，支持 Flask、静态站点等多种项目类型的部署配置生成和指导。

## 使用方法

在 Claude Code 中调用：
```
/deploy
```

或输入部署相关需求：
```
"帮我部署这个项目"
"生成 Vercel 配置"
"这个项目怎么部署？"
```

## 功能特性

- 自动检测项目类型（Flask/Django/静态站点/Next.js）
- 生成 vercel.json 配置文件
- 生成 requirements.txt（Python 项目）
- 提供部署步骤指导
- 检测部署配置问题并给出修复建议

## 项目类型检测规则

| 类型 | 检测条件 |
|------|----------|
| Flask | 存在 app.py 或 wsgi.py，且导入 flask |
| Django | 存在 manage.py |
| 静态站点 | 存在 index.html 和/或 dist/ 目录 |
| Next.js | 存在 next.config.js |
| Vite | 存在 vite.config.js |

## 输出模板

### Flask + Vercel 配置
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/app.py"
    }
  ]
}
```

### 静态站点配置
```json
{
  "version": 2,
  "public": true
}
```

## 部署流程

1. 分析项目结构和依赖
2. 生成/更新配置文件
3. 提供部署命令
4. 输出后续配置建议（域名、环境变量等）

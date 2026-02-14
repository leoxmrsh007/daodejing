# 后端性能监控

## 当前状态

### API 性能基线

```python
# 在 app.py 中添加性能监控中间件
import time
import functools
from typing import Callable

from flask import Flask, g, request


def init_performance_monitoring(app: Flask) -> None:
    """初始化性能监控"""
    
    @app.before_request
    def before_request():
        """请求开始计时"""
        g.start_time = time.time()
        g.request_id = f"{time.time():.6f}"
    
    @app.after_request
    def after_request(response):
        """记录请求性能指标"""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            # 记录慢请求
            if duration > 1.0:  # 超过1秒的请求
                app.logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.3f}s"
                )
            
            # 添加性能头部
            response.headers['X-Response-Time'] = f"{duration:.3f}s"
            
            # 记录到日志
            app.logger.info(
                f"{request.method} {request.path} - {response.status_code} "
                f"- {duration:.3f}s"
            )
        
        return response


def performance_monitor(threshold: float = 0.5) -> Callable:
    """函数性能监控装饰器
    
    Args:
        threshold: 慢函数阈值（秒）
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.time() - start
                if duration > threshold:
                    import logging
                    logging.getLogger(__name__).warning(
                        f"Slow function: {func.__name__} took {duration:.3f}s"
                    )
        return wrapper
    return decorator
```

### API 响应时间统计

```python
# services/monitoring.py
import time
from collections import defaultdict
from typing import Dict, List, Optional


class APIMetrics:
    """API性能指标收集器"""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.error_counts: Dict[str, int] = defaultdict(int)
    
    def record_request(self, endpoint: str, duration: float, status_code: int) -> None:
        """记录请求指标"""
        self.metrics[endpoint].append(duration)
        
        # 只保留最近1000个样本
        if len(self.metrics[endpoint]) > 1000:
            self.metrics[endpoint] = self.metrics[endpoint][-1000:]
        
        if status_code >= 400:
            self.error_counts[endpoint] += 1
    
    def get_stats(self, endpoint: Optional[str] = None) -> Dict:
        """获取性能统计"""
        if endpoint:
            return self._calc_stats(endpoint)
        
        return {
            endpoint: self._calc_stats(endpoint)
            for endpoint in self.metrics.keys()
        }
    
    def _calc_stats(self, endpoint: str) -> Dict:
        """计算端点统计信息"""
        times = self.metrics[endpoint]
        if not times:
            return {}
        
        times.sort()
        n = len(times)
        
        return {
            "count": n,
            "avg": sum(times) / n,
            "min": times[0],
            "max": times[-1],
            "p50": times[int(n * 0.5)],
            "p95": times[int(n * 0.95)],
            "p99": times[int(n * 0.99)],
            "errors": self.error_counts[endpoint]
        }


# 全局指标实例
api_metrics = APIMetrics()
```

### 性能监控 API

```python
# routes/monitoring_routes.py
from flask import Blueprint, jsonify

from services.monitoring import api_metrics

bp = Blueprint("monitoring", __name__, url_prefix="/monitoring")


@bp.route("/metrics")
def get_metrics():
    """获取API性能指标"""
    return jsonify(api_metrics.get_stats())


@bp.route("/health")
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    })


@bp.route("/stats")
def server_stats():
    """服务器统计信息"""
    import psutil
    
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return jsonify({
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": (disk.used / disk.total) * 100
        },
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count()
        }
    })
```

## 缓存优化

### 当前缓存策略

```python
# 优化现有缓存实现
import functools
import hashlib
import json
from typing import Any, Callable

from flask import current_app


def cached(timeout: int = 300, key_prefix: str = "") -> Callable:
    """函数结果缓存装饰器
    
    Args:
        timeout: 缓存过期时间（秒）
        key_prefix: 缓存键前缀
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = _generate_cache_key(key_prefix, func.__name__, args, kwargs)
            
            # 尝试从缓存获取
            cache = current_app.config.get('CACHE')
            if cache:
                cached_value = cache.get(cache_key)
                if cached_value is not None:
                    return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            if cache:
                cache.set(cache_key, result, timeout=timeout)
            
            return result
        return wrapper
    return decorator


def _generate_cache_key(prefix: str, func_name: str, args: tuple, kwargs: dict) -> str:
    """生成缓存键"""
    key_data = {
        "prefix": prefix,
        "func": func_name,
        "args": args,
        "kwargs": kwargs
    }
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return f"{prefix}:{hashlib.md5(key_str.encode()).hexdigest()}"
```

### 数据库查询优化（未来）

```python
# 如果使用数据库，优化查询
"""
数据库优化建议：

1. 添加索引
   - classic_id + chapter_id
   - search_text (全文索引)

2. 查询优化
   - 使用 select_related 减少查询次数
   - 使用 prefetch_related 预加载关联数据
   - 添加查询缓存

3. 连接池
   - 使用 SQLAlchemy 连接池
   - 配置适当的池大小
"""
```

## 性能目标

### API 响应时间

| 端点类型 | 当前目标 | 优化目标 |
|---------|----------|----------|
| 静态页面 | < 100ms | < 50ms |
| 章节数据 | < 200ms | < 100ms |
| 搜索 API | < 500ms | < 300ms |
| TTS 代理 | < 2000ms | < 1500ms |

### 并发能力

| 指标 | 目标 |
|------|------|
| 并发用户 | 1000+ |
| RPS (Requests Per Second) | 100+ |
| 错误率 | < 0.1% |

## 监控告警

### 告警规则

```yaml
# 告警配置示例
alerts:
  - name: high_error_rate
    condition: error_rate > 5%
    duration: 5m
    severity: critical
    
  - name: slow_api_response
    condition: p95_response_time > 500ms
    duration: 10m
    severity: warning
    
  - name: high_cpu_usage
    condition: cpu_usage > 80%
    duration: 15m
    severity: warning
    
  - name: memory_usage
    condition: memory_usage > 90%
    duration: 5m
    severity: critical
```

### 日志规范

```python
# 结构化日志
import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """JSON格式日志"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log")
    ]
)

for handler in logging.root.handlers:
    handler.setFormatter(JSONFormatter())
```

## 推荐工具

### APM 工具

1. **New Relic**: 全栈性能监控
2. **Datadog**: 云监控服务
3. **Prometheus + Grafana**: 开源监控方案
4. **Elastic APM**: ELK 集成方案

### 日志服务

1. **ELK Stack**: Elasticsearch + Logstash + Kibana
2. **Splunk**: 企业级日志分析
3. **Graylog**: 开源日志管理

### 集成示例

```python
# Prometheus 指标导出
from prometheus_client import Counter, Histogram, generate_latest

# 定义指标
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')


@bp.route("/metrics/prometheus")
def prometheus_metrics():
    """Prometheus 指标端点"""
    return generate_latest()
```

---

*创建日期: 2026-01-29*  
*下次评估: 2026-02-05*

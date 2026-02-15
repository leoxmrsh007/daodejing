# -*- coding: utf-8 -*-
"""
安全扫描和审计工具
实现自动化的安全漏洞扫描
"""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class SecurityScanner:
    """
    安全扫描器
    扫描代码和配置中的安全漏洞
    """

    def __init__(self, project_root: Path):
        """
        初始化安全扫描器

        Args:
            project_root: 项目根目录
        """
        self.project_root = project_root
        self.issues = []

    def scan_all(self) -> Dict[str, Any]:
        """
        执行完整的安全扫描

        Returns:
            扫描结果
        """
        results = {
            "scan_time": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "issues": {"critical": [], "high": [], "medium": [], "low": [], "info": []},
            "summary": {},
        }

        # 1. 代码安全扫描
        print("🔍 扫描代码安全问题...")
        self._scan_code_security(results)

        # 2. 依赖安全扫描
        print("🔍 扫描依赖安全问题...")
        self._scan_dependencies(results)

        # 3. 配置安全扫描
        print("🔍 扫描配置安全问题...")
        self._scan_configuration(results)

        # 4. 文件权限扫描
        print("🔍 扫描文件权限问题...")
        self._scan_file_permissions(results)

        # 生成摘要
        results["summary"] = {
            "total_issues": sum(len(v) for v in results["issues"].values()),
            "critical": len(results["issues"]["critical"]),
            "high": len(results["issues"]["high"]),
            "medium": len(results["issues"]["medium"]),
            "low": len(results["issues"]["low"]),
            "info": len(results["issues"]["info"]),
        }

        return results

    def _scan_code_security(self, results: Dict[str, Any]) -> None:
        """扫描代码安全问题"""
        # 扫描Python文件中的安全问题
        py_files = list(self.project_root.rglob("*.py"))

        # 常见安全模式
        security_patterns = {
            "SQL Injection": {
                "pattern": r"\bexecute\s*\(|exec\s*\(|eval\s*\(",
                "severity": "critical",
                "description": "可能存在SQL注入或代码注入漏洞",
            },
            "Hardcoded Secrets": {
                "pattern": r'(api_key|secret|password|token)\s*=\s*[\'"]\w+[\'"]',
                "severity": "high",
                "description": "检测到硬编码的密钥或密码",
            },
            "Weak SSL": {
                "pattern": r"ssl\.verify\s*=\s*(False|0)",
                "severity": "medium",
                "description": "SSL证书验证被禁用",
            },
            "Debug Mode": {
                "pattern": r"debug\s*=\s*True",
                "severity": "low",
                "description": "调试模式在生产环境中可能被启用",
            },
            "Unvalidated Input": {
                "pattern": r"request\.args\.get\([\047\042].*?[\047\042]\)",
                "severity": "high",
                "description": "未经验证的输入可能存在安全风险",
            },
        }

        for py_file in py_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                for line_num, line in enumerate(lines, 1):
                    for issue_name, issue_info in security_patterns.items():
                        if re.search(issue_info["pattern"], line, re.IGNORECASE):
                            results["issues"][issue_info["severity"]].append(
                                {
                                    "type": "code",
                                    "issue": issue_name,
                                    "severity": issue_info["severity"],
                                    "file": str(py_file.relative_to(self.project_root)),
                                    "line": line_num,
                                    "description": issue_info["description"],
                                    "code": line.strip(),
                                }
                            )
            except Exception as e:
                print(f"扫描文件失败 {py_file}: {e}")

    def _scan_dependencies(self, results: Dict[str, Any]) -> None:
        """扫描依赖安全问题"""
        requirements_file = self.project_root / "requirements.txt"
        requirements_dev_file = self.project_root / "requirements-dev.txt"

        # 已知有安全漏洞的包
        vulnerable_packages = {
            "flask": {"min_version": "2.0.0", "issue": "Flask < 2.0 存在已知安全漏洞"},
            "jinja2": {
                "min_version": "3.0.0",
                "issue": "Jinja2 < 3.0 存在模板注入风险",
            },
            "werkzeug": {
                "min_version": "2.0.0",
                "issue": "Werkzeug < 2.0 存在路径遍历风险",
            },
        }

        for req_file in [requirements_file, requirements_dev_file]:
            if not req_file.exists():
                continue

            try:
                with open(req_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    # 解析包名和版本
                    match = re.match(r"([a-zA-Z0-9_-]+)([><=~]+)([\d.]+)", line)
                    if match:
                        package_name = match.group(1)
                        operator = match.group(2)
                        version = match.group(3)

                        # 检查是否为已知漏洞包
                        if package_name.lower() in vulnerable_packages:
                            vuln_info = vulnerable_packages[package_name.lower()]
                            min_version = vuln_info["min_version"]

                            # 简单的版本比较
                            if self._version_less_than(version, min_version):
                                results["issues"]["high"].append(
                                    {
                                        "type": "dependency",
                                        "issue": f"{package_name} {version}",
                                        "severity": "high",
                                        "file": str(
                                            req_file.relative_to(self.project_root)
                                        ),
                                        "line": line_num,
                                        "description": vuln_info["issue"],
                                        "recommended": f"升级到 >= {min_version}",
                                    }
                                )
            except Exception as e:
                print(f"扫描依赖失败 {req_file}: {e}")

    def _scan_configuration(self, results: Dict[str, Any]) -> None:
        """扫描配置安全问题"""
        config_file = self.project_root / "config.py"

        if not config_file.exists():
            return

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 检查配置问题
            issues = [
                {
                    "pattern": r'SECRET_KEY\s*=\s*[\'"]\s*[\'"]',
                    "severity": "critical",
                    "description": "SECRET_KEY为空",
                },
                {
                    "pattern": r'SECRET_KEY\s*=\s*[\'"][a-zA-Z0-9]{1,10}[\'"]',
                    "severity": "critical",
                    "description": "SECRET_KEY太短（至少32字符）",
                },
                {
                    "pattern": r"DEBUG\s*=\s*True",
                    "severity": "low",
                    "description": "调试模式在生产环境中可能被启用",
                },
                {
                    "pattern": r"ALLOWED_HOSTS\s*=\s*[\[\]\*]",
                    "severity": "medium",
                    "description": "ALLOWED_HOSTS设置过于宽松",
                },
            ]

            for issue in issues:
                if re.search(issue["pattern"], content):
                    results["issues"][issue["severity"]].append(
                        {
                            "type": "configuration",
                            "issue": issue["description"],
                            "severity": issue["severity"],
                            "file": "config.py",
                            "description": issue["description"],
                        }
                    )
        except Exception as e:
            print(f"扫描配置失败: {e}")

    def _scan_file_permissions(self, results: Dict[str, Any]) -> None:
        """扫描文件权限问题"""
        # 检查敏感文件权限
        sensitive_files = [".env", ".env.local", "config.py", "credentials.json"]

        for file_name in sensitive_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                try:
                    # 检查文件权限（Unix系统）
                    if os.name != "nt":  # Windows不支持os.access的权限检查
                        if os.access(file_path, os.R_OK | os.W_OK):
                            # 在生产环境中，敏感文件应该有严格的权限
                            if os.access(file_path, os.X_OK):
                                results["issues"]["medium"].append(
                                    {
                                        "type": "file_permission",
                                        "issue": f"{file_name} 权限过于宽松",
                                        "severity": "medium",
                                        "file": file_name,
                                        "description": "敏感文件应限制访问权限",
                                    }
                                )
                except Exception as e:
                    print(f"检查文件权限失败 {file_name}: {e}")

    def _version_less_than(self, version1: str, version2: str) -> bool:
        """
        比较版本号

        Args:
            version1: 版本1
            version2: 版本2

        Returns:
            version1 < version2
        """
        v1_parts = [int(x) for x in version1.split(".")]
        v2_parts = [int(x) for x in version2.split(".")]

        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 < v2:
                return True
            elif v1 > v2:
                return False

        return len(v1_parts) < len(v2_parts)

    def generate_report(
        self, results: Dict[str, Any], output_file: Optional[Path] = None
    ) -> str:
        """
        生成安全报告

        Args:
            results: 扫描结果
            output_file: 输出文件路径（可选）

        Returns:
            报告文本
        """
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("🔒 安全扫描报告")
        report_lines.append("=" * 60)
        report_lines.append(f"扫描时间: {results['scan_time']}")
        report_lines.append(f"项目目录: {results['project_root']}")
        report_lines.append("")

        # 摘要
        summary = results["summary"]
        report_lines.append("📊 扫描摘要")
        report_lines.append("-" * 60)
        report_lines.append(f"总问题数: {summary['total_issues']}")
        report_lines.append(f"严重 (Critical): {summary['critical']}")
        report_lines.append(f"高危 (High): {summary['high']}")
        report_lines.append(f"中危 (Medium): {summary['medium']}")
        report_lines.append(f"低危 (Low): {summary['low']}")
        report_lines.append(f"信息 (Info): {summary['info']}")
        report_lines.append("")

        # 详细问题
        for severity in ["critical", "high", "medium", "low", "info"]:
            issues = results["issues"][severity]
            if issues:
                report_lines.append(f"🔴 {severity.upper()} ({len(issues)})")
                report_lines.append("-" * 60)

                for issue in issues:
                    report_lines.append(f"\n  类型: {issue.get('type', 'unknown')}")
                    report_lines.append(f"  问题: {issue['issue']}")
                    report_lines.append(f"  描述: {issue['description']}")
                    if "file" in issue:
                        report_lines.append(f"  文件: {issue['file']}")
                    if "line" in issue:
                        report_lines.append(f"  行号: {issue['line']}")
                    if "code" in issue:
                        report_lines.append(f"  代码: {issue['code']}")
                    if "recommended" in issue:
                        report_lines.append(f"  建议: {issue['recommended']}")
                report_lines.append("")

        report_lines.append("=" * 60)

        report_text = "\n".join(report_lines)

        # 保存到文件
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(report_text)
            print(f"✅ 安全报告已保存到: {output_file}")

        return report_text


def run_security_scan(project_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    运行安全扫描

    Args:
        project_root: 项目根目录（如果为None则使用当前目录）

    Returns:
        扫描结果
    """
    if project_root is None:
        project_root = Path(__file__).parent.parent

    scanner = SecurityScanner(project_root)
    results = scanner.scan_all()

    # 生成报告
    report_file = project_root / "security_report.txt"
    scanner.generate_report(results, report_file)

    # 保存JSON格式
    json_file = project_root / "security_report.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


if __name__ == "__main__":
    import sys

    project_root = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    )
    results = run_security_scan(project_root)
    print(f"\n✅ 安全扫描完成")
    print(f"总问题数: {results['summary']['total_issues']}")
    print(f"严重问题: {results['summary']['critical']}")
    print(f"高危问题: {results['summary']['high']}")

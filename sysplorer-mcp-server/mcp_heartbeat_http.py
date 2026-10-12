"""
可选 HTTP 健康检查：由 ACP Server 在启动 OpenCode 时注入 SYSPLORE_MCP_HEARTBEAT_PORT 等环境变量后，
本进程在指定 loopback 地址上提供 GET 端点。未设置 PORT 时本模块不启动任何监听（零行为变更）。

仅供「ACP 注入子进程环境」场景使用；独立运行 MCP 时通常无需配置。
"""
from __future__ import annotations

import json
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type

_LOG = logging.getLogger(__name__)


def _normalize_bind(raw: str) -> str:
    s = (raw or "").strip() or "127.0.0.1"
    if s in ("0.0.0.0", "[::]", "::", "*"):
        _LOG.warning(
            "SYSPLORE_MCP_HEARTBEAT_BIND=%r is not allowed as default-wide bind; using 127.0.0.1",
            s,
        )
        return "127.0.0.1"
    return s


def _normalize_path(raw: str) -> str:
    p = (raw or "").strip() or "/health"
    if not p.startswith("/"):
        p = "/" + p
    return p


def _make_handler_class(health_path: str) -> Type[BaseHTTPRequestHandler]:
    class _HeartbeatHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            req_path = self.path.split("?", 1)[0].rstrip("/") or "/"
            target = health_path.rstrip("/") or "/"
            if req_path == target:
                body = json.dumps({"ok": True}, separators=(",", ":")).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, fmt: str, *args: object) -> None:  # noqa: ARG002
            return

    return _HeartbeatHandler


def start_mcp_heartbeat_http() -> threading.Thread | None:
    """若环境变量指定端口则启动后台线程中的 HTTPServer；否则返回 None。"""
    port_s = os.environ.get("SYSPLORE_MCP_HEARTBEAT_PORT")
    if not port_s or not str(port_s).strip():
        return None
    try:
        port = int(str(port_s).strip(), 10)
    except ValueError:
        _LOG.warning("SYSPLORE_MCP_HEARTBEAT_PORT is not a valid integer: %r", port_s)
        return None
    if not (1 <= port <= 65535):
        _LOG.warning("SYSPLORE_MCP_HEARTBEAT_PORT out of range: %s", port)
        return None

    bind = _normalize_bind(os.environ.get("SYSPLORE_MCP_HEARTBEAT_BIND", "127.0.0.1"))
    path = _normalize_path(os.environ.get("SYSPLORE_MCP_HEARTBEAT_PATH", "/health"))
    handler_cls = _make_handler_class(path)

    try:
        server = HTTPServer((bind, port), handler_cls)
    except OSError:
        _LOG.exception(
            "MCP heartbeat HTTP bind failed bind=%s port=%s path=%s",
            bind,
            port,
            path,
        )
        return None

    def _run() -> None:
        try:
            server.serve_forever(poll_interval=0.5)
        except Exception:
            _LOG.exception("MCP heartbeat HTTP server exited unexpectedly")

    thread = threading.Thread(target=_run, name="sysplorer-mcp-heartbeat", daemon=True)
    thread.start()
    _LOG.warning(
        "MCP heartbeat HTTP listening on http://%s:%s%s (ACP probe)",
        bind,
        port,
        path,
    )
    return thread

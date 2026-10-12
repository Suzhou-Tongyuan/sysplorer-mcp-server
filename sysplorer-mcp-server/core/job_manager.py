"""Background async jobs for check / translate / simulate (used by workflow MCP tools)."""
from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from path_config import TEMP_CODE_FOLDER


@dataclass
class MWorksJob:
    job_id: str
    action: str
    status: str
    payload: Dict[str, Any]
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    result: Any = None
    error: str = ""

    def elapsed(self) -> str:
        sec = int(time.time() - self.created_at)
        return f"{sec}s" if sec < 60 else f"{sec // 60}m{sec % 60}s"


class JobManager:
    def __init__(self) -> None:
        self._jobs: Dict[str, MWorksJob] = {}
        self._lock = threading.Lock()

    def submit(self, action: str, payload: Dict[str, Any]) -> MWorksJob:
        job_id = f"mws_{uuid.uuid4().hex[:12]}"
        job = MWorksJob(job_id=job_id, action=action, status="queued", payload=payload)
        with self._lock:
            self._jobs[job_id] = job
        t = threading.Thread(target=self._run_job, args=(job_id,), daemon=True)
        t.start()
        return job

    def get(self, job_id: str) -> Optional[MWorksJob]:
        with self._lock:
            return self._jobs.get(job_id)

    def _update(self, job_id: str, **kwargs: Any) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            for key, value in kwargs.items():
                setattr(job, key, value)
            job.updated_at = time.time()

    def _run_job(self, job_id: str) -> None:
        job = self.get(job_id)
        if not job:
            return
        self._update(job_id, status="running")
        try:
            pl = job.payload
            if job.action == "check":
                from tools.model_ops import check_model

                raw = check_model(
                    model_names=pl.get("model_names"),
                    model_name=str(pl.get("model_name", "") or ""),
                    model_type=str(pl.get("model_type", "MODELICA")),
                    stop_on_error=bool(pl.get("stop_on_error", False)),
                    reload_mo_path=str(pl.get("reload_mo_path", "") or ""),
                )
                out = json.loads(raw)
                if out.get("ok"):
                    self._update(job_id, status="done", result=out)
                else:
                    self._update(job_id, status="failed", result=out, error=str(out.get("error", "") or ""))
                return
            if job.action == "translate":
                from tools.model_ops import translate_model

                raw = translate_model(
                    model_name=str(pl.get("model_name", "") or ""),
                    code_folder=str(pl.get("code_folder", TEMP_CODE_FOLDER) or TEMP_CODE_FOLDER),
                    model_type=str(pl.get("model_type", "MODELICA")),
                    code_type=str(pl.get("code_type", "NORMAL")),
                    build_type=str(pl.get("build_type", "BINARY")),
                    run_to=str(pl.get("run_to", "MAKING")),
                    config_json=str(pl.get("config_json", "") or ""),
                    reload_mo_path=str(pl.get("reload_mo_path", "") or ""),
                )
                out = json.loads(raw)
                if out.get("ok"):
                    self._update(job_id, status="done", result=out)
                else:
                    self._update(job_id, status="failed", result=out, error=str(out.get("error", "") or ""))
                return
            if job.action == "simulate":
                from tools.model_ops import simulate_model

                raw = simulate_model(
                    model_name=str(pl.get("model_name", "") or ""),
                    sim_mode=int(pl.get("sim_mode", 0)),
                    target_time=pl.get("target_time", []),
                    ext_res_path=str(pl.get("ext_res_path", "") or ""),
                    verify_result_var=str(pl.get("verify_result_var", "") or ""),
                    verify_time_point=pl.get("verify_time_point", "end"),
                    result_var_type=int(pl.get("result_var_type", 0)),
                    reload_mo_path=str(pl.get("reload_mo_path", "") or ""),
                )
                out = json.loads(raw)
                if out.get("ok"):
                    self._update(job_id, status="done", result=out)
                else:
                    self._update(job_id, status="failed", result=out, error=str(out.get("error", "") or ""))
                return

            self._update(job_id, status="failed", error=f"Unsupported action: {job.action}")
            return
        except Exception as exc:
            self._update(job_id, status="failed", error=f"{job.action} failed: {exc}")


job_manager = JobManager()

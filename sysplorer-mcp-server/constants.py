"""MWorks MCP Server — all immutable constants."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from path_config import PROJECT_ROOT, METADATA_LIB_PATH, SMART_LAYOUT_TEMP_DIR

# ── Project paths（PROJECT_ROOT = 工作区根；查阅 resources 见 path_config.get_resources_root） ──
_PROJECT_ROOT = PROJECT_ROOT
_METADATA_LIB_PATH = METADATA_LIB_PATH
_SMART_LAYOUT_TEMP_DIR = SMART_LAYOUT_TEMP_DIR

# ── Regex constants ───────────────────────────────────────────────────────────
_CLASS_RE = re.compile(r"\b(package|model|block|record|connector|class)\s+([A-Za-z_]\w*)")
_EXTENDS_RE = re.compile(r"^\s*extends\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)", re.MULTILINE)
_IMPORT_RE = re.compile(r"^\s*import\s+([^;]+);", re.MULTILINE)
_PARAM_RE = re.compile(
    r'^\s*parameter\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s+([A-Za-z_]\w*)'
    r'(?:\s*=\s*([^;"\n]+))?\s*(?:"([^"]*)")?\s*;',
    re.MULTILINE,
)
_DECL_RE = re.compile(
    r'^\s*([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s+([A-Za-z_]\w*)\s*(?:\([^;\n]*\))?\s*(?:"([^"]*)")?\s*;',
    re.MULTILINE,
)
_WITHIN_RE = re.compile(r"^\s*within\s+([\w.]+)\s*;", re.MULTILINE)
# Dotted names only (A.B or A.B.C). LoadLibrary uses the first segment, not every Ident.
_NS_REF_RE = re.compile(r"\b([A-Z][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)")
_LIB_NAME_VERSION_RE = re.compile(r"^(?P<family>.+?)\s+(?P<version>\d+(?:\.\d+)*(?:\.[A-Za-z0-9]+)*)$")
_IFACE_CONN_DECL_RE = re.compile(
    r"^\s*([\w.]+)\s+(\w+)\s*(?:\([^;]*?\))?\s*(?:\"([^\"]*)\")?\s*;",
    re.MULTILINE,
)
_CLASS_TOKEN_RE = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*")

# ── Connector / parameter probe lists ─────────────────────────────────────────
_CONNECTOR_SUFFIXES: Tuple[str, ...] = ("Pin", "Port", "Flange", "Terminal", "Plug")

_PROBE_CONNECTORS: Tuple[str, ...] = (
    "flange_a", "flange_b", "support", "flange",
    "port", "port_a", "port_b",
    "p", "n", "pin_p", "pin_n",
    "frame_a", "frame_b", "axis", "bearing",
    "heat_port", "heatPort",
    "inlet", "outlet", "frame",
    "ring", "sun", "carrier",
)

_PROBE_PARAMS: Tuple[str, ...] = (
    # mechanics — translational
    "m", "m1", "m2", "k", "d", "b", "L", "L1", "L2",
    "s_rel0", "phi_rel0", "f0", "v_small", "v0", "a0",
    "f_Coulomb", "f_Stribeck", "fexp",
    # mechanics — rotational
    "J", "J1", "J2", "phi0", "w0", "tau0",
    "tau_Coulomb", "tau_Stribeck", "wexp",
    "ratio", "gearRatio", "i", "R", "T", "F", "v",
    # multi-body / general
    "r", "r0", "e", "n", "N", "nParallel",
    "s_max", "s_min", "phi_max", "phi_min",
    "c_contact", "d_contact",
    # electrical
    "Rc", "Lc", "Cc", "Vnom", "Inom",
    "RRef", "R_ref", "Vref", "Lm", "Lr", "Ls", "Rs", "Rr",
    "Jr", "Js", "Ra", "La", "Ke", "Kt", "Bm",
    "Pn", "nn", "Mn", "Vn", "fn", "cosPhis", "pf",
    # hydraulic / pneumatic
    "A", "V", "V0", "Q", "Cd", "rho", "mu", "nu",
    "dp_nominal", "m_flow_nominal",
    "kv", "pS", "pT", "qnom", "D", "l",
    # thermal / fluid
    "C", "G", "R_th", "T_ref", "alpha",
    "cp", "lambda_", "T0", "T_start", "p0", "p_start",
    "h_start", "rho0", "Gc", "C_th",
    # control / signal
    "k_p", "k_i", "k_d", "T_i", "T_d",
    "Ti", "Td", "Tf", "Nd",
    "gain", "k3",
    "amplitude", "freqHz", "phase", "offset", "startTime",
    "y0", "y_start", "x_start", "x1_start", "x2_start",
    "uMax", "uMin", "yMax", "yMin", "limitsAtInit",
    "initType",
    # battery / power electronics
    "Q_max", "SOC_init", "V0_cell", "R0_cell", "Tau", "Cin",
    "Vdc", "duty", "fsw", "Lf", "Cf",
    # engine
    "eta",
    # common boolean flags
    "stateSelect", "useSupport", "useHeatPort",
    "useFlange", "animation",
    # spring-damper / contact
    "c", "c1", "c2", "d1", "d2",
    "k1", "k2", "b1", "b2",
    "k_c", "k_d",
)

_IFACE_CONN_KEYWORDS: Tuple[str, ...] = (
    "Flange", "Pin", "Port", "Plug", "Frame", "HeatPort",
    "Connector", "Interfaces.", "Support", "Terminal",
    "ring", "sun", "carrier",
)

_PREFERRED_LIBRARY_VERSIONS: Dict[str, str] = {
    "Modelica": "4.0.0.TY.1",
}


def split_trailing_version_from_library_display_name(library_name: str) -> Tuple[str, str]:
    """若名称为「库名 + 空格 + 版本号」展示形式，拆成 (库名, 版本)；否则 (原样去空白, '')。"""
    raw = (library_name or "").strip()
    if not raw:
        return "", ""
    m = _LIB_NAME_VERSION_RE.match(raw)
    if m:
        return m.group("family").strip(), m.group("version").strip()
    return raw, ""


def commercial_lib_load_without_version(library_name: str) -> bool:
    """是否对 LoadLibrary 只传库名、不传第二参版本字符串。

    除内置 **Modelica** 标准库外，其余商业库均由 Sysplorer 官方 API 自行解析合适版本。
    """
    n = (library_name or "").strip()
    if not n:
        return False
    return n != "Modelica"


def normalize_load_library_call(library_name: str, library_version: str = "") -> Tuple[str, str]:
    """返回传给 Sysplorer ``LoadLibrary`` 的 (库名, 版本)。

    策略与 ``commercial_lib_load_without_version`` 一致：除 **Modelica** 外一律不传版本字符串，
    由 Sysplorer 自选已安装版本；避免误传不存在的 ``TYMultibody`` 等版本导致加载失败。
    """
    family, trailing_ver = split_trailing_version_from_library_display_name(library_name or "")
    if not family:
        return "", ""
    ver_combined = (library_version or "").strip() or trailing_ver
    if commercial_lib_load_without_version(family):
        return family, ""
    # Modelica：显式版本优先，否则用首选
    if ver_combined:
        return family, ver_combined
    return family, _PREFERRED_LIBRARY_VERSIONS.get(family, "")

# ── Error hints ───────────────────────────────────────────────────────────────
_SYSPLORER_CONNECT_ERROR_HINTS: Tuple[str, ...] = (
    "failed to connect sysplorer api",
    "list index out of range",
    "connectsysplorer",
    "未找到端口",
)

# ── Smart Layout Engine constants ─────────────────────────────────────────────
_SL_PORT_SIDE_MAP: Dict[str, str] = {
    # Rotational mechanics
    "flange_a": "WEST",  "flange_b": "EAST",
    "support":  "SOUTH", "bearing":  "SOUTH", "axis": "NORTH",
    # Translational mechanics
    "flange":   "WEST",
    "s_ref":    "WEST",
    "v_ref":    "WEST",  "a_ref": "WEST",
    # MultiBody
    "frame_a":  "WEST",  "frame_b":  "EAST",
    "frame":    "SOUTH",
    # Electrical
    "p":        "WEST",  "n":        "EAST",
    "pin_p":    "WEST",  "pin_n":    "EAST",
    "plug_p":   "WEST",  "plug_n":   "EAST",
    "heatPort": "SOUTH", "heat_port":"SOUTH",
    # Magnetic
    "port_p":   "WEST",  "port_n":   "EAST",
    # Fluid
    "port_a":   "WEST",  "port_b":   "EAST",
    "inlet":    "WEST",  "outlet":   "EAST",
    "port":     "SOUTH",
    # Signal / Control
    "u":        "WEST",  "u1": "WEST", "u2": "WEST", "u3": "WEST", "u4": "WEST",
    "y":        "EAST",  "y1": "EAST", "y2": "EAST",
    "in1":      "WEST",  "in2": "WEST",
    "out1":     "EAST",  "out2": "EAST",
    "reference":"WEST",  "actual": "WEST", "error": "EAST",
    "tau":      "WEST",  "tau_ref": "WEST",
    "w_ref":    "WEST",  "f_normalized": "SOUTH",
}

_SL_DOMAIN_COLORS: Dict[str, Tuple[int, int, int]] = {
    "rotational":    (0,   0,   0),
    "translational": (0,  127,  0),
    "multibody":     (95,  95, 95),
    "electrical":    (0,   0, 255),
    "magnetic":      (255,127,  0),
    "fluid":         (0,  127,255),
    "thermal":       (191,  0,  0),
    "signal":        (0,   0, 127),
    "unknown":       (0,   0, 127),
}

_SL_PORT_DOMAIN: Dict[str, str] = {
    "flange_a": "rotational", "flange_b": "rotational",
    "support":  "rotational", "bearing":  "rotational", "axis": "rotational",
    "flange":   "translational",
    "s_ref":    "translational", "v_ref": "translational", "a_ref": "translational",
    "frame_a":  "multibody",  "frame_b": "multibody",  "frame": "multibody",
    "p":        "electrical", "n":       "electrical",
    "pin_p":    "electrical", "pin_n":   "electrical",
    "plug_p":   "electrical", "plug_n":  "electrical",
    "heatPort": "thermal",    "heat_port":"thermal",
    "port_p":   "magnetic",   "port_n":  "magnetic",
    "port_a":   "fluid",      "port_b":  "fluid",
    "inlet":    "fluid",      "outlet":  "fluid",
    "port":     "thermal",
    "u":        "signal",     "u1": "signal", "u2": "signal",
    "y":        "signal",     "y1": "signal",
    "tau":      "signal",     "f_normalized": "signal",
}

_SL_H_SPACING: float = 48.0
_SL_V_SPACING: float = 52.0
_SL_DEFAULT_HW: float = 10.0
_SL_DEFAULT_HH: float = 10.0
_SL_MIN_GAP: float = 10.0

_SL_PRIMARY_PORTS: Tuple[str, ...] = (
    "flange_a", "frame_a", "port_a", "port_p", "pin_p", "inlet", "p", "u", "u1", "in1",
)

_SL_ROTATION_MAP: Dict[Tuple[str, str], int] = {
    ("WEST",  "WEST"):   0,   ("WEST",  "EAST"):  180,
    ("WEST",  "NORTH"):  90,  ("WEST",  "SOUTH"): 270,
    ("EAST",  "EAST"):   0,   ("EAST",  "WEST"):  180,
    ("EAST",  "NORTH"): 270,  ("EAST",  "SOUTH"):  90,
    ("NORTH", "NORTH"):  0,   ("NORTH", "SOUTH"): 180,
    ("NORTH", "WEST"):  270,  ("NORTH", "EAST"):   90,
    ("SOUTH", "SOUTH"):  0,   ("SOUTH", "NORTH"): 180,
    ("SOUTH", "WEST"):   90,  ("SOUTH", "EAST"):  270,
}

# ── Electrical circuit layout ─────────────────────────────────────────────────
# 两端电气器件：自然方向是「左(p)→右(n)」横置。在电路图模式下需要竖置（p朝上）。
_SL_ELEC_TWO_TERMINAL: frozenset = frozenset({
    # 电源
    "ConstantVoltage", "SineVoltage", "StepVoltage", "PulseVoltage",
    "RampVoltage", "TableVoltage", "SignalVoltage", "ConstantCurrent",
    "SineCurrent", "StepCurrent", "SignalCurrent",
    # 无源器件
    "Resistor", "Conductor", "Capacitor", "Inductor",
    "VariableResistor", "VariableCapacitor", "VariableInductor",
    "SaturatingInductor",
    # 理想器件
    "IdealDiode", "IdealThyristor", "IdealGTOThyristor",
    "IdealOpeningSwitch", "IdealClosingSwitch",
    "IdealTransformer", "IdealGyrator",
    # 半导体
    "Diode", "ZenerDiode", "NMOS", "PMOS", "NPN", "PNP",
    # 测量
    "VoltageSensor", "CurrentSensor", "PowerSensor",
})

# 只有单个电气引脚的"地"类器件
_SL_ELEC_GROUND: frozenset = frozenset({
    "Ground",
})

# 纯信号源/测量块（不走两端竖置）
_SL_ELEC_SIGNAL_BLOCKS: frozenset = frozenset({
    "BooleanPulse", "BooleanStep", "BooleanConstant",
    "BooleanExpression", "BooleanTable",
    "Pulse", "Step", "Ramp", "Sine", "Trapezoid",
    "Constant", "Clock", "SampleTrigger",
    "RealExpression", "IntegerExpression",
    "BooleanToReal", "RealToBoolean",
})

# 电路图模式识别：图中≥此比例的节点属于电气两端器件时激活电路模式
_SL_CIRCUIT_MODE_THRESHOLD: float = 0.4

# 电路图布局参数
_SL_CIRC_H_STEP: float  = 40.0   # 主路径水平步进（两组件中心距）
_SL_CIRC_V_STEP: float  = 50.0   # 竖置器件中心到母线距离
_SL_CIRC_RAIL_Y: float  = 30.0   # 高压母线 y 坐标
_SL_CIRC_GND_Y:  float  = -20.0  # 地线母线 y 坐标（器件 n 脚所在 y）
_SL_CIRC_GND_SYM_Y: float = -30.0  # Ground 符号中心 y
_SL_CIRC_SIG_Y:  float  = -20.0  # 信号源块（PWM等）中心 y
_SL_CIRC_COMP_HW: float = 10.0   # 默认器件半宽
_SL_CIRC_COMP_HH: float = 10.0   # 默认器件半高

# ── Domain keyword sets (used by lib_catalog / metadata) ──────────────────────
_DOM_THERMAL   = frozenset({"heatport", "heat_port", "heatport_a", "heatport_b"})
_DOM_FLUID     = frozenset({"port", "port_a", "port_b", "port_1", "port_2",
                             "inlet", "outlet", "inlet_a", "inlet_b"})
_DOM_MULTIBODY = frozenset({"frame", "frame_a", "frame_b", "frame_resolve",
                             "frame_ia", "frame_ib", "frame_im"})
_DOM_ROTATIONAL = frozenset({"axis", "bearing", "ring", "sun", "carrier",
                              "shaft", "shaft_a", "shaft_b"})
_DOM_FLANGE     = frozenset({"flange", "flange_a", "flange_b", "support",
                              "flange1", "flange2", "flange_support"})
_DOM_ELECTRICAL = frozenset({"pin_p", "pin_n", "plus", "minus", "positive",
                              "negative", "ac", "dc", "terminal", "terminal_p",
                              "terminal_n", "hv", "lv"})
_DOM_ROT_KW     = ("rotational", "gear", "clutch", "brake", "planetary",
                    "differential", "epicyclic", "shaft", "crankshaft")
_DOM_TRANS_KW   = ("translational", "suspension", "piston", "stopper", "contact",
                    "actuator", "vehicle", "masses")
_DOM_ELEC_KW    = ("electrical", "electric", "circuit", "battery", "inverter",
                    "converter", "power", "analog", "motor", "generator",
                    "semiconductor", "fuel")
_DOM_FLUID_KW   = ("fluid", "hydraulic", "pneumatic", "coolant", "pump",
                    "valve", "pipe", "tank")
_DOM_THERM_KW   = ("thermal", "heat", "temperature", "cooling")

# ── Query intent tokens ───────────────────────────────────────────────────────
_HYDRAULIC_INTENT_TOKENS = {
    "hydraulic", "servo", "actuator", "cylinder", "valve",
    "pump", "pressure", "flow", "fluid",
}

_HYDRAULIC_INTENT_FAMILIES = [
    "TYHydraulics",
    "TYHydraulicComponents",
    "TYThermalHydraulics",
    "TYThermalHydraulicComponents",
]

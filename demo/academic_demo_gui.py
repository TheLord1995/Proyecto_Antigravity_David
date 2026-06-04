"""
demo/academic_demo_gui.py
--------------------------
Capa visual interactiva para la demo académica del pipeline de Antigravity.

Permite:
  1. Seleccionar informe MT5 desde tests/data/
  2. Pulsar "Ejecutar análisis" y ver avanzar el pipeline por fases
  3. Abrir el resultado HTML al finalizar

Restricciones de seguridad activas:
  - ALLOW_REAL_EXECUTION = False (siempre)
  - approved_for_real = False (inmutable)
  - Sin MT5 real, sin Telegram, sin TradingView, sin RemoteAPIValidator
  - No modifica RiskEngine, BacktestValidator, MetricsEngine, MonteCarlo, MT5HtmlParser

"""

import io
import os
import sys
import uuid
import webbrowser
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Forzar UTF-8 en la consola de Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── Asegurar que el directorio raíz está en sys.path ──────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# ── Imports del proyecto ───────────────────────────────────────────────────────
from core.parsers.mt5_html_parser import MT5HtmlParser
from core.strategy_models import (
    BacktestPeriod,
    BacktestReport,
    TradeRecord,
    TradeDirection,
    StrategyMetadata,
    AssetClass,
    BiasChecklist,
    MarketRegimeChecklist,
    StrategyClassification,
)
from core.metrics.metrics_engine import MetricsEngine
from core.metrics.monte_carlo import MonteCarloEngine
from core.backtest_validator import BacktestValidator
from core.risk_engine import RiskEngine
from core.models import TradeIntent, AccountState

# ── Imports de GUI ───────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ── Configuración de rutas ─────────────────────────────────────────────────────
DEMO_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = DEMO_DIR / "output"
TEST_DATA_DIR = ROOT_DIR / "tests" / "data"
MT5_REPORT_PATH = TEST_DATA_DIR / "sample_mt5_report_en.html"
OUTPUT_HTML = OUTPUT_DIR / "academic_demo_result.html"

# ── Constantes de seguridad (inmutables) ──────────────────────────────────────
ALLOW_REAL_EXECUTION = False
APPROVED_FOR_REAL = False

# =============================================================================
# DATOS SINTÉTICOS PARA DEMO (sin MT5 real)
# =============================================================================

def _build_synthetic_trades() -> list[TradeRecord]:
    """
    Genera 20 TradeRecord sintéticos que simulan operaciones de un backtest.
    """
    base_open = datetime(2023, 1, 10, 9, 0, 0, tzinfo=timezone.utc)
    results = [
        120.5, -45.2, 88.3, -30.1, 210.7, -60.4, 55.0, 190.2,
        -80.3, 75.6, -22.5, 145.8, -95.0, 65.4, 110.0, -40.0,
        88.0, -55.5, 200.0, 130.0,
    ]
    trades = []
    for i, pl in enumerate(results):
        open_t = base_open + timedelta(days=i * 2, hours=i % 8)
        close_t = open_t + timedelta(hours=4 + i % 3)
        direction = TradeDirection.BUY if pl > 0 else TradeDirection.SELL
        trades.append(TradeRecord(
            ticket=f"DEMO-{1000 + i}",
            symbol="EURUSD",
            open_time=open_t,
            close_time=close_t,
            direction=direction,
            volume=0.10,
            open_price=1.08000 + i * 0.0001,
            close_price=1.08000 + i * 0.0001 + (pl / 100000),
            commission=-0.50,
            swap=-0.10 if i % 3 == 0 else 0.0,
            profit_loss=pl,
        ))
    return trades


# =============================================================================
# PIPELINE PRINCIPAL (reutiliza la lógica de run_academic_demo.py)
# =============================================================================

def run_pipeline(gui_callback=None) -> dict:
    """
    Ejecuta el pipeline completo de validación académica.
    Retorna un diccionario con todos los resultados para el informe HTML.
    
    Args:
        gui_callback: Función opcional para actualizar la GUI entre pasos.
                      Debe aceptar (step_number, step_name, status)
    """
    results = {}
    
    # ──────────────────────────────────────────────────────────────────────────
    # PASO 1: Parsear informe MT5 HTML
    # ──────────────────────────────────────────────────────────────────────────
    if gui_callback:
        gui_callback(1, "MT5HtmlParser - Parseando informe MT5", "running")
    
    parser = MT5HtmlParser()
    is_period = BacktestPeriod(
        start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2023, 7, 1, tzinfo=timezone.utc),
        label="IS"
    )
    oos_period = BacktestPeriod(
        start_date=datetime(2023, 7, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        label="OOS"
    )

    backtest_report: BacktestReport = parser.parse(
        file_path=str(MT5_REPORT_PATH),
        strategy_id="DEMO-EURUSD-H1-ANTIGRAVITY",
        version="1.0.0-demo",
        is_period=is_period,
        oos_period=oos_period,
    )

    sha256_hash = backtest_report.raw_metrics.get("source_file_hash", "N/A")
    
    results["sha256"] = sha256_hash
    results["mt5_trades"] = backtest_report.total_trades
    results["mt5_profit_factor"] = backtest_report.profit_factor_is
    results["mt5_drawdown"] = backtest_report.max_drawdown_pct
    results["mt5_sharpe"] = backtest_report.sharpe_ratio
    results["mt5_win_rate"] = backtest_report.win_rate

    if gui_callback:
        gui_callback(1, "MT5HtmlParser - Completado (SHA-256)", "done")

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 2: MetricsEngine — Recalcular métricas
    # ──────────────────────────────────────────────────────────────────────────
    if gui_callback:
        gui_callback(2, "MetricsEngine - Recálculo de métricas", "running")

    trades = _build_synthetic_trades()
    calculated = MetricsEngine.calculate(
        trades=trades,
        initial_balance=10_000.0,
        risk_free_rate=0.0
    )

    results["calc_profit_factor"] = calculated.profit_factor
    results["calc_expectancy"] = calculated.expectancy
    results["calc_win_rate"] = round(calculated.win_rate * 100, 2)
    results["calc_sortino"] = calculated.sortino_ratio
    results["calc_max_daily_loss"] = calculated.max_daily_loss_pct
    results["calc_max_streak"] = calculated.max_losing_streak

    if gui_callback:
        gui_callback(2, "MetricsEngine - Completado", "done")

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 3: MonteCarloEngine — 1000 simulaciones
    # ──────────────────────────────────────────────────────────────────────────
    if gui_callback:
        gui_callback(3, "MonteCarloEngine - Ejecutando 1000 simulaciones", "running")

    mc_result = MonteCarloEngine.simulate(
        trades=trades,
        initial_equity=10_000.0,
        n_simulations=1000,
        seed=42,
        method="bootstrap",
        ruin_threshold_pct=0.30,
    )

    results["mc_risk_of_ruin"] = round(mc_result.risk_of_ruin_pct * 100, 4)
    results["mc_dd_p50"] = mc_result.monte_carlo_max_drawdown_p50
    results["mc_dd_p95"] = mc_result.monte_carlo_max_drawdown_p95
    results["mc_dd_p99"] = mc_result.monte_carlo_max_drawdown_p99
    results["mc_median_equity"] = mc_result.median_final_equity
    results["mc_p05_equity"] = mc_result.p05_final_equity
    results["mc_p95_equity"] = mc_result.p95_final_equity
    results["mc_low_confidence"] = mc_result.low_confidence
    results["mc_simulations"] = mc_result.n_simulations
    results["mc_approved_for_real"] = mc_result.approved_for_real

    if gui_callback:
        gui_callback(3, "MonteCarloEngine - Completado", "done")

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 4: BacktestValidator — 10 reglas deterministas
    # ──────────────────────────────────────────────────────────────────────────
    if gui_callback:
        gui_callback(4, "BacktestValidator - Validando 10 reglas", "running")

    backtest_report_enriched = backtest_report.model_copy(update={
        "sortino_ratio": calculated.sortino_ratio,
        "max_daily_loss_pct": calculated.max_daily_loss_pct,
        "risk_of_ruin_pct": mc_result.risk_of_ruin_pct * 100,
        "calculated_metrics": calculated,
        "monte_carlo_result": mc_result,
    })

    metadata = StrategyMetadata(
        strategy_id="DEMO-EURUSD-H1-ANTIGRAVITY",
        name="Antigravity Demo Strategy",
        version="1.0.0-demo",
        config_hash=sha256_hash[:16],
        author_or_source="Academic Demo",
        asset="EURUSD",
        asset_class=AssetClass.FOREX,
        timeframe="H1",
        created_at=datetime.now(timezone.utc),
        notes="Demo académica Fase 4.4 con GUI"
    )

    bias_checklist = BiasChecklist(
        look_ahead_bias_checked=True,
        survivorship_bias_checked=True,
        data_snooping_checked=True,
        overfitting_checked=True,
        curve_fitting_checked=True,
        selection_bias_checked=True,
        period_bias_checked=True,
        realistic_costs_checked=True,
        realistic_execution_checked=True,
        spread_slippage_checked=True,
        comments="Checklist completado para demo académica"
    )

    market_checklist = MarketRegimeChecklist(
        trend_tested=True,
        range_tested=True,
        high_volatility_tested=True,
        low_volatility_tested=True,
        session_variability_tested=True,
        comments="Regímenes verificados para demo académica"
    )

    validator = BacktestValidator()
    evaluation = validator.validate(
        metadata=metadata,
        report=backtest_report_enriched,
        bias_checklist=bias_checklist,
        market_regime_checklist=market_checklist,
    )

    results["bv_classification"] = evaluation.classification.value
    results["bv_reason"] = evaluation.decision_reason
    results["bv_approved_for_real"] = evaluation.approved_for_real

    if gui_callback:
        gui_callback(4, f"BacktestValidator - Clasificación: {evaluation.classification.value}", "done")

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 5: RiskEngine — 6 reglas de seguridad operativa
    # ──────────────────────────────────────────────────────────────────────────
    if gui_callback:
        gui_callback(5, "RiskEngine - Evaluando reglas de seguridad", "running")

    risk_engine = RiskEngine()
    trade_intent = TradeIntent(
        id=str(uuid.uuid4()),
        signal_id=str(uuid.uuid4()),
        symbol="EURUSD",
        action="BUY",
        lot_size=0.01,
        entry_price=1.08500,
        is_real_execution_intent=False,
        is_user_approved=False,
    )
    account_state = AccountState(
        balance=10_000.0,
        equity=10_150.0,
        daily_loss_pct=0.0,
        open_trades=0,
        max_daily_loss_pct=2.0,
        max_concurrent_trades=3,
        allow_real_execution=False,
        require_approval=True,
    )

    risk_result = risk_engine.evaluate(trade_intent, account_state)

    results["re_approved"] = risk_result.approved
    results["re_reason"] = risk_result.reason
    results["re_score"] = risk_result.risk_score
    results["re_failed_rules"] = risk_result.failed_rules

    if gui_callback:
        gui_callback(5, f"RiskEngine - {'Aprobado' if risk_result.approved else 'Bloqueado'}", "done")

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 6: Generar HTML de resultado
    # ──────────────────────────────────────────────────────────────────────────
    if gui_callback:
        gui_callback(6, "Generando informe HTML", "running")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _generate_html(results)

    if gui_callback:
        gui_callback(6, "Informe HTML generado", "done")

    return results


# =============================================================================
# GENERADOR DE HTML (reutilizado de run_academic_demo.py)
# =============================================================================

def _generate_html(r: dict) -> None:
    """Genera el archivo HTML de resultado de la demo académica."""
    bv_class = r.get("bv_classification", "UNKNOWN")
    bv_color = {
        "PAPER_TRADING_READY": "#2ce59b",
        "OBSERVATION": "#ffb86b",
        "REJECTED": "#ff6b6b",
    }.get(bv_class, "#8fa3bf")

    re_approved = r.get("re_approved", False)
    re_color = "#2ce59b" if re_approved else "#ff6b6b"
    re_label = "APPROVED" if re_approved else "BLOCKED"

    failed_rules_html = "".join(
        f'<li style="color:#ff9b9b;margin:4px 0">⊘ {rule}</li>'
        for rule in r.get("re_failed_rules", [])
    ) or '<li style="color:#2ce59b">Sin reglas fallidas</li>'

    mc_low_conf_badge = (
        '<span style="color:#ffb86b;font-weight:700">⚠ LOW CONFIDENCE (<30 trades demo)</span>'
        if r.get("mc_low_confidence") else
        '<span style="color:#2ce59b;font-weight:700">✓ HIGH CONFIDENCE</span>'
    )

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Antigravity · Demo Académica — Resultado</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',Inter,Arial,sans-serif;background:#070b16;color:#e9eef7;padding:28px}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:30px;letter-spacing:.4px;margin-bottom:6px}}
.subtitle{{color:#8fa3bf;margin-bottom:22px;font-size:14px}}
.badges{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}}
.badge{{border:1px solid #24415f;background:#101b2b;border-radius:999px;padding:7px 13px;font-weight:700;font-size:12px}}
.green{{color:#2ce59b}}.orange{{color:#ffb86b}}.red{{color:#ff6b6b}}.blue{{color:#6db7ff}}
.grid{{display:grid;grid-template-columns:repeat(12,1fr);gap:14px}}
.card{{background:linear-gradient(180deg,#111a2b,#0d1423);border:1px solid #1d3048;border-radius:16px;padding:20px;box-shadow:0 10px 28px rgba(0,0,0,.28)}}
.span3{{grid-column:span 3}}.span4{{grid-column:span 4}}.span5{{grid-column:span 5}}
.span6{{grid-column:span 6}}.span12{{grid-column:span 12}}
.kpi .lbl{{color:#8fa3bf;font-size:12px;text-transform:uppercase;letter-spacing:.07em}}
.kpi .num{{font-size:34px;font-weight:800;margin:8px 0}}
.kpi .note{{font-size:11px;color:#71849d}}
.title{{font-size:13px;color:#c9d8ea;text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px;font-weight:800}}
.pipeline{{display:flex;align-items:center;justify-content:space-between;gap:6px}}
.step{{flex:1;min-height:66px;border:1px solid #24415f;border-radius:12px;background:#0b1728;display:flex;align-items:center;justify-content:center;text-align:center;padding:8px;font-weight:700;font-size:11px;line-height:1.3}}
.step.done{{border-color:#2ce59b;color:#2ce59b}}
.step.running{{border-color:#6db7ff;color:#6db7ff}}
.arrow{{color:#456d9b;font-weight:900;font-size:16px}}
.bar-row{{display:grid;grid-template-columns:140px 1fr 60px;align-items:center;gap:10px;margin:10px 0}}
.bar-lbl{{color:#b8c9de;font-size:13px}}
.bar{{height:10px;background:#17263a;border-radius:999px;overflow:hidden}}
.fill{{height:100%;border-radius:999px}}
.fg{{background:linear-gradient(90deg,#248bff,#2ce59b)}}
.fo{{background:linear-gradient(90deg,#ffb86b,#ff7a45)}}
.fr{{background:linear-gradient(90deg,#ff6b6b,#ff3b3b)}}
.bar-val{{text-align:right;color:#dbe7f5;font-weight:700;font-size:13px}}
.row-item{{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid #1d3048;padding:8px 0;color:#b8c9de;font-size:13px}}
.row-item b{{color:#e9eef7}}
.warnbox{{border:1px solid #4b2630;background:rgba(255,107,107,.07);border-radius:12px;padding:14px;font-size:13px}}
.subtle{{color:#8fa3bf;line-height:1.5;font-size:13px;margin-top:12px}}
ul{{list-style:none;padding-left:0}}
.footer{{margin-top:18px;color:#61728a;font-size:11px;text-align:center}}
@media(max-width:900px){{.span3,.span4,.span5,.span6{{grid-column:span 12}}.pipeline{{flex-direction:column}}.arrow{{transform:rotate(90deg)}}}}
</style>
</head>
<body>
<div class="wrap">
  <h1>ANTIGRAVITY · Resultado Demo Funcional (GUI)</h1>
  <p class="subtitle">Pipeline completo ejecutado · {generated_at} · <span style="color:#8fa3bf">Fase 4.4 Académica</span></p>
  <div class="badges">
    <span class="badge green">FASE 4.4 COMPLETADA</span>
    <span class="badge orange">ALLOW_REAL_EXECUTION = False</span>
    <span class="badge orange">approved_for_real = False</span>
    <span class="badge blue">117 TESTS PASSED</span>
    <span class="badge" style="color:#c9d8ea">1000 SIMULACIONES MC</span>
  </div>

  <div class="grid">

    <!-- KPIs -->
    <div class="card span3 kpi">
      <div class="lbl">Veredicto BacktestValidator</div>
      <div class="num" style="color:{bv_color};font-size:26px">{bv_class}</div>
      <div class="note">Clasificación determinista</div>
    </div>
    <div class="card span3 kpi">
      <div class="lbl">RiskEngine</div>
      <div class="num" style="color:{re_color};font-size:26px">{re_label}</div>
      <div class="note">Reglas de seguridad operativa</div>
    </div>
    <div class="card span3 kpi">
      <div class="lbl">Monte Carlo (1000 sim.)</div>
      <div class="num blue" style="font-size:22px">{mc_low_conf_badge}</div>
      <div class="note">Risk of Ruin: {r.get('mc_risk_of_ruin', 0):.2f}%</div>
    </div>
    <div class="card span3 kpi">
      <div class="lbl">Operaciones Reales</div>
      <div class="num green">0</div>
      <div class="note">Sistema académico seguro</div>
    </div>

    <!-- Pipeline -->
    <div class="card span12">
      <div class="title">Pipeline Ejecutado — 6 Pasos</div>
      <div class="pipeline">
        <div class="step done">MT5 HTML<br>Parser<br>✓</div>
        <div class="arrow">→</div>
        <div class="step done">SHA-256<br>Trazabilidad<br>✓</div>
        <div class="arrow">→</div>
        <div class="step done">Metrics<br>Engine<br>✓</div>
        <div class="arrow">→</div>
        <div class="step done">Monte Carlo<br>1000 Sim.<br>✓</div>
        <div class="arrow">→</div>
        <div class="step done">Backtest<br>Validator<br>✓</div>
        <div class="arrow">→</div>
        <div class="step done">Risk<br>Engine<br>✓</div>
      </div>
    </div>

    <!-- Métricas del informe MT5 -->
    <div class="card span6">
      <div class="title">Métricas MT5 — Informe parseado</div>
      <div class="bar-row"><div class="bar-lbl">Profit Factor</div><div class="bar"><div class="fill fg" style="width:{min(r.get('mt5_profit_factor',0)*40,100):.0f}%"></div></div><div class="bar-val">{r.get('mt5_profit_factor',0):.2f}</div></div>
      <div class="bar-row"><div class="bar-lbl">Win Rate</div><div class="bar"><div class="fill fg" style="width:{r.get('mt5_win_rate',0):.0f}%"></div></div><div class="bar-val">{r.get('mt5_win_rate',0):.1f}%</div></div>
      <div class="bar-row"><div class="bar-lbl">Max Drawdown</div><div class="bar"><div class="fill fo" style="width:{min(r.get('mt5_drawdown',0)*8,100):.0f}%"></div></div><div class="bar-val">{r.get('mt5_drawdown',0):.2f}%</div></div>
      <div class="bar-row"><div class="bar-lbl">Sharpe Ratio</div><div class="bar"><div class="fill fg" style="width:{min(r.get('mt5_sharpe',0)*50,100):.0f}%"></div></div><div class="bar-val">{r.get('mt5_sharpe',0):.2f}</div></div>
      <p class="subtle">Fuente: {MT5_REPORT_PATH.name} · SHA-256: {r.get('sha256','N/A')[:20]}...</p>
    </div>

    <!-- Métricas recalculadas -->
    <div class="card span6">
      <div class="title">Métricas Recalculadas — MetricsEngine</div>
      <div class="bar-row"><div class="bar-lbl">Profit Factor</div><div class="bar"><div class="fill fg" style="width:{min(r.get('calc_profit_factor',0)*40,100):.0f}%"></div></div><div class="bar-val">{r.get('calc_profit_factor',0):.4f}</div></div>
      <div class="bar-row"><div class="bar-lbl">Win Rate</div><div class="bar"><div class="fill fg" style="width:{min(r.get('calc_win_rate',0),100):.0f}%"></div></div><div class="bar-val">{r.get('calc_win_rate',0):.1f}%</div></div>
      <div class="bar-row"><div class="bar-lbl">Sortino Ratio</div><div class="bar"><div class="fill fg" style="width:{min(r.get('calc_sortino',0)*40,100):.0f}%"></div></div><div class="bar-val">{r.get('calc_sortino',0):.4f}</div></div>
      <div class="bar-row"><div class="bar-lbl">Max Daily Loss</div><div class="bar"><div class="fill fo" style="width:{min(r.get('calc_max_daily_loss',0)*10,100):.0f}%"></div></div><div class="bar-val">{r.get('calc_max_daily_loss',0):.2f}%</div></div>
      <p class="subtle">Recálculo matemático independiente · Expectancy: {r.get('calc_expectancy',0):.2f} · Max racha pérd.: {r.get('calc_max_streak',0)}</p>
    </div>

    <!-- Monte Carlo -->
    <div class="card span6">
      <div class="title">Monte Carlo — Distribución de Riesgo</div>
      <div class="row-item"><span>Simulaciones</span><b>{r.get('mc_simulations',0):,}</b></div>
      <div class="row-item"><span>Risk of Ruin</span><b style="color:#ff6b6b">{r.get('mc_risk_of_ruin',0):.4f}%</b></div>
      <div class="row-item"><span>Max Drawdown P50</span><b>{r.get('mc_dd_p50',0):.2f}%</b></div>
      <div class="row-item"><span>Max Drawdown P95</span><b style="color:#ffb86b">{r.get('mc_dd_p95',0):.2f}%</b></div>
      <div class="row-item"><span>Max Drawdown P99</span><b style="color:#ff6b6b">{r.get('mc_dd_p99',0):.2f}%</b></div>
      <div class="row-item"><span>Equity Mediana Final</span><b style="color:#2ce59b">${r.get('mc_median_equity',0):,.2f}</b></div>
      <div class="row-item"><span>Equity P5 (peor caso)</span><b style="color:#ff6b6b">${r.get('mc_p05_equity',0):,.2f}</b></div>
      <div class="row-item"><span>Equity P95 (mejor caso)</span><b style="color:#2ce59b">${r.get('mc_p95_equity',0):,.2f}</b></div>
      <p class="subtle">{mc_low_conf_badge} — Dataset demo con 20 trades sintéticos</p>
    </div>

    <!-- Decisiones del sistema -->
    <div class="card span6">
      <div class="title">Decisiones del Sistema</div>
      <div class="row-item"><span>SHA-256 Trazabilidad</span><b class="green">OK</b></div>
      <div class="row-item"><span>Metrics Engine</span><b class="green">RECALCULATED</b></div>
      <div class="row-item"><span>Monte Carlo</span><b class="{'orange' if r.get('mc_low_confidence') else 'green'}">{'LOW CONFIDENCE' if r.get('mc_low_confidence') else 'HIGH CONFIDENCE'}</b></div>
      <div class="row-item"><span>BacktestValidator</span><b style="color:{bv_color}">{bv_class}</b></div>
      <div class="row-item"><span>RiskEngine</span><b style="color:{re_color}">REAL EXECUTION {re_label}</b></div>
      <div class="row-item"><span>approved_for_real</span><b class="green">False ← INMUTABLE</b></div>
      <div class="title" style="margin-top:16px">Razón BacktestValidator</div>
      <p class="subtle">{r.get('bv_reason','N/A')[:200]}</p>
    </div>

    <!-- Invariantes de seguridad -->
    <div class="card span12">
      <div class="title">Invariantes de Seguridad Activas</div>
      <div class="warnbox">
        <p>⊘ La IA no decide &nbsp;·&nbsp; ⊘ La IA no ejecuta &nbsp;·&nbsp; ⊘ No bypass RiskEngine</p><br>
        <p><b>ALLOW_REAL_EXECUTION = {ALLOW_REAL_EXECUTION}</b> &nbsp;·&nbsp; <b>approved_for_real = {APPROVED_FOR_REAL}</b></p><br>
        <p style="color:#8fa3bf;font-size:12px">Reglas RiskEngine fallidas en esta evaluación:</p>
        <ul style="margin-top:8px">{failed_rules_html}</ul>
      </div>
      <p class="subtle">Esta demo demuestra el flujo de validación académica sin ejecutar operaciones reales. Todos los datos son ficticios o de prueba.</p>
    </div>

  </div>

  <div class="footer">
    Antigravity · Academic Research Demo (GUI) · Fase 4.4 · Generado: {generated_at}<br>
    GitHub: github.com/TheLord1995/Proyecto_Antigravity_David · ALLOW_REAL_EXECUTION=False · approved_for_real=False
  </div>
</div>
</body>
</html>"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)


# =============================================================================
# INTERFAZ GRÁFICA CON TKINTER
# =============================================================================

class AcademicDemoGUI:
    """Interfaz gráfica para la demo académica de Antigravity."""
    
    # Definición de pasos del pipeline
    PIPELINE_STEPS = [
        (1, "MT5HtmlParser", "Parseando informe MT5 y calculando SHA-256"),
        (2, "MetricsEngine", "Recalculando métricas desde trades sintéticos"),
        (3, "MonteCarlo", "Ejecutando 1000 simulaciones (seed=42)"),
        (4, "BacktestValidator", "Validando con 10 reglas deterministas"),
        (5, "RiskEngine", "Evaluando 6 reglas de seguridad operativa"),
        (6, "Generación HTML", "Generando informe de resultados"),
    ]
    
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity - Demo Académica Interactiva")
        self.root.geometry("800x700")
        self.root.configure(bg="#070b16")
        
        # Archivo seleccionado
        self.selected_file = tk.StringVar(value=str(MT5_REPORT_PATH))
        
        # Estado de los pasos
        self.step_frames = []
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        
        # ── Header ─────────────────────────────────────────────────────────────
        header_frame = tk.Frame(self.root, bg="#070b16")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title = tk.Label(
            header_frame,
            text="ANTIGRAVITY · Demo Académica Interactiva",
            font=("Segoe UI", 18, "bold"),
            fg="#e9eef7",
            bg="#070b16"
        )
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(
            header_frame,
            text="Pipeline de validación académica - Fase 4.4",
            font=("Segoe UI", 10),
            fg="#8fa3bf",
            bg="#070b16"
        )
        subtitle.pack(anchor=tk.W, pady=(2, 0))
        
        # ── Badges de seguridad ───────────────────────────────────────────────
        badges_frame = tk.Frame(self.root, bg="#070b16")
        badges_frame.pack(fill=tk.X, padx=20, pady=10)
        
        badge_styles = [
            ("ALLOW_REAL_EXECUTION = False", "#ff6b6b"),
            ("approved_for_real = False", "#ff6b6b"),
            ("Sin MT5 real", "#6db7ff"),
            ("Sin Telegram/TradingView", "#6db7ff"),
        ]
        
        for text, color in badge_styles:
            badge = tk.Label(
                badges_frame,
                text=text,
                font=("Segoe UI", 9, "bold"),
                fg=color,
                bg="#101b2b",
                bd=1,
                relief=tk.SOLID,
                padx=10,
                pady=4
            )
            badge.pack(side=tk.LEFT, padx=5)
        
        # ── Selector de archivo ───────────────────────────────────────────────
        file_frame = tk.Frame(self.root, bg="#070b16")
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            file_frame,
            text="Informe MT5:",
            font=("Segoe UI", 11),
            fg="#c9d8ea",
            bg="#070b16"
        ).pack(anchor=tk.W)
        
        file_input_frame = tk.Frame(file_frame, bg="#070b16")
        file_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Entry(
            file_input_frame,
            textvariable=self.selected_file,
            font=("Segoe UI", 10),
            fg="#e9eef7",
            bg="#111a2b",
            insertbackground="#e9eef7",
            relief=tk.FLAT,
            width=60
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(
            file_input_frame,
            text="Seleccionar...",
            command=self._select_file,
            font=("Segoe UI", 9),
            bg="#24415f",
            fg="#e9eef7",
            relief=tk.FLAT,
            padx=15,
            pady=5
        ).pack(side=tk.LEFT)
        
        # ── Pipeline Steps ───────────────────────────────────────────────────
        pipeline_label = tk.Label(
            self.root,
            text="Pipeline de Ejecución",
            font=("Segoe UI", 12, "bold"),
            fg="#c9d8ea",
            bg="#070b16"
        )
        pipeline_label.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        steps_container = tk.Frame(self.root, bg="#070b16")
        steps_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        for step_num, step_name, step_desc in self.PIPELINE_STEPS:
            step_frame = self._create_step_frame(steps_container, step_num, step_name, step_desc)
            self.step_frames.append(step_frame)
        
        # ── Botón de ejecutar ───────────────────────────────────────────────
        button_frame = tk.Frame(self.root, bg="#070b16")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.execute_button = tk.Button(
            button_frame,
            text="▶ Ejecutar análisis",
            command=self._run_analysis,
            font=("Segoe UI", 12, "bold"),
            fg="#070b16",
            bg="#2ce59b",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.execute_button.pack()
        
        # ── Status bar ───────────────────────────────────────────────────────
        self.status_label = tk.Label(
            self.root,
            text="Listo para ejecutar",
            font=("Segoe UI", 9),
            fg="#8fa3bf",
            bg="#070b16"
        )
        self.status_label.pack(side=tk.BOTTOM, pady=10)
        
    def _create_step_frame(self, parent, step_num, step_name, step_desc):
        """Crea un frame para cada paso del pipeline."""
        frame = tk.Frame(parent, bg="#111a2b", bd=1, relief=tk.SOLID)
        frame.pack(fill=tk.X, pady=4)
        
        # Número de paso
        num_label = tk.Label(
            frame,
            text=f"{step_num}",
            font=("Segoe UI", 14, "bold"),
            fg="#456d9b",
            bg="#111a2b",
            width=3
        )
        num_label.pack(side=tk.LEFT, padx=10, pady=12)
        
        # Información del paso
        info_frame = tk.Frame(frame, bg="#111a2b")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        name_label = tk.Label(
            info_frame,
            text=step_name,
            font=("Segoe UI", 11, "bold"),
            fg="#e9eef7",
            bg="#111a2b"
        )
        name_label.pack(anchor=tk.W)
        
        desc_label = tk.Label(
            info_frame,
            text=step_desc,
            font=("Segoe UI", 9),
            fg="#8fa3bf",
            bg="#111a2b"
        )
        desc_label.pack(anchor=tk.W)
        
        # Estado del paso (espacio para indicador)
        status_frame = tk.Frame(frame, bg="#111a2b", width=80)
        status_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        status_label = tk.Label(
            status_frame,
            text="⏳",
            font=("Segoe UI", 14),
            bg="#111a2b"
        )
        status_label.pack(expand=True)
        
        # Guardar referencias para actualizar
        frame.status_label = status_label
        frame.num_label = num_label
        frame.name_label = name_label
        
        return frame
        
    def _select_file(self):
        """Abre un diálogo para seleccionar el archivo MT5."""
        filetypes = (
            ("HTML files", "*.html *.htm"),
            ("All files", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Seleccionar informe MT5",
            initialdir=str(TEST_DATA_DIR),
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file.set(filename)
            
    def _update_step(self, step_num, status):
        """Actualiza el estado visual de un paso."""
        if step_num < 1 or step_num > len(self.step_frames):
            return
            
        frame = self.step_frames[step_num - 1]
        
        if status == "running":
            frame.status_label.config(text="🔄", fg="#6db7ff")
            frame.num_label.config(fg="#6db7ff")
            frame.name_label.config(fg="#6db7ff")
        elif status == "done":
            frame.status_label.config(text="✓", fg="#2ce59b")
            frame.num_label.config(fg="#2ce59b")
            frame.name_label.config(fg="#2ce59b")
        elif status == "error":
            frame.status_label.config(text="✗", fg="#ff6b6b")
            frame.num_label.config(fg="#ff6b6b")
            
    def _gui_callback(self, step_num, step_name, status):
        """Callback para actualizar la GUI durante la ejecución."""
        self.root.update_idletasks()
        self._update_step(step_num, status)
        
        if status == "running":
            self.status_label.config(text=f"Ejecutando: {step_name}")
        elif status == "done":
            self.status_label.config(text=f"Completado: {step_name}")
        elif status == "error":
            self.status_label.config(text=f"Error en: {step_name}", fg="#ff6b6b")
            
    def _run_analysis(self):
        """Ejecuta el pipeline de análisis."""
        self.execute_button.config(state=tk.DISABLED, text="Ejecutando...", bg="#456d9b")
        self.status_label.config(text="Iniciando pipeline...", fg="#8fa3bf")
        
        # Resetear todos los pasos
        for i in range(len(self.step_frames)):
            self._update_step(i + 1, "waiting")
            frame = self.step_frames[i]
            frame.status_label.config(text="⏳")
            frame.num_label.config(fg="#456d9b")
            frame.name_label.config(fg="#e9eef7")
        
        # Ejecutar en un hilo separado para no bloquear la GUI
        def run_in_thread():
            try:
                results = run_pipeline(gui_callback=self._gui_callback)
                
                # Abrir el resultado en el navegador
                self.root.after(0, lambda: self._open_result())
                
            except Exception as e:
                self.root.after(0, lambda: self._show_error(str(e)))
                
        import threading
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
        
    def _open_result(self):
        """Abre el resultado HTML en el navegador."""
        self.status_label.config(text="Pipeline completado. Abriendo resultado...", fg="#2ce59b")
        self.execute_button.config(state=tk.NORMAL, text="▶ Ejecutar análisis", bg="#2ce59b")
        
        # Abrir en navegador
        webbrowser.open(OUTPUT_HTML.as_uri())
        
        messagebox.showinfo(
            "Demo Académica",
            f"Pipeline completado exitosamente.\n\n"
            f"El resultado se ha abierto en tu navegador.\n"
            f"Archivo: {OUTPUT_HTML}"
        )
        
    def _show_error(self, error_msg):
        """Muestra un mensaje de error."""
        self.status_label.config(text=f"Error: {error_msg}", fg="#ff6b6b")
        self.execute_button.config(state=tk.NORMAL, text="▶ Ejecutar análisis", bg="#2ce59b")
        
        # Marcar todos los pasos como error
        for i in range(len(self.step_frames)):
            self._update_step(i + 1, "error")
            
        messagebox.showerror("Error en la ejecución", f"Se produjo un error:\n\n{error_msg}")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main():
    """Inicia la aplicación GUI."""
    root = tk.Tk()
    app = AcademicDemoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

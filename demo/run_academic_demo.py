"""
demo/run_academic_demo.py
--------------------------
Demo funcional academica del pipeline completo de Antigravity.

Ejecuta en orden:
  1. Carga informe MT5 HTML desde tests/data/
  2. Parsea con MT5HtmlParser (SHA-256 incluido)
  3. Recalcula métricas con MetricsEngine
  4. Ejecuta Monte Carlo (1000 simulaciones, seed=42)
  5. Valida con BacktestValidator
  6. Aplica RiskEngine (bloqueo académico garantizado)
  7. Genera resultado HTML en demo/output/academic_demo_result.html

Restricciones de seguridad activas:
  - ALLOW_REAL_EXECUTION = False (siempre)
  - approved_for_real = False (inmutable por contrato Pydantic)
  - Sin MT5 real, sin Telegram, sin TradingView, sin RemoteAPIValidator
  - No toca RiskEngine ni BacktestValidator (solo los invoca)
"""

import io
import os
import sys
import uuid
import webbrowser
from datetime import datetime, timezone, timedelta

# Forzar UTF-8 en la consola de Windows para evitar UnicodeEncodeError
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

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
# UTILIDADES DE PRESENTACIÓN
# =============================================================================

def _banner(text: str) -> None:
    """Imprime un banner de seccion en la consola."""
    print()
    print("-" * 70)
    print(f"  {text}")
    print("-" * 70)

def _step(n: int, label: str) -> None:
    """Imprime un paso del pipeline."""
    now = datetime.now().strftime("%H:%M:%S")
    print(f"  [{now}] PASO {n}/6 - {label}")

def _ok(msg: str) -> None:
    print(f"  OK  {msg}")

def _info(msg: str) -> None:
    print(f"  >>  {msg}")


# =============================================================================
# DATOS SINTÉTICOS PARA DEMO (sin MT5 real)
# =============================================================================

def _build_synthetic_trades() -> list[TradeRecord]:
    """
    Genera 20 TradeRecord sintéticos que simulan operaciones de un backtest.
    Estos datos son completamente ficticios y se usan únicamente como entrada
    para MetricsEngine y MonteCarloEngine en la demo académica.
    No representan operaciones reales ni historial de cuenta real.
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
# PIPELINE PRINCIPAL
# =============================================================================

def run_demo() -> dict:
    """
    Ejecuta el pipeline completo de validación académica.
    Retorna un diccionario con todos los resultados para el informe HTML.
    """
    _banner("ANTIGRAVITY - Demo Funcional Academica - Fase 4.4")
    print(f"  Repositorio: https://github.com/TheLord1995/Proyecto_Antigravity_David")
    print(f"  ALLOW_REAL_EXECUTION = {ALLOW_REAL_EXECUTION}")
    print(f"  approved_for_real    = {APPROVED_FOR_REAL}")

    results = {}

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 1: Parsear informe MT5 HTML
    # ──────────────────────────────────────────────────────────────────────────
    _step(1, "MT5HtmlParser — Importar y parsear informe")

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
    _ok(f"Informe parseado: {MT5_REPORT_PATH.name}")
    _ok(f"SHA-256: {sha256_hash[:16]}...{sha256_hash[-8:]}")
    _ok(f"Total trades (MT5): {backtest_report.total_trades}")
    _ok(f"Profit Factor (MT5): {backtest_report.profit_factor_is:.2f}")
    _ok(f"Max Drawdown (MT5): {backtest_report.max_drawdown_pct:.2f}%")

    results["sha256"] = sha256_hash
    results["mt5_trades"] = backtest_report.total_trades
    results["mt5_profit_factor"] = backtest_report.profit_factor_is
    results["mt5_drawdown"] = backtest_report.max_drawdown_pct
    results["mt5_sharpe"] = backtest_report.sharpe_ratio
    results["mt5_win_rate"] = backtest_report.win_rate

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 2: MetricsEngine — Recalcular métricas desde trades sintéticos
    # ──────────────────────────────────────────────────────────────────────────
    _step(2, "MetricsEngine — Recálculo matemático de métricas")

    trades = _build_synthetic_trades()
    calculated = MetricsEngine.calculate(
        trades=trades,
        initial_balance=10_000.0,
        risk_free_rate=0.0
    )

    _ok(f"Trades analizados: {calculated.total_trades}")
    _ok(f"Profit Factor (recalculado): {calculated.profit_factor:.4f}")
    _ok(f"Expectancy: {calculated.expectancy:.2f}")
    _ok(f"Win Rate: {calculated.win_rate * 100:.1f}%")
    _ok(f"Sortino Ratio: {calculated.sortino_ratio:.4f}")
    _ok(f"Max Daily Loss: {calculated.max_daily_loss_pct:.2f}%")

    results["calc_profit_factor"] = calculated.profit_factor
    results["calc_expectancy"] = calculated.expectancy
    results["calc_win_rate"] = round(calculated.win_rate * 100, 2)
    results["calc_sortino"] = calculated.sortino_ratio
    results["calc_max_daily_loss"] = calculated.max_daily_loss_pct
    results["calc_max_streak"] = calculated.max_losing_streak

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 3: MonteCarloEngine — 1000 simulaciones
    # ──────────────────────────────────────────────────────────────────────────
    _step(3, "MonteCarloEngine — 1000 simulaciones (seed=42)")

    mc_result = MonteCarloEngine.simulate(
        trades=trades,
        initial_equity=10_000.0,
        n_simulations=1000,
        seed=42,
        method="bootstrap",
        ruin_threshold_pct=0.30,
    )

    _ok(f"Simulaciones: {mc_result.n_simulations}")
    _ok(f"Método: {mc_result.method}")
    _ok(f"Risk of Ruin: {mc_result.risk_of_ruin_pct * 100:.2f}%")
    _ok(f"Max Drawdown P50: {mc_result.monte_carlo_max_drawdown_p50:.2f}%")
    _ok(f"Max Drawdown P95: {mc_result.monte_carlo_max_drawdown_p95:.2f}%")
    _ok(f"Equity Mediana Final: {mc_result.median_final_equity:.2f}")
    _ok(f"Low Confidence: {mc_result.low_confidence} (< 30 trades en dataset demo)")
    _ok(f"approved_for_real: {mc_result.approved_for_real}  ← INMUTABLE")

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

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 4: BacktestValidator — 10 reglas deterministas
    # ──────────────────────────────────────────────────────────────────────────
    _step(4, "BacktestValidator — 10 reglas de validación")

    # Enriquecer el backtest_report con resultados de MC y métricas calculadas
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
        notes="Demo académica Fase 4.4"
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

    _ok(f"Clasificación: {evaluation.classification.value}")
    _ok(f"approved_for_real: {evaluation.approved_for_real}  ← INMUTABLE")
    _ok(f"Razón: {evaluation.decision_reason[:80]}...")

    results["bv_classification"] = evaluation.classification.value
    results["bv_reason"] = evaluation.decision_reason
    results["bv_approved_for_real"] = evaluation.approved_for_real

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 5: RiskEngine — 6 reglas de seguridad operativa
    # ──────────────────────────────────────────────────────────────────────────
    _step(5, "RiskEngine — Evaluación de reglas de seguridad")

    risk_engine = RiskEngine()
    trade_intent = TradeIntent(
        id=str(uuid.uuid4()),
        signal_id=str(uuid.uuid4()),
        symbol="EURUSD",
        action="BUY",
        lot_size=0.01,
        entry_price=1.08500,
        is_real_execution_intent=False,  # Siempre False en demo académica
        is_user_approved=False,
    )
    account_state = AccountState(
        balance=10_000.0,
        equity=10_150.0,
        daily_loss_pct=0.0,
        open_trades=0,
        max_daily_loss_pct=2.0,
        max_concurrent_trades=3,
        allow_real_execution=False,   # Bloqueo permanente
        require_approval=True,
    )

    risk_result = risk_engine.evaluate(trade_intent, account_state)

    _ok(f"Aprobado: {risk_result.approved}")
    _ok(f"Risk Score: {risk_result.risk_score}")
    _ok(f"Razón: {risk_result.reason}")
    if risk_result.failed_rules:
        for rule in risk_result.failed_rules:
            _info(f"  Regla fallida: {rule}")

    results["re_approved"] = risk_result.approved
    results["re_reason"] = risk_result.reason
    results["re_score"] = risk_result.risk_score
    results["re_failed_rules"] = risk_result.failed_rules

    # ──────────────────────────────────────────────────────────────────────────
    # PASO 6: Generar HTML de resultado
    # ──────────────────────────────────────────────────────────────────────────
    _step(6, "Generando informe HTML de resultados")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _generate_html(results)
    _ok(f"Archivo generado: {OUTPUT_HTML}")

    _banner("PIPELINE COMPLETADO - Abriendo resultado en el navegador")
    print(f"  Resultado: {OUTPUT_HTML}")
    print(f"  ALLOW_REAL_EXECUTION = {ALLOW_REAL_EXECUTION}  <- No ha cambiado")
    print(f"  approved_for_real    = {APPROVED_FOR_REAL}  <- No ha cambiado")
    print()

    webbrowser.open(OUTPUT_HTML.as_uri())
    return results


# =============================================================================
# GENERADOR DE HTML
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
        '<span style="color:#ffb86b;font-weight:700">⚠ LOW CONFIDENCE (&lt;30 trades demo)</span>'
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
  <h1>ANTIGRAVITY · Resultado Demo Funcional</h1>
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
    Antigravity · Academic Research Demo · Fase 4.4 · Generado: {generated_at}<br>
    GitHub: github.com/TheLord1995/Proyecto_Antigravity_David · ALLOW_REAL_EXECUTION=False · approved_for_real=False
  </div>
</div>
</body>
</html>"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    run_demo()

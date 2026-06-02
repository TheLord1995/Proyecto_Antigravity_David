# Final Project Report: Proyecto Antigravity

**Date:** 2026-06-02
**Course / Delivery:** Academic Final Project
**Version:** 1.4.0 (Phase 4.4 Completed)

## 1. Executive Summary
The Antigravity Project is an academic algorithmic trading ecosystem heavily focused on risk management, deterministic validation, and software architecture. Its primary goal is to provide a unified pipeline that imports backtest reports, mathematically recalculates their metrics to avoid tampering, runs stochastic simulations (Monte Carlo), applies strict deterministic risk rules (RiskEngine), and prepares an explanation using an adapter-based AI layer. 

Crucially, **the system does not execute real trades**. `ALLOW_REAL_EXECUTION` is permanently set to `False` across the entire codebase to preserve the academic and safe nature of the project.

## 2. Project Architecture & Pipeline
The ecosystem follows a strict unidirectional data flow:
1. **Signal Parser (MT5 HTML Parser):** Ingests raw MetaTrader 5 HTML reports, sanitizes the data, and generates a SHA-256 cryptographic signature to ensure file integrity.
2. **Metrics Engine:** Recalculates complex metrics independently (e.g., Expectancy, Sortino Ratio, Max Daily Loss, Consecutive Streaks) rather than trusting the imported data.
3. **Monte Carlo & Risk of Ruin:** Evaluates the statistical robustness of the strategy by applying Bootstrap and Shuffle resampling techniques, flagging strategies with low confidence.
4. **BacktestValidator:** A logical evaluator that assigns a classification (`PAPER_TRADING_READY`, `OBSERVATION`, `REJECTED`) based on the computed metrics and the Monte Carlo confidence flag (Rule D4).
5. **AI Validator (Contracts & Adapters Phase):** A conceptual AI layer implemented via the `AIValidatorAdapter` pattern. Currently, a `MockAIValidator` handles static offline evaluations. It provides semantic context but has zero operational authority.
6. **RiskEngine:** The ultimate authority. A black-box deterministic engine applying Rules R1 to R6 to block real execution, enforce maximum daily losses, and limit concurrent trades.

## 3. Key Achievements & Milestones
- **Deterministic Risk Engine:** Fully isolated risk validation that operates independently of any external AI or network calls.
- **Data Integrity & Traceability:** Implemented SHA-256 hashing for all incoming reports to prevent tampering.
- **Advanced Quantitative Metrics:** Centralized computation of Sortino Ratio, Expectancy, and Risk of Ruin.
- **Robust Testing Suite:** 117 tests covering integration and edge cases with a 100% pass rate.
- **Adapter-Based AI Architecture:** Future-proof design allowing seamless integration with OpenAI, Claude, or local Ollama instances without modifying the core pipeline.

## 4. Security & Safety Invariants
The core philosophy of Antigravity is security-first:
- **No autonomous AI execution:** The AI Validator's output is restricted by Pydantic models to explanatory recommendations.
- **Immutable real execution lock:** `approved_for_real = False` is enforced at the data model level.
- **Human-in-the-loop:** The pipeline is designed to pause at the "Approval Layer" for manual review.

## 5. Future Roadmap (Post-Delivery)
- **Phase 4.4B:** `RemoteAPIValidator` implementation.
- **Phase 4.5:** Unified UI / Telegram Approval Layer.
- **Phase 4.6:** Real-time MT5 demo sandbox integration (Gatekeeper).

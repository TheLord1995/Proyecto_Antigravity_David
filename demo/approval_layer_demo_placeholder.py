"""
demo/approval_layer_demo_placeholder.py
---------------------------------------
[PLACEHOLDER - FASE FUTURA]
Demostración conceptual de la futura Approval Layer (Fase 4.5).

Esta capa orquestará la aprobación final requerida para autorizar
el Paper Trading. Intervendrán tres factores clave:
1. Aprobación cuantitativa (ResearchValidator -> RESEARCH_APPROVED)
2. Análisis cualitativo y contextual de IA (AI Validator -> OK)
3. Aprobación final humana (Operador -> Autoriza)
"""

from enum import Enum
from pydantic import BaseModel

class FinalStatus(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    REJECTED_BY_AI = "REJECTED_BY_AI"
    REJECTED_BY_HUMAN = "REJECTED_BY_HUMAN"
    PAPER_TRADING_READY = "PAPER_TRADING_READY"

class ApprovalLayerDemo:
    
    def evaluate_strategy(self, 
                          research_status: str, 
                          ai_validator_ok: bool, 
                          human_approval: bool) -> FinalStatus:
        """
        Simula la decisión de la Approval Layer.
        """
        if research_status != "RESEARCH_APPROVED":
            return FinalStatus.PENDING_APPROVAL
            
        if not ai_validator_ok:
            return FinalStatus.REJECTED_BY_AI
            
        if not human_approval:
            return FinalStatus.REJECTED_BY_HUMAN
            
        # Si todo está en orden, se emite el codiciado estado final:
        return FinalStatus.PAPER_TRADING_READY

if __name__ == "__main__":
    print("="*80)
    print("APPROVAL LAYER DEMO (CONCEPTO FASE FUTURA)")
    print("="*80)
    
    layer = ApprovalLayerDemo()
    
    print("Caso 1: Estrategia pasó el ResearchValidator pero el humano la rechaza.")
    status_1 = layer.evaluate_strategy("RESEARCH_APPROVED", True, False)
    print(f"Estado Final: {status_1.value}\n")
    
    print("Caso 2: Estrategia pasó el ResearchValidator, IA aprueba y Humano aprueba.")
    status_2 = layer.evaluate_strategy("RESEARCH_APPROVED", True, True)
    print(f"Estado Final: {status_2.value} -> eligible_for_paper_trading = True\n")

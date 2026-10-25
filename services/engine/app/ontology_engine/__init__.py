"""
Backward compatibility re-export shim: app.ontology_engine -> app.ontology
"""
from app.ontology.core import GlobalTerminologyEvolutionEngine
from app.ontology import core

__all__ = ["GlobalTerminologyEvolutionEngine", "core"]

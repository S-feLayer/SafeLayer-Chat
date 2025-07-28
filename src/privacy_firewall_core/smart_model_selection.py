#!/usr/bin/env python3
"""
Smart Model Selection for Redaction

This module provides intelligent model selection based on content type
and characteristics for optimal redaction performance.
"""

import re
from typing import Dict, List, Any, Optional
from enum import Enum

class ModelType(Enum):
    """Available Tinfoil models."""
    DEEPSEEK = "deepseek"  # DeepSeek R1 70B
    LLAMA = "llama"        # Llama 3.3 70B
    QWEN = "qwen"          # Qwen 2.5 72B
    MISTRAL = "mistral"    # Mistral Small 3.1 24B

class SmartModelSelector:
    """
    Intelligent model selection for redaction tasks.
    """
    
    def __init__(self):
        # Model characteristics and strengths
        self.model_profiles = {
            ModelType.DEEPSEEK: {
                "name": "DeepSeek R1 70B",
                "strengths": ["reasoning", "context_understanding", "pattern_detection"],
                "best_for": ["general_redaction", "complex_documents", "mixed_content"],
                "context_length": 64000,
                "cost_factor": 1.0,  # Baseline
                "speed_factor": 1.0   # Baseline
            },
            ModelType.LLAMA: {
                "name": "Llama 3.3 70B",
                "strengths": ["multilingual", "reasoning", "chat_optimized"],
                "best_for": ["multilingual_content", "international_documents", "conversational_text"],
                "context_length": 64000,
                "cost_factor": 1.0,
                "speed_factor": 1.0
            },
            ModelType.QWEN: {
                "name": "Qwen 2.5 72B",
                "strengths": ["programming", "mathematical_reasoning", "long_context"],
                "best_for": ["code_files", "technical_documents", "financial_documents", "long_documents"],
                "context_length": 128000,
                "cost_factor": 1.1,  # Slightly higher due to larger model
                "speed_factor": 0.9   # Slightly slower
            },
            ModelType.MISTRAL: {
                "name": "Mistral Small 3.1 24B",
                "strengths": ["efficiency", "cost_effective", "fast_processing"],
                "best_for": ["simple_redaction", "budget_constrained", "high_volume"],
                "context_length": 128000,
                "cost_factor": 0.6,  # Lower cost
                "speed_factor": 1.2   # Faster processing
            }
        }
    
    def detect_content_characteristics(self, content: str) -> Dict[str, Any]:
        """
        Analyze content to determine its characteristics.
        """
        characteristics = {
            "length": len(content),
            "has_code": False,
            "has_multilingual": False,
            "has_technical_terms": False,
            "has_financial_data": False,
            "complexity_score": 0,
            "languages": []
        }
        
        # Detect code patterns
        code_patterns = [
            r'def\s+\w+\s*\(',           # Python functions
            r'function\s+\w+\s*\(',      # JavaScript functions
            r'class\s+\w+',              # Classes
            r'import\s+\w+',             # Imports
            r'const\s+\w+\s*=',          # Constants
            r'var\s+\w+\s*=',            # Variables
            r'if\s*\(',                  # Conditionals
            r'for\s*\(',                 # Loops
            r'api_key\s*=',              # API keys
            r'password\s*=',             # Passwords
            r'database_url\s*=',         # Database URLs
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                characteristics["has_code"] = True
                characteristics["complexity_score"] += 2
                break
        
        # Detect multilingual content
        non_english_chars = re.findall(r'[^\x00-\x7F]', content)
        if len(non_english_chars) > len(content) * 0.1:  # More than 10% non-ASCII
            characteristics["has_multilingual"] = True
            characteristics["complexity_score"] += 1
        
        # Detect technical terms
        technical_patterns = [
            r'\b(api|sdk|endpoint|microservice|kubernetes|docker|aws|azure|gcp)\b',
            r'\b(database|server|client|protocol|algorithm|framework)\b',
            r'\b(encryption|authentication|authorization|ssl|tls)\b'
        ]
        
        for pattern in technical_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                characteristics["has_technical_terms"] = True
                characteristics["complexity_score"] += 1
                break
        
        # Detect financial data
        financial_patterns = [
            r'\$\d+',                    # Dollar amounts
            r'\b\d+\.\d{2}\b',           # Decimal amounts
            r'\b(contract|invoice|payment|budget|revenue|profit)\b',
            r'\b(account|bank|credit|debit|transaction)\b'
        ]
        
        for pattern in financial_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                characteristics["has_financial_data"] = True
                characteristics["complexity_score"] += 1
                break
        
        # Adjust complexity based on length
        if characteristics["length"] > 10000:
            characteristics["complexity_score"] += 2
        elif characteristics["length"] > 5000:
            characteristics["complexity_score"] += 1
        
        return characteristics
    
    def select_optimal_model(self, 
                           content: str, 
                           content_type: str = "text",
                           budget_constraint: bool = False,
                           speed_priority: bool = False) -> ModelType:
        """
        Select the optimal model based on content characteristics and constraints.
        """
        characteristics = self.detect_content_characteristics(content)
        
        # Budget constraint overrides other factors
        if budget_constraint:
            return ModelType.MISTRAL
        
        # Speed priority for simple content
        if speed_priority and characteristics["complexity_score"] < 2:
            return ModelType.MISTRAL
        
        # Code-heavy content
        if characteristics["has_code"] or content_type == "code":
            return ModelType.QWEN
        
        # Multilingual content
        if characteristics["has_multilingual"]:
            return ModelType.LLAMA
        
        # Technical or financial documents
        if (characteristics["has_technical_terms"] or 
            characteristics["has_financial_data"] or
            characteristics["complexity_score"] > 3):
            return ModelType.QWEN
        
        # Long documents
        if characteristics["length"] > 8000:
            return ModelType.QWEN
        
        # Default to DeepSeek for general redaction
        return ModelType.DEEPSEEK
    
    def get_model_recommendation(self, 
                               content: str, 
                               content_type: str = "text",
                               budget_constraint: bool = False,
                               speed_priority: bool = False) -> Dict[str, Any]:
        """
        Get detailed model recommendation with reasoning.
        """
        characteristics = self.detect_content_characteristics(content)
        selected_model = self.select_optimal_model(
            content, content_type, budget_constraint, speed_priority
        )
        
        model_info = self.model_profiles[selected_model]
        
        recommendation = {
            "selected_model": selected_model.value,
            "model_name": model_info["name"],
            "reasoning": self._generate_reasoning(characteristics, selected_model, model_info),
            "characteristics": characteristics,
            "model_info": model_info,
            "alternatives": self._get_alternatives(selected_model, characteristics)
        }
        
        return recommendation
    
    def _generate_reasoning(self, 
                          characteristics: Dict[str, Any], 
                          selected_model: ModelType,
                          model_info: Dict[str, Any]) -> str:
        """Generate reasoning for model selection."""
        reasons = []
        
        if characteristics["has_code"]:
            reasons.append("Content contains code patterns")
        
        if characteristics["has_multilingual"]:
            reasons.append("Content appears to be multilingual")
        
        if characteristics["has_technical_terms"]:
            reasons.append("Content contains technical terminology")
        
        if characteristics["has_financial_data"]:
            reasons.append("Content contains financial data")
        
        if characteristics["length"] > 8000:
            reasons.append("Content is very long")
        
        if characteristics["complexity_score"] > 3:
            reasons.append("Content has high complexity")
        
        if not reasons:
            reasons.append("General purpose redaction")
        
        return f"Selected {model_info['name']} because: {'; '.join(reasons)}"
    
    def _get_alternatives(self, 
                         selected_model: ModelType, 
                         characteristics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get alternative model recommendations."""
        alternatives = []
        
        for model_type, model_info in self.model_profiles.items():
            if model_type != selected_model:
                # Calculate suitability score
                suitability_score = 0
                
                if characteristics["has_code"] and "programming" in model_info["strengths"]:
                    suitability_score += 3
                
                if characteristics["has_multilingual"] and "multilingual" in model_info["strengths"]:
                    suitability_score += 2
                
                if characteristics["complexity_score"] > 2 and "reasoning" in model_info["strengths"]:
                    suitability_score += 2
                
                if characteristics["length"] > 8000 and model_info["context_length"] > 64000:
                    suitability_score += 1
                
                if suitability_score > 0:
                    alternatives.append({
                        "model": model_type.value,
                        "name": model_info["name"],
                        "suitability_score": suitability_score,
                        "cost_factor": model_info["cost_factor"],
                        "speed_factor": model_info["speed_factor"]
                    })
        
        # Sort by suitability score
        alternatives.sort(key=lambda x: x["suitability_score"], reverse=True)
        return alternatives[:2]  # Return top 2 alternatives

# Integration with existing TinfoilLLM
class EnhancedTinfoilLLM:
    """
    Enhanced TinfoilLLM with smart model selection.
    """
    
    def __init__(self, api_key: str = None):
        from .tinfoil_llm import TinfoilLLM
        self.tinfoil_llm = TinfoilLLM()
        self.model_selector = SmartModelSelector()
    
    def get_smart_response(self, 
                          prompt: str, 
                          content: str = "",
                          content_type: str = "text",
                          budget_constraint: bool = False,
                          speed_priority: bool = False) -> Dict[str, Any]:
        """
        Get response using smart model selection.
        """
        # Get model recommendation
        recommendation = self.model_selector.get_model_recommendation(
            content, content_type, budget_constraint, speed_priority
        )
        
        # Get response from selected model
        response = self.tinfoil_llm.get_tinfoil_response(
            prompt, model=recommendation["selected_model"]
        )
        
        return {
            "response": response,
            "model_used": recommendation["selected_model"],
            "model_name": recommendation["model_name"],
            "reasoning": recommendation["reasoning"],
            "characteristics": recommendation["characteristics"]
        }
    
    def analyze_content_for_model_selection(self, content: str, content_type: str = "text") -> Dict[str, Any]:
        """
        Analyze content and provide model recommendations.
        """
        return self.model_selector.get_model_recommendation(content, content_type)

# Usage examples
def demonstrate_smart_model_selection():
    """Demonstrate smart model selection."""
    
    selector = SmartModelSelector()
    
    # Test different content types
    test_cases = [
        {
            "name": "Code File",
            "content": """
            import os
            from flask import Flask
            
            app = Flask(__name__)
            
            DATABASE_URL = "postgresql://user:password@localhost:5432/db"
            API_KEY = "sk-1234567890abcdef"
            
            @app.route('/')
            def hello():
                return "Hello World!"
            """,
            "type": "code"
        },
        {
            "name": "Multilingual Document",
            "content": """
            Bonjour! This is a mixed language document.
            Hola! We have content in multiple languages.
            Hello! This contains English, French, and Spanish.
            """,
            "type": "text"
        },
        {
            "name": "Financial Document",
            "content": """
            Quarterly Report Q1 2024
            
            Revenue: $1,250,000
            Expenses: $850,000
            Profit: $400,000
            
            Contract Number: CNT-2024-001
            Budget Allocation: $500,000
            """,
            "type": "text"
        },
        {
            "name": "Simple Text",
            "content": "Hi John, my email is john@example.com and phone is 555-123-4567",
            "type": "text"
        }
    ]
    
    print("🧠 SMART MODEL SELECTION DEMONSTRATION")
    print("=" * 60)
    
    for test_case in test_cases:
        print(f"\n📋 {test_case['name']}")
        print("-" * 40)
        
        recommendation = selector.get_model_recommendation(
            test_case["content"], 
            test_case["type"]
        )
        
        print(f"Selected Model: {recommendation['model_name']}")
        print(f"Reasoning: {recommendation['reasoning']}")
        print(f"Content Length: {recommendation['characteristics']['length']} chars")
        print(f"Complexity Score: {recommendation['characteristics']['complexity_score']}")
        
        if recommendation['alternatives']:
            print("Alternatives:")
            for alt in recommendation['alternatives']:
                print(f"  • {alt['name']} (Score: {alt['suitability_score']})")

if __name__ == "__main__":
    demonstrate_smart_model_selection() 
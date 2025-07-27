#!/usr/bin/env python3
"""
Example Data Analysis Agent
Protected with AI Agent PII Shield
"""

from ai_agent_pii_shield import create_agent_shield, AgentType, ProtectionLevel
from typing import Dict, Any

# Create shield for data analysis
data_shield = create_agent_shield(
    agent_type=AgentType.DATA_ANALYSIS,
    protection_level=ProtectionLevel.ENTERPRISE
)

@data_shield.protect_agent
def analyze_business_data(analysis_request: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze business data with automatic PII protection."""
    database_url = analysis_request.get('database_url', '')
    customer_data = analysis_request.get('customer_data', {})
    
    analysis_result = {
        "database_connection": f"Connected to {database_url}",
        "customer_analysis": f"Analyzed data for {customer_data.get('name', 'Customer')}",
        "metrics": {
            "total_customers": 1500,
            "revenue": "$50,000",
            "growth_rate": "15%"
        }
    }
    return analysis_result

# Example usage
if __name__ == "__main__":
    test_data = {
        "database_url": "postgresql://user:password123@localhost:5432/business_db",
        "customer_data": {
            "name": "Acme Corporation",
            "email": "contact@acme.com"
        }
    }
    
    result = analyze_business_data(test_data)
    print("Protected analysis result:", result)

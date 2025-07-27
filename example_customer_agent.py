#!/usr/bin/env python3
"""
Example Customer Service Agent
Protected with AI Agent PII Shield
"""

from ai_agent_pii_shield import create_agent_shield, AgentType, ProtectionLevel
from typing import Dict, Any

# Create shield for customer service
customer_shield = create_agent_shield(
    agent_type=AgentType.CUSTOMER_SERVICE,
    protection_level=ProtectionLevel.COMPREHENSIVE
)

@customer_shield.protect_agent
def handle_customer_inquiry(customer_data: Dict[str, Any]) -> str:
    """Handle customer service inquiries with automatic PII protection."""
    name = customer_data.get('name', 'Customer')
    email = customer_data.get('email', '')
    order_id = customer_data.get('order_id', '')
    
    response = f"""
    Hello {name}, thank you for contacting us!
    
    I can see your order {order_id} and will help you with your inquiry.
    I'll send updates to {email}.
    
    How can I assist you today?
    """
    return response

# Example usage
if __name__ == "__main__":
    test_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "555-123-4567",
        "order_id": "ORD-12345"
    }
    
    result = handle_customer_inquiry(test_data)
    print("Protected response:", result)

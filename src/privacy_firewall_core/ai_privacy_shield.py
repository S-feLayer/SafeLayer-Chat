#!/usr/bin/env python3
"""
AI Privacy Shield - Enterprise PII Protection for AI

This module implements the core AI Privacy Shield functionality:
- Real-time PII detection and redaction
- Continuous entity persistence
- Context preservation
- Enterprise security features
"""

import os
import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from dataclasses import dataclass, asdict
from functools import lru_cache

from .tinfoil_llm import TinfoilLLM
from .enhanced_detection import EnhancedDetection
from .advanced_masking import AdvancedMasking, MaskingStrategy
from .smart_model_selection import SmartModelSelector

logger = logging.getLogger(__name__)

class EntityType(Enum):
    """Types of entities that can be persisted."""
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    API_KEY = "api_key"
    CUSTOM = "custom"

@dataclass
class EntityMapping:
    """Represents a persistent entity mapping."""
    entity_id: str
    original_value: str
    masked_value: str
    entity_type: EntityType
    context_hash: str
    created_at: datetime
    last_seen: datetime
    usage_count: int
    confidence_score: float
    metadata: Dict[str, Any]

@dataclass
class RedactionResult:
    """Result of a redaction operation."""
    original_content: str
    redacted_content: str
    detected_entities: List[Dict[str, Any]]
    entity_mappings: List[EntityMapping]
    redaction_summary: Dict[str, Any]
    processing_time_ms: float
    model_used: str
    confidence_score: float

class EntityPersistenceManager:
    """
    Manages continuous entity persistence across sessions and conversations.
    """
    
    def __init__(self, redis_url: str = None, postgres_url: str = None):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self.postgres_url = postgres_url or os.getenv("POSTGRES_URL")
        
        # Initialize connections
        self.redis_client = redis.from_url(self.redis_url)
        self.postgres_conn = None
        if self.postgres_url:
            self.postgres_conn = psycopg2.connect(self.postgres_url)
            self._init_database()
    
    def _init_database(self):
        """Initialize database tables."""
        with self.postgres_conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entity_mappings (
                    id SERIAL PRIMARY KEY,
                    entity_id VARCHAR(255) UNIQUE NOT NULL,
                    original_value TEXT NOT NULL,
                    masked_value VARCHAR(255) NOT NULL,
                    entity_type VARCHAR(50) NOT NULL,
                    context_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 1,
                    confidence_score FLOAT DEFAULT 1.0,
                    metadata JSONB DEFAULT '{}',
                    INDEX idx_context_hash (context_hash),
                    INDEX idx_entity_type (entity_type),
                    INDEX idx_last_seen (last_seen)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS redaction_sessions (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) UNIQUE NOT NULL,
                    user_id VARCHAR(255),
                    organization_id VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_entities INTEGER DEFAULT 0,
                    metadata JSONB DEFAULT '{}'
                )
            """)
            
            self.postgres_conn.commit()
    
    def get_entity_mapping(self, 
                          original_value: str, 
                          context_hash: str,
                          entity_type: EntityType) -> Optional[EntityMapping]:
        """
        Get existing entity mapping or create new one.
        """
        # Try Redis first for speed
        cache_key = f"entity:{context_hash}:{hashlib.md5(original_value.encode()).hexdigest()}"
        cached = self.redis_client.get(cache_key)
        
        if cached:
            data = json.loads(cached)
            return EntityMapping(**data)
        
        # Check database
        if self.postgres_conn:
            with self.postgres_conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM entity_mappings 
                    WHERE context_hash = %s AND entity_type = %s
                    ORDER BY usage_count DESC, confidence_score DESC
                    LIMIT 1
                """, (context_hash, entity_type.value))
                
                row = cursor.fetchone()
                if row:
                    mapping = EntityMapping(
                        entity_id=row['entity_id'],
                        original_value=row['original_value'],
                        masked_value=row['masked_value'],
                        entity_type=EntityType(row['entity_type']),
                        context_hash=row['context_hash'],
                        created_at=row['created_at'],
                        last_seen=row['last_seen'],
                        usage_count=row['usage_count'],
                        confidence_score=row['confidence_score'],
                        metadata=row['metadata']
                    )
                    
                    # Cache in Redis
                    self.redis_client.setex(
                        cache_key, 
                        3600,  # 1 hour TTL
                        json.dumps(asdict(mapping))
                    )
                    
                    return mapping
        
        return None
    
    def create_entity_mapping(self, 
                            original_value: str,
                            entity_type: EntityType,
                            context_hash: str,
                            confidence_score: float = 1.0,
                            metadata: Dict[str, Any] = None) -> EntityMapping:
        """
        Create a new entity mapping.
        """
        # Generate masked value based on entity type
        masked_value = self._generate_masked_value(original_value, entity_type)
        
        # Create entity ID
        entity_id = str(uuid.uuid4())
        
        mapping = EntityMapping(
            entity_id=entity_id,
            original_value=original_value,
            masked_value=masked_value,
            entity_type=entity_type,
            context_hash=context_hash,
            created_at=datetime.now(),
            last_seen=datetime.now(),
            usage_count=1,
            confidence_score=confidence_score,
            metadata=metadata or {}
        )
        
        # Store in database
        if self.postgres_conn:
            with self.postgres_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO entity_mappings 
                    (entity_id, original_value, masked_value, entity_type, context_hash, 
                     created_at, last_seen, usage_count, confidence_score, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    mapping.entity_id, mapping.original_value, mapping.masked_value,
                    mapping.entity_type.value, mapping.context_hash, mapping.created_at,
                    mapping.last_seen, mapping.usage_count, mapping.confidence_score,
                    json.dumps(mapping.metadata)
                ))
                self.postgres_conn.commit()
        
        # Cache in Redis
        cache_key = f"entity:{context_hash}:{hashlib.md5(original_value.encode()).hexdigest()}"
        self.redis_client.setex(
            cache_key, 
            3600,  # 1 hour TTL
            json.dumps(asdict(mapping))
        )
        
        return mapping
    
    def update_entity_usage(self, entity_id: str):
        """Update entity usage statistics."""
        if self.postgres_conn:
            with self.postgres_conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE entity_mappings 
                    SET usage_count = usage_count + 1, last_seen = CURRENT_TIMESTAMP
                    WHERE entity_id = %s
                """, (entity_id,))
                self.postgres_conn.commit()
    
    def _generate_masked_value(self, original_value: str, entity_type: EntityType) -> str:
        """Generate a masked value for an entity."""
        if entity_type == EntityType.PERSON:
            # Generate consistent person names
            hash_val = hashlib.md5(original_value.encode()).hexdigest()
            person_num = int(hash_val[:8], 16) % 10000
            return f"Person {person_num}"
        
        elif entity_type == EntityType.ORGANIZATION:
            hash_val = hashlib.md5(original_value.encode()).hexdigest()
            org_num = int(hash_val[:8], 16) % 10000
            return f"Organization {org_num}"
        
        elif entity_type == EntityType.EMAIL:
            return "[EMAIL]"
        
        elif entity_type == EntityType.PHONE:
            return "[PHONE]"
        
        elif entity_type == EntityType.SSN:
            return "[SSN]"
        
        elif entity_type == EntityType.CREDIT_CARD:
            return "[CREDIT_CARD]"
        
        elif entity_type == EntityType.API_KEY:
            return "[API_KEY]"
        
        else:
            # Generic masking
            return f"[{entity_type.value.upper()}]"

class AIPrivacyShield:
    """
    Main AI Privacy Shield class that orchestrates PII detection and redaction.
    """
    
    def __init__(self, 
                 tinfoil_api_key: str = None,
                 redis_url: str = None,
                 postgres_url: str = None,
                 enable_persistence: bool = True):
        
        # Initialize components
        self.tinfoil_llm = TinfoilLLM()
        if tinfoil_api_key:
            self.tinfoil_llm.api_key = tinfoil_api_key
        
        self.detector = EnhancedDetection(self.tinfoil_llm)
        self.masker = AdvancedMasking(MaskingStrategy.PARTIAL)
        self.model_selector = SmartModelSelector()
        
        # Entity persistence
        self.persistence_enabled = enable_persistence
        if enable_persistence:
            self.persistence_manager = EntityPersistenceManager(redis_url, postgres_url)
        
        # Configuration
        self.config = {
            "enable_context_preservation": True,
            "enable_entity_persistence": enable_persistence,
            "enable_audit_logging": True,
            "max_context_length": 64000,
            "confidence_threshold": 0.8
        }
        
        logger.info("AI Privacy Shield initialized successfully")
    
    def redact_content(self, 
                      content: str,
                      content_type: str = "text",
                      session_id: str = None,
                      user_id: str = None,
                      organization_id: str = None,
                      custom_rules: Dict[str, Any] = None) -> RedactionResult:
        """
        Main redaction method with continuous entity persistence.
        """
        start_time = datetime.now()
        
        # Generate context hash for entity persistence
        context_hash = self._generate_context_hash(session_id, user_id, organization_id)
        
        # Select optimal model
        model_recommendation = self.model_selector.get_model_recommendation(
            content, content_type
        )
        
        # Detect sensitive data
        detected_entities = self._detect_sensitive_data(
            content, content_type, model_recommendation["selected_model"]
        )
        
        # Apply entity persistence
        entity_mappings = []
        if self.persistence_enabled:
            entity_mappings = self._apply_entity_persistence(
                detected_entities, context_hash
            )
        
        # Redact content
        redacted_content = self._redact_with_persistence(
            content, detected_entities, entity_mappings
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Generate summary
        redaction_summary = self._generate_redaction_summary(
            detected_entities, entity_mappings, processing_time
        )
        
        return RedactionResult(
            original_content=content,
            redacted_content=redacted_content,
            detected_entities=detected_entities,
            entity_mappings=entity_mappings,
            redaction_summary=redaction_summary,
            processing_time_ms=processing_time,
            model_used=model_recommendation["model_name"],
            confidence_score=model_recommendation["model_info"]["confidence_score"]
        )
    
    def _detect_sensitive_data(self, 
                              content: str, 
                              content_type: str,
                              model: str) -> List[Dict[str, Any]]:
        """Detect sensitive data using enhanced detection."""
        # Use pattern-based detection
        pattern_results = self.detector.detect_with_patterns(content)
        
        # Use AI-based detection
        ai_results = self.detector.detect_with_ai(content, content_type)
        
        # Combine and validate results
        combined_results = self.detector.detect_sensitive_data(content, content_type)
        
        # Convert to standardized format
        entities = []
        for entity_type, values in combined_results.items():
            for value in values:
                entities.append({
                    "type": entity_type,
                    "value": value,
                    "confidence": 0.9,  # High confidence for validated results
                    "source": "combined"
                })
        
        return entities
    
    def _apply_entity_persistence(self, 
                                 detected_entities: List[Dict[str, Any]],
                                 context_hash: str) -> List[EntityMapping]:
        """Apply continuous entity persistence."""
        mappings = []
        
        for entity in detected_entities:
            entity_type = self._map_entity_type(entity["type"])
            
            # Check for existing mapping
            existing_mapping = self.persistence_manager.get_entity_mapping(
                entity["value"], context_hash, entity_type
            )
            
            if existing_mapping:
                # Use existing mapping
                mappings.append(existing_mapping)
                self.persistence_manager.update_entity_usage(existing_mapping.entity_id)
            else:
                # Create new mapping
                new_mapping = self.persistence_manager.create_entity_mapping(
                    entity["value"],
                    entity_type,
                    context_hash,
                    entity["confidence"],
                    {"source": entity["source"]}
                )
                mappings.append(new_mapping)
        
        return mappings
    
    def _redact_with_persistence(self, 
                                content: str,
                                detected_entities: List[Dict[str, Any]],
                                entity_mappings: List[EntityMapping]) -> str:
        """Redact content while preserving entity consistency."""
        redacted_content = content
        
        # Create mapping from original values to masked values
        value_mapping = {}
        for mapping in entity_mappings:
            value_mapping[mapping.original_value] = mapping.masked_value
        
        # Apply redactions
        for entity in detected_entities:
            original_value = entity["value"]
            if original_value in value_mapping:
                masked_value = value_mapping[original_value]
                redacted_content = redacted_content.replace(original_value, masked_value)
        
        return redacted_content
    
    def _generate_context_hash(self, 
                              session_id: str = None,
                              user_id: str = None,
                              organization_id: str = None) -> str:
        """Generate a context hash for entity persistence."""
        context_parts = []
        
        if session_id:
            context_parts.append(f"session:{session_id}")
        if user_id:
            context_parts.append(f"user:{user_id}")
        if organization_id:
            context_parts.append(f"org:{organization_id}")
        
        if not context_parts:
            context_parts.append("default")
        
        context_string = "|".join(context_parts)
        return hashlib.md5(context_string.encode()).hexdigest()
    
    def _map_entity_type(self, detected_type: str) -> EntityType:
        """Map detected entity type to EntityType enum."""
        type_mapping = {
            "name": EntityType.PERSON,
            "email": EntityType.EMAIL,
            "phone": EntityType.PHONE,
            "ssn": EntityType.SSN,
            "credit_card": EntityType.CREDIT_CARD,
            "api_key": EntityType.API_KEY,
            "organization": EntityType.ORGANIZATION,
            "location": EntityType.LOCATION
        }
        
        return type_mapping.get(detected_type, EntityType.CUSTOM)
    
    def _generate_redaction_summary(self,
                                  detected_entities: List[Dict[str, Any]],
                                  entity_mappings: List[EntityMapping],
                                  processing_time: float) -> Dict[str, Any]:
        """Generate a summary of the redaction operation."""
        entity_types = {}
        for entity in detected_entities:
            entity_type = entity["type"]
            if entity_type not in entity_types:
                entity_types[entity_type] = 0
            entity_types[entity_type] += 1
        
        return {
            "total_entities_detected": len(detected_entities),
            "total_entities_redacted": len(entity_mappings),
            "entity_types": entity_types,
            "processing_time_ms": processing_time,
            "persistence_enabled": self.persistence_enabled,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_entity_statistics(self, 
                            context_hash: str = None,
                            user_id: str = None,
                            organization_id: str = None) -> Dict[str, Any]:
        """Get statistics about entity usage."""
        if not self.persistence_enabled:
            return {"error": "Entity persistence not enabled"}
        
        # This would query the database for statistics
        # Implementation depends on specific requirements
        return {
            "total_entities": len(self.persistence_manager.get_all_entities(context_hash)),
            "most_used_entities": [],
            "entity_types": {},
            "usage_trends": {}
        }
    
    def export_entity_mappings(self, 
                             context_hash: str = None,
                             format: str = "json") -> str:
        """Export entity mappings for audit purposes."""
        if not self.persistence_enabled:
            return json.dumps({"error": "Entity persistence not enabled"})
        
        # This would export mappings from the database
        # Implementation depends on specific requirements
        return json.dumps({
            "mappings": [],
            "export_timestamp": datetime.now().isoformat(),
            "format": format
        })

# Enterprise API wrapper
class EnterprisePrivacyAPI:
    """
    Enterprise API wrapper for AI Privacy Shield.
    """
    
    def __init__(self, 
                 tinfoil_api_key: str,
                 redis_url: str = None,
                 postgres_url: str = None):
        self.shield = AIPrivacyShield(
            tinfoil_api_key=tinfoil_api_key,
            redis_url=redis_url,
            postgres_url=postgres_url,
            enable_persistence=True
        )
    
    def redact_message(self, 
                      message: str,
                      session_id: str = None,
                      user_id: str = None,
                      organization_id: str = None) -> Dict[str, Any]:
        """Redact a single message."""
        result = self.shield.redact_content(
            message, "text", session_id, user_id, organization_id
        )
        
        return {
            "redacted_message": result.redacted_content,
            "entities_detected": len(result.detected_entities),
            "processing_time_ms": result.processing_time_ms,
            "model_used": result.model_used
        }
    
    def redact_conversation(self, 
                           messages: List[Dict[str, str]],
                           session_id: str = None,
                           user_id: str = None,
                           organization_id: str = None) -> List[Dict[str, Any]]:
        """Redact an entire conversation."""
        results = []
        
        for message in messages:
            result = self.shield.redact_content(
                message["content"],
                "text",
                session_id,
                user_id,
                organization_id
            )
            
            results.append({
                "original_message": message["content"],
                "redacted_message": result.redacted_content,
                "entities_detected": len(result.detected_entities),
                "timestamp": message.get("timestamp", datetime.now().isoformat())
            })
        
        return results

# Usage example
def demonstrate_ai_privacy_shield():
    """Demonstrate AI Privacy Shield functionality."""
    
    # Initialize the shield
    shield = AIPrivacyShield(enable_persistence=True)
    
    # Test conversation with entity persistence
    conversation = [
        "Hi, my name is John Smith and my email is john.smith@company.com",
        "I work at Acme Corporation and my phone number is 555-123-4567",
        "Can you help me with the project for John Smith?",
        "I need to contact john.smith@company.com about the budget"
    ]
    
    session_id = "demo_session_123"
    user_id = "user_456"
    
    print("🛡️ AI PRIVACY SHIELD DEMONSTRATION")
    print("=" * 50)
    
    for i, message in enumerate(conversation, 1):
        print(f"\n📝 Message {i}: {message}")
        
        result = shield.redact_content(
            message, "text", session_id, user_id
        )
        
        print(f"🔒 Redacted: {result.redacted_content}")
        print(f"📊 Entities: {len(result.detected_entities)} detected")
        print(f"⚡ Time: {result.processing_time_ms:.2f}ms")
        
        if result.entity_mappings:
            print("🔄 Entity Mappings:")
            for mapping in result.entity_mappings:
                print(f"  • {mapping.original_value} → {mapping.masked_value}")

if __name__ == "__main__":
    demonstrate_ai_privacy_shield() 
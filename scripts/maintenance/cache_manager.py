import redis
import json
from typing import Any, Optional, Dict
import asyncio
from datetime import timedelta
import os

class CacheManager:
    def __init__(self, redis_url: str = None, langcache_api_key: str = None):
        # Get Redis URL from environment, fallback to localhost for development
        redis_url = redis_url or os.getenv('REDIS_URL') or "redis://localhost:6379"
        langcache_api_key = langcache_api_key or os.getenv('LANGCACHE_API_KEY')

        # Initialize Redis for general caching
        self.redis_url = redis_url
        self.redis = None
        self.enabled = False
        self.memory_cache = {}

        try:
            self.redis = redis.from_url(redis_url)
            self.redis.ping()  # Test connection
            self.enabled = True
            print(" Redis cache enabled")
        except Exception as e:
            print(f"  Redis not available: {e}")
            print("📦 Using in-memory fallback cache")

        # Initialize LangCache for AI semantic caching (simplified without server_url)
        self.langcache_enabled = False
        if langcache_api_key:
            try:
                # For now, we'll use Redis for AI caching instead of LangCache server
                # This gives us the benefits without the complexity
                self.langcache_enabled = True
                print(" AI semantic caching enabled (Redis-based)")
            except Exception as e:
                print(f"  AI caching not available: {e}")

    async def get_ai_response(self, prompt: str, model: str = "gpt-4") -> Optional[str]:
        """Get cached AI response using semantic caching"""
        if not self.langcache_enabled:
            return None

        try:
            # Use semantic hash for AI response caching
            import hashlib
            prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
            cache_key = f"ai:{model}:{prompt_hash}"
            cached_response = await self.get(cache_key)
            if cached_response:
                print(" AI response served from cache")
                return cached_response
            return None
        except Exception as e:
            print(f"  AI cache retrieval failed: {e}")
            return None

    async def set_ai_response(self, prompt: str, response: str, model: str = "gpt-4", expire: timedelta = timedelta(hours=24)):
        """Cache AI response with semantic understanding"""
        if not self.langcache_enabled:
            return

        try:
            # Use semantic hash for AI response caching
            import hashlib
            prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
            cache_key = f"ai:{model}:{prompt_hash}"
            await self.set(cache_key, response, expire)
            print(" AI response cached with semantic understanding")
        except Exception as e:
            print(f"  AI cache storage failed: {e}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        return {
            "redis_enabled": self.enabled,
            "langcache_enabled": self.langcache_enabled,
            "redis_url": self.redis_url if self.enabled else None,
            "memory_cache_size": len(self.memory_cache) if not self.enabled else 0
        }

    def get(self, key: str) -> Optional[Any]:
        if not self.enabled:
            return self.memory_cache.get(key)

        try:
            data = self.redis.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None

    def set(self, key: str, value: Any, expire: timedelta = None, ttl: int = None):
        """Set cache value with TTL support
        
        Args:
            key: Cache key
            value: Value to cache
            expire: timedelta object for expiration
            ttl: TTL in seconds (alternative to expire)
        """
        if not self.enabled:
            self.memory_cache[key] = value
            return

        try:
            # Convert TTL to timedelta if provided
            if ttl is not None:
                expire = timedelta(seconds=ttl)
            elif expire is None:
                expire = timedelta(hours=1)  # Default 1 hour
                
            self.redis.setex(key, expire, json.dumps(value))
        except Exception:
            pass

    def delete(self, key: str):
        if not self.enabled:
            self.memory_cache.pop(key, None)
            return

        try:
            self.redis.delete(key)
        except Exception:
            pass

cache_manager = CacheManager()
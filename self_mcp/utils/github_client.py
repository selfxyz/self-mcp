"""GitHub API client for fetching Self protocol documentation"""

import base64
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
from pydantic import BaseModel


class CachedDocument(BaseModel):
    """Cached document with metadata"""
    content: str
    fetched_at: datetime
    path: str


class GitHubDocsClient:
    """Client for fetching documentation from GitHub with caching"""
    
    def __init__(self, repo: str = "selfxyz/self-docs", cache_ttl_minutes: int = 60):
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}/contents"
        self.cache: Dict[str, CachedDocument] = {}
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        self._client = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "Self-MCP-Server"
                },
                timeout=30.0
            )
        return self._client
    
    def _is_cache_valid(self, cached: CachedDocument) -> bool:
        """Check if cached document is still valid"""
        return datetime.now() - cached.fetched_at < self.cache_ttl
    
    async def fetch_document(self, path: str) -> Optional[str]:
        """Fetch a document from GitHub, with caching"""
        # Check cache first
        if path in self.cache:
            cached = self.cache[path]
            if self._is_cache_valid(cached):
                return cached.content
        
        try:
            client = await self._get_client()
            url = f"{self.base_url}/{path}"
            
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Decode base64 content
            if data.get("encoding") == "base64":
                content = base64.b64decode(data["content"]).decode("utf-8")
                
                # Cache the document
                self.cache[path] = CachedDocument(
                    content=content,
                    fetched_at=datetime.now(),
                    path=path
                )
                
                return content
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            # Log error but don't crash
            print(f"Error fetching {path}: {e}")
            
            # Return cached version if available, even if expired
            if path in self.cache:
                return self.cache[path].content
            
            return None
    
    async def list_directory(self, path: str = "") -> Optional[Dict[str, Any]]:
        """List contents of a directory"""
        try:
            client = await self._get_client()
            url = f"{self.base_url}/{path}" if path else self.base_url
            
            response = await client.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error listing directory {path}: {e}")
            return None
    
    def clear_cache(self):
        """Clear all cached documents"""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        valid_count = sum(1 for doc in self.cache.values() if self._is_cache_valid(doc))
        return {
            "total_cached": len(self.cache),
            "valid_cached": valid_count,
            "expired_cached": len(self.cache) - valid_count,
            "cache_ttl_minutes": self.cache_ttl.total_seconds() / 60
        }
    
    async def close(self):
        """Close the HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None


# Global client instance
_docs_client: Optional[GitHubDocsClient] = None


def get_docs_client() -> GitHubDocsClient:
    """Get or create the global docs client"""
    global _docs_client
    if _docs_client is None:
        _docs_client = GitHubDocsClient()
    return _docs_client
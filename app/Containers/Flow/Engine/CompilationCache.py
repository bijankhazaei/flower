import hashlib
import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CacheEntry:
    code: str
    timestamp: datetime
    flow_hash: str

class CompilationCache:
    def __init__(self, cache_dir: str = "cache/compilation"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_flow_hash(self, flow_definition: Dict[str, Any]) -> str:
        """Generate hash for flow definition"""
        flow_str = json.dumps(flow_definition, sort_keys=True)
        return hashlib.md5(flow_str.encode()).hexdigest()
    
    def _get_cache_path(self, flow_hash: str) -> str:
        """Get cache file path for flow hash"""
        return os.path.join(self.cache_dir, f"{flow_hash}.json")
    
    def get(self, flow_definition: Dict[str, Any]) -> Optional[str]:
        """Get cached compilation result"""
        flow_hash = self._get_flow_hash(flow_definition)
        cache_path = self._get_cache_path(flow_hash)
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    cache_data = json.load(f)
                return cache_data.get('code')
            except:
                pass
        return None
    
    def set(self, flow_definition: Dict[str, Any], code: str) -> None:
        """Cache compilation result"""
        flow_hash = self._get_flow_hash(flow_definition)
        cache_path = self._get_cache_path(flow_hash)
        
        cache_data = {
            'code': code,
            'timestamp': datetime.now().isoformat(),
            'flow_hash': flow_hash
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f)
    
    def clear(self) -> None:
        """Clear all cached entries"""
        for file in os.listdir(self.cache_dir):
            if file.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, file))
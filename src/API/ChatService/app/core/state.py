import asyncio
from typing import Dict, List

# Keyed by "user_id:chat_thread_id" → list of asyncio.Queue
connections: Dict[str, List[asyncio.Queue]] = {}
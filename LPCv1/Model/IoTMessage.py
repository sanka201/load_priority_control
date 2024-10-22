from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict

@dataclass
class IoTMessage:

    device_id: int
    message_type: str
    payload: Dict[str, any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    priority: Optional[int] = 0
    
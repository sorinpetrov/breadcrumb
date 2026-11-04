"""Pure-Python trail bookkeeping. No ROS imports so it stays unit-testable."""

from collections import deque
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Crumb:
    x: float
    y: float
    yaw: float
    stamp: float


class Trail:
    def __init__(self, drop_distance=0.5, drop_angle=0.35, max_crumbs=2048):
        self.drop_distance = drop_distance
        self.drop_angle = drop_angle
        self._crumbs = deque(maxlen=max_crumbs)

    def __len__(self):
        return len(self._crumbs)

    @property
    def first(self):
        # The one that matters. Everything else is just how you got here.
        return self._crumbs[0] if self._crumbs else None

    @property
    def last(self):
        return self._crumbs[-1] if self._crumbs else None

    def offer(self, crumb):
        """Store the crumb if it is far enough from the last one. Returns True if stored."""
        last = self.last
        if last is None:
            self._crumbs.append(crumb)
            return True
        dist = math.hypot(crumb.x - last.x, crumb.y - last.y)
        dyaw = abs(math.atan2(math.sin(crumb.yaw - last.yaw), math.cos(crumb.yaw - last.yaw)))
        if dist >= self.drop_distance or dyaw >= self.drop_angle:
            self._crumbs.append(crumb)
            return True
        return False

    def path_home(self):
        """Crumbs from newest to oldest. Follow them and you end up at the start."""
        return list(reversed(self._crumbs))

    def clear(self):
        self._crumbs.clear()

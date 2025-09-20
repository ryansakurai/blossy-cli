"""Domain models for the 'calculate' command."""

from dataclasses import dataclass


class Time:
    """Custom time class supporting arithmetic operations."""

    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0) -> None:
        absolute = abs(seconds) + abs(minutes) * 60 + abs(hours) * 60 * 60
        if hours < 0 or minutes < 0 or seconds < 0:
            self._total_secs = 0 - absolute
        else:
            self._total_secs = absolute

    @property
    def hours(self) -> int:
        """Hours component in HH:MM:SS display format."""
        absolute = abs(self._total_secs) // (60 * 60)
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def minutes(self) -> int:
        """Minutes component in HH:MM:SS display format."""
        absolute = (abs(self._total_secs) % (60 * 60)) // 60
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def seconds(self) -> int:
        """Seconds component in HH:MM:SS display format."""
        absolute = abs(self._total_secs) % 60
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def total_hours(self) -> int:
        """Total duration converted to whole hours."""
        absolute = abs(self._total_secs) // (60 * 60)
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def total_minutes(self) -> int:
        """Total duration converted to whole minutes."""
        absolute = abs(self._total_secs) // 60
        return absolute if self._total_secs >= 0 else 0 - absolute

    @property
    def total_seconds(self) -> int:
        """Total duration in seconds."""
        return self._total_secs

    def __add__(self, other):
        if isinstance(other, Time):
            return Time(seconds=self.total_seconds + other.total_seconds)
        raise TypeError(
            f"unsupported operand type(s) for +: 'Time' and '{type(other).__name__}'"
        )

    def __sub__(self, other):
        if isinstance(other, Time):
            return Time(seconds=self.total_seconds - other.total_seconds)
        raise TypeError(
            f"unsupported operand type(s) for -: 'Time' and '{type(other).__name__}'"
        )

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Time(seconds=int(self.total_seconds * other))
        raise TypeError(
            f"unsupported operand type(s) for *: 'Time' and '{type(other).__name__}'"
        )

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Time(seconds=int(self.total_seconds * other))
        raise TypeError(
            f"unsupported operand type(s) for *: '{type(other).__name__}' and 'Time'"
        )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Time(seconds=int(self.total_seconds / other))
        raise TypeError(
            f"unsupported operand type(s) for /: 'Time' and '{type(other).__name__}'"
        )

    def __str__(self):
        if self.total_seconds < 0:
            return f"-{abs(self.hours)}:{abs(self.minutes):02}:{abs(self.seconds):02}"
        return f"{abs(self.hours)}:{abs(self.minutes):02}:{abs(self.seconds):02}"


@dataclass
class ExpressionResult:
    """Represents the result of parsing an expression for visualization."""

    value: tuple[str] | str
    type: str


@dataclass
class VisualCalcStep:
    """Represents a single step in the calculation process."""

    operation: str | None
    stack: str | None
    input: str | None

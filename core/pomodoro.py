"""
Pomodoro Timer module: handles 25-min work sessions and breaks.
"""
import time
import threading
from typing import Callable, Optional


class PomodoroTimer:
    """Thread-safe Pomodoro timer with completion callback."""

    def __init__(self, work_minutes: int = 25, break_minutes: int = 5):
        """
        Initialize timer.
        
        Args:
            work_minutes: duration of work session (default 25)
            break_minutes: duration of break (default 5)
        """
        self.work_seconds = work_minutes * 60
        self.break_seconds = break_minutes * 60
        self.seconds_left = self.work_seconds
        self.running = False
        self.paused = False
        self.on_tick: Optional[Callable[[str], None]] = None
        self.on_complete: Optional[Callable[[str], None]] = None

    def start(self) -> None:
        """Start the timer in a background thread."""
        if self.running:
            return
        self.running = True
        self.paused = False
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self) -> None:
        """Stop the timer and reset."""
        self.running = False
        self.paused = False
        self.seconds_left = self.work_seconds
        if self.on_tick:
            self.on_tick(self._format_time(self.seconds_left))

    def pause(self) -> None:
        """Pause the timer (can resume)."""
        self.paused = True

    def resume(self) -> None:
        """Resume a paused timer."""
        self.paused = False

    def _format_time(self, seconds: int) -> str:
        """Format seconds as MM:SS."""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def _run(self) -> None:
        """Main timer loop (runs in background thread)."""
        is_work_session = True
        while self.running and self.seconds_left > 0:
            if not self.paused:
                self.seconds_left -= 1
                if self.on_tick:
                    self.on_tick(self._format_time(self.seconds_left))
            time.sleep(1)

        if self.running and self.seconds_left == 0:
            # Session completed
            session_type = "Work" if is_work_session else "Break"
            if self.on_complete:
                self.on_complete(session_type)

            # Auto-transition to break or next session
            if is_work_session:
                self.seconds_left = self.break_seconds
                is_work_session = False
                time.sleep(2)
                if self.running:
                    self._run()
            else:
                self.running = False

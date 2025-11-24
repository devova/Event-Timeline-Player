import reflex as rx
from typing import TypedDict
import asyncio
import random
import string
import logging


class TimelineEvent(TypedDict):
    id: str
    time: float
    label: str
    type: str
    description: str
    status: str


class EventLog(TypedDict):
    timestamp: str
    event_label: str
    action: str


class TimelineItem(TypedDict):
    id: str
    name: str
    type: str
    duration: float
    current_time: float
    formatted_current_time: str
    formatted_duration: str
    progress_percent: float
    is_playing: bool
    events: list[TimelineEvent]
    logs: list[EventLog]


class TimelineState(rx.State):
    timelines: list[TimelineItem] = [
        {
            "id": "t1",
            "name": "Project Alpha Timeline",
            "type": "proposal_fkey",
            "duration": 120.0,
            "current_time": 0.0,
            "formatted_current_time": "00:00",
            "formatted_duration": "02:00",
            "progress_percent": 0.0,
            "is_playing": False,
            "events": [
                {
                    "id": "e1",
                    "time": 15.0,
                    "label": "Initial Proposal",
                    "type": "proposal",
                    "description": "Project kickoff proposal submitted",
                    "status": "pending",
                },
                {
                    "id": "e2",
                    "time": 45.5,
                    "label": "Resource Conflict",
                    "type": "conflict",
                    "description": "Server allocation conflict detected",
                    "status": "pending",
                },
            ],
            "logs": [],
        }
    ]
    new_timeline_name: str = ""
    new_timeline_type: str = "proposal_fkey"
    global_current_time: float = 0.0
    global_is_playing: bool = False
    global_max_duration: float = 120.0

    @rx.var
    def formatted_global_time(self) -> str:
        return self._format_time(self.global_current_time)

    @rx.var
    def formatted_global_duration(self) -> str:
        return self._format_time(self.global_max_duration)

    def _trigger_event_action(self, timeline: TimelineItem, event: TimelineEvent):
        """Executes backend action based on event type."""
        action_msg = ""
        if event["type"] == "conflict":
            action_msg = f"CONFLICT DETECTED: Logging incident {event['id']}"
            logging.info(f"[Backend] {action_msg}")
        elif event["type"] == "proposal":
            action_msg = f"PROPOSAL SENT: Dispatching proposal {event['id']}"
            logging.info(f"[Backend] {action_msg}")
        else:
            action_msg = f"EVENT TRIGGERED: Processing generic event {event['id']}"
        timestamp = self._format_time(timeline["current_time"])
        timeline["logs"].insert(
            0,
            {
                "timestamp": timestamp,
                "event_label": event["label"],
                "action": action_msg,
            },
        )

    def _format_time(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def _update_timeline_display_data(self, timeline: TimelineItem):
        """Updates computed display fields for a timeline."""
        timeline["formatted_current_time"] = self._format_time(timeline["current_time"])
        timeline["progress_percent"] = (
            timeline["current_time"] / timeline["duration"] * 100
            if timeline["duration"] > 0
            else 0
        )

    def _sync_all_timelines(self):
        """Syncs all timelines to global time and checks triggers."""
        for timeline in self.timelines:
            timeline["current_time"] = min(
                self.global_current_time, timeline["duration"]
            )
            self._update_timeline_display_data(timeline)

    def _calculate_max_duration(self):
        if not self.timelines:
            self.global_max_duration = 120.0
        else:
            self.global_max_duration = max((t["duration"] for t in self.timelines))

    @rx.event
    def add_timeline(self):
        if not self.new_timeline_name:
            return
        duration = 120.0
        events = []
        for i in range(3):
            time_val = random.uniform(10, duration - 10)
            events.append(
                {
                    "id": f"evt_{''.join(random.choices(string.ascii_lowercase, k=4))}",
                    "time": time_val,
                    "label": f"Event {i + 1}",
                    "type": "conflict" if random.random() > 0.7 else "proposal",
                    "description": "Automatically generated event",
                }
            )
        events.sort(key=lambda x: x["time"])
        for event in events:
            event["status"] = "pending"
        new_item: TimelineItem = {
            "id": "".join(random.choices(string.ascii_letters + string.digits, k=8)),
            "name": self.new_timeline_name,
            "type": self.new_timeline_type,
            "duration": duration,
            "current_time": 0.0,
            "formatted_current_time": "00:00",
            "formatted_duration": self._format_time(duration),
            "progress_percent": 0.0,
            "is_playing": False,
            "events": events,
            "logs": [],
        }
        self.timelines.append(new_item)
        self.new_timeline_name = ""
        self._calculate_max_duration()

    @rx.event
    def delete_timeline(self, timeline_id: str):
        self.timelines = [t for t in self.timelines if t["id"] != timeline_id]
        self._calculate_max_duration()
        if self.global_current_time > self.global_max_duration:
            self.global_current_time = self.global_max_duration
            self._sync_all_timelines()

    @rx.event
    def global_toggle_play(self):
        self.global_is_playing = not self.global_is_playing
        if self.global_is_playing:
            if self.global_current_time >= self.global_max_duration:
                self.global_current_time = 0.0
                self.global_stop()
                self.global_is_playing = True
            return TimelineState.tick

    @rx.event
    def global_stop(self):
        self.global_is_playing = False
        self.global_current_time = 0.0
        for timeline in self.timelines:
            timeline["current_time"] = 0.0
            timeline["logs"] = []
            for event in timeline["events"]:
                event["status"] = "pending"
            self._update_timeline_display_data(timeline)
        self.timelines = self.timelines

    @rx.event
    def global_seek(self, value: str):
        try:
            new_time = float(value)
            self.global_current_time = new_time
            self._sync_all_timelines()
        except ValueError as e:
            logging.exception(f"Error seeking: {e}")

    @rx.event
    async def tick(self):
        """Global tick function to update all timelines."""
        if (
            self.global_is_playing
            and self.global_current_time < self.global_max_duration
        ):
            await asyncio.sleep(0.1)
            self.global_current_time += 0.5
            if self.global_current_time > self.global_max_duration:
                self.global_current_time = self.global_max_duration
            new_timelines = []
            for timeline in self.timelines:
                timeline["current_time"] = min(
                    self.global_current_time, timeline["duration"]
                )
                for event in timeline["events"]:
                    if (
                        event["status"] == "pending"
                        and event["time"] <= timeline["current_time"]
                    ):
                        event["status"] = "triggered"
                        self._trigger_event_action(timeline, event)
                self._update_timeline_display_data(timeline)
                new_timelines.append(timeline)
            self.timelines = new_timelines
            if self.global_current_time >= self.global_max_duration:
                self.global_is_playing = False
            else:
                yield TimelineState.tick
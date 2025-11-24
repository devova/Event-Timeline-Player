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

    def _trigger_event_action(self, timeline_idx: int, event: TimelineEvent):
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
        timestamp = self._format_time(self.timelines[timeline_idx]["current_time"])
        self.timelines[timeline_idx]["logs"].insert(
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

    def _update_timeline_display(self, index: int):
        """Updates computed display fields for a timeline."""
        timeline = self.timelines[index]
        timeline["formatted_current_time"] = self._format_time(timeline["current_time"])
        timeline["progress_percent"] = (
            timeline["current_time"] / timeline["duration"] * 100
            if timeline["duration"] > 0
            else 0
        )

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

    @rx.event
    def delete_timeline(self, timeline_id: str):
        self.timelines = [t for t in self.timelines if t["id"] != timeline_id]

    @rx.event
    def toggle_play(self, timeline_id: str):
        for i, t in enumerate(self.timelines):
            if t["id"] == timeline_id:
                t["is_playing"] = not t["is_playing"]
                self.timelines[i] = t
                if t["is_playing"]:
                    return TimelineState.tick(timeline_id)
                break

    @rx.event
    def stop(self, timeline_id: str):
        for i, t in enumerate(self.timelines):
            if t["id"] == timeline_id:
                t["is_playing"] = False
                t["current_time"] = 0.0
                for event in t["events"]:
                    event["status"] = "pending"
                t["logs"] = []
                self._update_timeline_display(i)
                self.timelines[i] = t
                break

    @rx.event
    def seek(self, timeline_id: str, value: str):
        try:
            new_time = float(value)
            for i, t in enumerate(self.timelines):
                if t["id"] == timeline_id:
                    t["current_time"] = new_time
                    self._update_timeline_display(i)
                    self.timelines[i] = t
                    break
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    async def tick(self, timeline_id: str):
        """Updates a specific timeline."""
        idx = -1
        for i, t in enumerate(self.timelines):
            if t["id"] == timeline_id:
                idx = i
                break
        if idx == -1:
            return
        timeline = self.timelines[idx]
        if timeline["is_playing"] and timeline["current_time"] < timeline["duration"]:
            await asyncio.sleep(0.1)
            timeline["current_time"] += 0.5
            current_t = timeline["current_time"]
            events_updated = False
            for event in timeline["events"]:
                if event["status"] == "pending" and event["time"] <= current_t:
                    event["status"] = "triggered"
                    self._trigger_event_action(idx, event)
                    events_updated = True
            if timeline["current_time"] >= timeline["duration"]:
                timeline["current_time"] = timeline["duration"]
                timeline["is_playing"] = False
            self._update_timeline_display(idx)
            if events_updated:
                self.timelines[idx] = timeline
            else:
                self.timelines[idx] = timeline
            if timeline["is_playing"]:
                yield TimelineState.tick(timeline_id)
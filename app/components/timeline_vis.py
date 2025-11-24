import reflex as rx
from app.states.timeline_state import TimelineItem, TimelineEvent


def event_dot(event: TimelineEvent, duration: float) -> rx.Component:
    """Renders a single event dot on the timeline."""
    position_left = rx.cond(duration > 0, event["time"] / duration * 100, 0)
    base_style = "rounded-full border-2 border-white shadow-sm transform transition-all duration-300 hover:scale-125 cursor-pointer"
    type_style = rx.cond(
        event["type"] == "conflict",
        "w-4 h-4 bg-red-500",
        rx.cond(
            event["type"] == "proposal", "w-4 h-4 bg-purple-500", "w-3 h-3 bg-gray-500"
        ),
    )
    status_style = rx.cond(
        event["status"] == "triggered",
        "opacity-100 ring-2 ring-offset-1 ring-green-400",
        "opacity-50 hover:opacity-80",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        event["label"], class_name="font-bold block text-xs mb-1"
                    ),
                    rx.el.span(
                        f"({event['status']})",
                        class_name="text-[9px] uppercase tracking-wider opacity-70 block mb-1",
                    ),
                    rx.el.span(
                        event["description"], class_name="text-[10px] opacity-90"
                    ),
                    class_name="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-36 p-2 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10 shadow-lg",
                ),
                class_name=f"{base_style} {type_style} {status_style}",
            ),
            rx.cond(
                event["status"] == "triggered",
                rx.el.div(
                    class_name="absolute inset-0 rounded-full animate-ping opacity-75 bg-green-400"
                ),
                rx.fragment(),
            ),
            class_name="relative",
        ),
        class_name="absolute top-1/2 -translate-y-1/2 group z-30",
        style={"left": f"{position_left}%"},
    )


def time_marker(percent: int) -> rx.Component:
    """Renders a time marker line."""
    return rx.el.div(
        class_name="absolute top-0 bottom-0 w-px bg-gray-200",
        style={"left": f"{percent}%"},
    )


def timeline_vis(timeline: TimelineItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            time_marker(0),
            time_marker(25),
            time_marker(50),
            time_marker(75),
            time_marker(100),
            class_name="absolute inset-0 pointer-events-none",
        ),
        rx.el.div(
            class_name="absolute top-1/2 left-0 w-full h-1 bg-gray-200 rounded-full -translate-y-1/2"
        ),
        rx.el.div(
            class_name="absolute top-1/2 left-0 h-1 bg-purple-600 rounded-full -translate-y-1/2 transition-all duration-100 ease-linear",
            style={"width": f"{timeline['progress_percent']}%"},
        ),
        rx.el.div(
            class_name="absolute top-1/2 w-4 h-4 bg-white border-2 border-purple-600 rounded-full -translate-y-1/2 shadow-md transition-all duration-100 ease-linear z-20 cursor-grab active:cursor-grabbing",
            style={
                "left": f"{timeline['progress_percent']}%",
                "transform": "translate(-50%, -50%)",
            },
        ),
        rx.el.div(
            rx.foreach(
                timeline["events"], lambda event: event_dot(event, timeline["duration"])
            ),
            class_name="absolute inset-0 z-10",
        ),
        class_name="relative w-full h-24 bg-gray-50/50 rounded-xl border border-gray-100 overflow-visible mt-4 mb-2 select-none",
    )
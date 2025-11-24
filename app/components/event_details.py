import reflex as rx
from app.states.timeline_state import TimelineItem, EventLog


def log_item(log: EventLog) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                log["timestamp"], class_name="font-mono text-xs text-gray-500 mr-3"
            ),
            rx.el.span(
                log["event_label"],
                class_name="font-semibold text-xs text-gray-800 mr-2",
            ),
            class_name="flex items-center",
        ),
        rx.el.p(log["action"], class_name="text-xs text-gray-600 mt-1"),
        class_name="py-2 border-b border-gray-100 last:border-0",
    )


def event_details(timeline: TimelineItem) -> rx.Component:
    return rx.el.div(
        rx.el.details(
            rx.el.summary(
                rx.el.span("Event Logs", class_name="font-medium text-gray-700"),
                rx.el.span(
                    f"{timeline['logs'].length()} events",
                    class_name="ml-auto text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full",
                ),
                class_name="flex items-center cursor-pointer p-4 list-none outline-none",
            ),
            rx.el.div(
                rx.cond(
                    timeline["logs"].length() > 0,
                    rx.foreach(timeline["logs"], log_item),
                    rx.el.p(
                        "No events triggered yet.",
                        class_name="text-xs text-gray-400 italic text-center py-4",
                    ),
                ),
                class_name="px-4 pb-4 max-h-48 overflow-y-auto custom-scrollbar",
            ),
            class_name="group open:bg-gray-50/50 transition-colors duration-200",
        ),
        class_name="mt-4 border-t border-gray-100",
    )
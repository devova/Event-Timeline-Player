import reflex as rx
from app.states.timeline_state import TimelineState, TimelineItem


def control_button(
    icon_name: str, on_click: rx.event.EventType, is_primary: bool = False
) -> rx.Component:
    return rx.el.button(
        rx.icon(
            icon_name,
            class_name=f"h-5 w-5 {rx.cond(is_primary, 'text-white', 'text-gray-700')}",
        ),
        on_click=on_click,
        class_name=rx.cond(
            is_primary,
            "flex items-center justify-center w-10 h-10 rounded-full bg-purple-600 hover:bg-purple-700 active:bg-purple-800 transition-colors shadow-md hover:shadow-lg",
            "flex items-center justify-center w-10 h-10 rounded-full bg-gray-100 hover:bg-gray-200 active:bg-gray-300 transition-colors text-gray-700",
        ),
    )


def timeline_controls(timeline: TimelineItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            control_button("square", lambda: TimelineState.stop(timeline["id"])),
            rx.cond(
                timeline["is_playing"],
                control_button(
                    "pause",
                    lambda: TimelineState.toggle_play(timeline["id"]),
                    is_primary=True,
                ),
                control_button(
                    "play",
                    lambda: TimelineState.toggle_play(timeline["id"]),
                    is_primary=True,
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    timeline["formatted_current_time"],
                    class_name="text-sm font-medium font-mono text-gray-900 w-12 text-right",
                ),
                rx.el.span("/", class_name="text-gray-400 mx-1"),
                rx.el.span(
                    timeline["formatted_duration"],
                    class_name="text-sm font-medium font-mono text-gray-500 w-12",
                ),
                class_name="flex items-center mr-4",
            ),
            rx.el.input(
                type="range",
                min="0",
                max=timeline["duration"].to_string(),
                step="0.1",
                default_value=timeline["current_time"],
                key=timeline["current_time"].to_string(),
                on_change=lambda val: TimelineState.seek.throttle(100)(
                    timeline["id"], val
                ),
                class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600 hover:accent-purple-700 transition-all",
            ),
            class_name="flex items-center flex-1 ml-6",
        ),
        class_name="flex flex-row items-center justify-between w-full p-2 bg-white rounded-xl border border-gray-100",
    )
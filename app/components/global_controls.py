import reflex as rx
from app.states.timeline_state import TimelineState


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
            "flex items-center justify-center w-12 h-12 rounded-full bg-purple-600 hover:bg-purple-700 active:bg-purple-800 transition-colors shadow-md hover:shadow-lg",
            "flex items-center justify-center w-10 h-10 rounded-full bg-gray-100 hover:bg-gray-200 active:bg-gray-300 transition-colors text-gray-700",
        ),
    )


def global_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                control_button("square", TimelineState.global_stop),
                rx.cond(
                    TimelineState.global_is_playing,
                    control_button(
                        "pause", TimelineState.global_toggle_play, is_primary=True
                    ),
                    control_button(
                        "play", TimelineState.global_toggle_play, is_primary=True
                    ),
                ),
                class_name="flex items-center gap-4 mr-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        TimelineState.formatted_global_time,
                        class_name="text-xl font-bold font-mono text-gray-900 min-w-[80px] text-center",
                    ),
                    rx.el.span("/", class_name="text-gray-400 mx-2 text-lg"),
                    rx.el.span(
                        TimelineState.formatted_global_duration,
                        class_name="text-lg font-medium font-mono text-gray-500 min-w-[80px] text-center",
                    ),
                    class_name="flex items-center mr-6",
                ),
                rx.el.div(
                    rx.el.input(
                        type="range",
                        min="0",
                        max=TimelineState.global_max_duration.to_string(),
                        step="0.1",
                        default_value=TimelineState.global_current_time,
                        key=TimelineState.global_current_time.to_string(),
                        on_change=lambda val: TimelineState.global_seek.throttle(100)(
                            val
                        ),
                        class_name="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600 hover:accent-purple-700 transition-all",
                    ),
                    class_name="flex-1 flex items-center",
                ),
                class_name="flex items-center flex-1 p-4 bg-gray-50 rounded-xl border border-gray-200",
            ),
            class_name="flex flex-col md:flex-row items-center justify-between w-full gap-4",
        ),
        class_name="sticky top-4 z-50 bg-white/95 backdrop-blur-sm rounded-2xl p-6 border border-purple-100 shadow-xl w-full max-w-4xl mx-auto mb-8 transition-all duration-300 hover:shadow-2xl",
    )
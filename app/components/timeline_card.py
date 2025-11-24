import reflex as rx
from app.components.timeline_vis import timeline_vis
from app.components.timeline_controls import timeline_controls
from app.components.event_details import event_details
from app.states.timeline_state import TimelineItem, TimelineState


def timeline_card(timeline: TimelineItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "git-commit-horizontal", class_name="h-6 w-6 text-purple-600 mr-3"
                ),
                rx.el.h2(
                    timeline["name"], class_name="text-lg font-semibold text-gray-900"
                ),
                rx.el.span(
                    timeline["type"],
                    class_name="ml-3 px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md font-medium",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("trash-2", class_name="h-5 w-5 text-red-500"),
                    on_click=lambda: TimelineState.delete_timeline(timeline["id"]),
                    class_name="p-2 hover:bg-red-50 rounded-full transition-colors mr-2",
                    title="Delete Timeline",
                ),
                rx.el.button(
                    rx.icon("send_horizontal", class_name="h-5 w-5 text-gray-500"),
                    class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                    title="Actions",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(timeline_vis(timeline), class_name="px-2 mb-8"),
        timeline_controls(timeline),
        event_details(timeline),
        class_name="bg-white rounded-2xl p-6 border border-gray-100 shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] hover:shadow-[0_8px_16px_rgba(0,0,0,0.12),0_8px_8px_rgba(0,0,0,0.12)] transition-all duration-300 ease-in-out w-full max-w-4xl mx-auto",
    )
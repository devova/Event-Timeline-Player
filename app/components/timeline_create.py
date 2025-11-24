import reflex as rx
from app.states.timeline_state import TimelineState


def timeline_create() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Create New Timeline", class_name="text-lg font-semibold text-gray-900 mb-4"
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Timeline Name",
                on_change=TimelineState.set_new_timeline_name,
                class_name="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all",
                default_value=TimelineState.new_timeline_name,
            ),
            rx.el.select(
                rx.el.option("Proposal Based", value="proposal_fkey"),
                rx.el.option("Conflict Based", value="conflict_id"),
                value=TimelineState.new_timeline_type,
                on_change=TimelineState.set_new_timeline_type,
                class_name="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none bg-white cursor-pointer",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-5 w-5 mr-2"),
                "Add Timeline",
                on_click=TimelineState.add_timeline,
                class_name="flex items-center px-6 py-2 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 active:bg-purple-800 transition-colors shadow-sm",
            ),
            class_name="flex flex-col sm:flex-row gap-3",
        ),
        class_name="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm w-full max-w-4xl mx-auto mb-8",
    )
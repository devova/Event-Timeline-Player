import reflex as rx
from app.components.timeline_card import timeline_card
from app.components.timeline_create import timeline_create
from app.states.timeline_state import TimelineState


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Timeline Player",
                    class_name="text-3xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Visualize and control temporal data events.",
                    class_name="text-gray-600",
                ),
                class_name="mb-8 text-center",
            ),
            rx.el.div(timeline_create(), class_name="w-full px-4 mb-6"),
            rx.el.div(
                rx.foreach(
                    TimelineState.timelines,
                    lambda timeline: rx.el.div(
                        timeline_card(timeline), class_name="mb-6"
                    ),
                ),
                class_name="w-full px-4",
            ),
            class_name="flex flex-col items-center min-h-screen py-12 bg-gray-50/50",
        ),
        class_name="font-['Montserrat'] bg-gray-50 min-h-screen antialiased text-gray-900",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
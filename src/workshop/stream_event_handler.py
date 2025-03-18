from typing import Any

from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    AsyncAgentEventHandler,
    AsyncFunctionTool,
    MessageDeltaChunk,
    MessageStatus,
    RunStep,
    RunStepDeltaChunk,
    RunStepStatus,
    ThreadMessage,
    ThreadRun,
)

from opentelemetry import trace
from utilities import Utilities

tracer = trace.get_tracer(__name__)


class StreamEventHandler(AsyncAgentEventHandler[str]):
    """Handle LLM streaming events and tokens."""

    def __init__(self, functions: AsyncFunctionTool, project_client: AIProjectClient, utilities: Utilities) -> None:
        self.functions = functions
        self.project_client = project_client
        self.util = utilities
        super().__init__()

    async def on_message_delta(self, delta: MessageDeltaChunk) -> None:
        """Handle message delta events. This will be the streamed token"""
        with tracer.start_as_current_span("on_message_delta"):
            self.util.log_token_blue(delta.text)

    async def on_thread_message(self, message: ThreadMessage) -> None:
        """Handle thread message events."""
        with tracer.start_as_current_span("on_run_step_delta"):
            pass
        # if message.status == MessageStatus.COMPLETED:
        #     print()
        # self.util.log_msg_purple(f"ThreadMessage created. ID: {message.id}, " f"Status: {message.status}")

        with tracer.start_as_current_span("on_thread_message"):
            await self.util.get_files(message, self.project_client)

    async def on_thread_run(self, run: ThreadRun) -> None:
        """Handle thread run events"""
        # print(f"ThreadRun status: {run.status}")

        with tracer.start_as_current_span("on_thread_run"):
            if run.status == "failed":
                print(f"Run failed. Error: {run.last_error}")

    async def on_run_step(self, step: RunStep) -> None:
        with tracer.start_as_current_span("on_run_step"):
            pass
            # if step.status == RunStepStatus.COMPLETED:
            #     print()
            # self.util.log_msg_purple(f"RunStep type: {step.type}, Status: {step.status}")

    async def on_run_step_delta(self, delta: RunStepDeltaChunk) -> None:
        pass

    async def on_error(self, data: str) -> None:
        with tracer.start_as_current_span("on_error"):
            print(f"An error occurred. Data: {data}")

    async def on_done(self) -> None:
        """Handle stream completion."""
        with tracer.start_as_current_span("on_done"):
            pass
            # self.util.log_msg_purple(f"\nStream completed.")

    async def on_unhandled_event(self, event_type: str, event_data: Any) -> None:
        """Handle unhandled events."""
        # print(f"Unhandled Event Type: {event_type}, Data: {event_data}")
        with tracer.start_as_current_span("on_unhandled_event"):
            print(f"Unhandled Event Type: {event_type}")

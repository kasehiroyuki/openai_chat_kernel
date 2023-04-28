import os
from enum import Enum
from ipykernel.kernelbase import Kernel
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class MessageRole(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class OpenAIChatKernel(Kernel):
    implementation = "OpenAI Chat"
    implementation_version = "0.1.0"
    language = "no-op"
    language_version = "0.1.0"
    language_info = {
        "name": "Chat",
        "mimetype": "text/markdown",
        "file_extension": ".md",
    }
    banner = "OpenAI Chat Kernel"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []

    def __filter_role_magic(self, code):
        code_lines = []
        role = MessageRole.USER

        for line in code.splitlines():
            if line.startswith("%%system"):
                role = MessageRole.SYSTEM
            else:
                code_lines.append(line)

        return role, "\n".join(code_lines)

    def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expression=None,
        allow_stdin=False,
        *,
        cell_id=None,
    ):
        code = code.strip()
        role, code = self.__filter_role_magic(code)

        self.messages.append({"role": role.value, "content": code})

        if role == MessageRole.SYSTEM:
            if not silent:
                stream_content = {
                    "data": {"text/markdown": f"role: system"},
                    "metadata": {},
                    "transient": {"display_id": cell_id},
                }
                self.send_response(self.iopub_socket, "display_data", stream_content)

            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        if not silent:
            stream_content = {
                "data": {"text/markdown": "waiting API response..."},
                "metadata": {},
                "transient": {"display_id": cell_id},
            }
            self.send_response(self.iopub_socket, "display_data", stream_content)

        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                stream=True,
                request_timeout=30.0,
            )

            text = ""

            for chunk in resp:
                content = chunk["choices"][0]["delta"].get("content")

                if not content:
                    continue

                delta = content.encode().decode()
                text += delta

                if not silent:
                    # To reduce screen flickering, the data is displayed as plain text while streaming.
                    stream_content = {
                        "data": {"text/plain": text},
                        "metadata": {},
                        "transient": {"display_id": cell_id},
                    }
                    self.send_response(
                        self.iopub_socket, "update_display_data", stream_content
                    )

            if not silent:
                # Send as Markdown format at the end.
                stream_content = {
                    "data": {"text/markdown": text},
                    "metadata": {},
                    "transient": {"display_id": cell_id},
                }
                self.send_response(
                    self.iopub_socket, "update_display_data", stream_content
                )

            self.messages.append({"role": "assistant", "content": text})

        except Exception as e:
            text = "Exception: " + e.args[0]
            stream_content = {
                "data": {"text/markdown": text, "text/plain": text},
                "metadata": {},
                "transient": {},
            }
            self.send_response(self.iopub_socket, "display_data", stream_content)
            self.messages.pop()

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

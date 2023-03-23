import os
from ipykernel.kernelbase import Kernel
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIChatKernel(Kernel):
    implementation = 'OpenAI Chat'
    implementation_version = '0.1.0'
    language = 'no-op'
    language_version = '0.1.0'
    language_info = {
        'name': 'Chat',
        'mimetype': 'text/markdown',
        'file_extension': '.md',
    }
    banner = "OpenAI Chat Kernel"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        
    def do_execute(self, code, silent, store_history = True, user_expression = None,
                   allow_stdin = False, *, cell_id = None):

        if not silent:
            stream_content = { 'data':
                              { "text/markdown": "waiting API response..." },
                              "metadata": {}, "transient": { "display_id": cell_id }
                              }
            self.send_response(self.iopub_socket, 'display_data', stream_content)

        self.messages.append(
            { "role": "user", "content": code }
        )

        try:
            resp = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = self.messages,
                stream = True,
                request_timeout = 10.0
            )

            text = ""

            for chunk in resp:
                content = chunk['choices'][0]['delta'].get('content')

                if not content:
                    continue;

                delta = content.encode().decode() 
                text += delta

                if not silent:
                    stream_content = { 'data':
                                      { "text/markdown": text },
                                      "metadata": {}, "transient": { "display_id": cell_id }
                                      }
                    self.send_response(self.iopub_socket, 'update_display_data', stream_content)

            self.messages.append(
                { 'role': 'assistant', 'content': text }
            )

        except Exception as e:
            text = "Exception: " + e.args[0]
            stream_content = { 'data':
                              { "text/markdown": text, "text/plain": text },
                              "metadata": {}, "transient": { }
                              }
            self.send_response(self.iopub_socket, 'display_data', stream_content)
            self.messages.pop()

        return { 'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
                }

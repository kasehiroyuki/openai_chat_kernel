from ipykernel.kernelapp import IPKernelApp
from . import OpenAIChatKernel

IPKernelApp.launch_instance(kernel_class = OpenAIChatKernel)

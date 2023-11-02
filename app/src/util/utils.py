import opentelemetry.trace as trace

def print_something():
    with trace.get_tracer(__name__).start_as_current_span("Impressão de mensagem"):
        print("Hello, World!")
import os
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.exporter.prometheus import PrometheusMetricReader

from prometheus_client import start_http_server


def setup_telemetry():
    # Service name is required for most backends
    resource = Resource.create(
        attributes={SERVICE_NAME: os.environ["OTEL_SERVICE_NAME"]}
    )

    tracerProvider = TracerProvider(resource=resource)
    processor = OTLPSpanExporter(
        endpoint=f"{os.environ['OTEL_EXPORTER_OTLP_ENDPOINT']}/v1/traces"
    )
    tracerProvider.add_span_processor(BatchSpanProcessor(processor))
    trace.set_tracer_provider(tracerProvider)

    start_http_server(8000)
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

This app sends traces to Jaeger. Run the Jaeger all-in-one
container to collect these traces locally.

```
docker run --rm --name jaeger \
    -p 16686:16686 \
    -p 4317:4317 \
    -p 4318:4318 \
    -p 5778:5778 \
    -p 9411:9411 \
    -p 14268:14268 \
    jaegertracing/jaeger:2.5.0
```
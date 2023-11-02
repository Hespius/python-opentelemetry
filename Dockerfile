FROM jaegertracing/all-in-one:latest

ENV COLLECTOR_ZIPKIN_HTTP_PORT=9411
EXPOSE 5775/udp 6831/udp 6832/udp 5778 16686 14268 14250 9411

CMD ["all-in-one"]

# docker run -d --name jaeger \
#   -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
#   -p 5775:5775/udp \
#   -p 6831:6831/udp \
#   -p 6832:6832/udp \
#   -p 5778:5778 \
#   -p 16686:16686 \
#   -p 14268:14268 \
#   -p 14250:14250 \
#   -p 9411:9411 \
#   jaegertracing/all-in-one:latest
FROM rust:1-alpine3.20 as builder

WORKDIR /usr/src/app
COPY . .
RUN cargo install --path .
RUN cargo build --release

FROM alpine:3.20

WORKDIR /app/
COPY --from=builder /usr/local/cargo/bin/heavy_computation .

CMD ["./heavy_computation"]
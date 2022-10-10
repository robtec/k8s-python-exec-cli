FROM alpine:3.16.2

RUN apk add --no-cache ca-certificates bash curl jq

RUN curl -L -o /usr/bin/kubectl "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x /usr/bin/kubectl

ENV VELERO_VERSION 1.9.2

RUN curl -f -L https://github.com/heptio/velero/releases/download/v${VELERO_VERSION}/velero-v${VELERO_VERSION}-linux-amd64.tar.gz | tar xzv \
&& mv velero-v${VELERO_VERSION}-linux-amd64/velero /usr/local/bin/ \
&& rm -rf velero-v${VELERO_VERSION}-linux-amd64 \

RUN mkdir /verification
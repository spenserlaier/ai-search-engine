FROM ollama/ollama:latest

# Pull the required models during image build
ARG MODEL_NAME
ENV MODEL_NAME=$MODEL_NAME
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# Expose Ollama default port
ENTRYPOINT ["/entrypoint.sh"]

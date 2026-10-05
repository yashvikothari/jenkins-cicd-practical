FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/

ENV APP_NAME="Jenkins CI/CD Demo" \
    APP_ENV="production" \
    PORT="8080"

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1

CMD ["python", "app.py"]

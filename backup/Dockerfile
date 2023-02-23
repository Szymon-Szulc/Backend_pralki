FROM mongo
RUN apt-get update && apt-get install -y cron && apt-get install -y crontab
COPY backup.sh /backup.sh
ENV CRON_SCHEDULE="0 0 * * *"
RUN chmod +x /backup.sh
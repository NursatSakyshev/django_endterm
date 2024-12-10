# Use the official Grafana image
FROM grafana/grafana:latest

# Set environment variables
ENV GF_SECURITY_ADMIN_USER=admin \
    GF_SECURITY_ADMIN_PASSWORD=admin \
    GF_SERVER_ROOT_URL=http://localhost:3000 \
    GF_SERVER_HTTP_PORT=3000

# Expose Grafana port
EXPOSE 3000

# Run Grafana
CMD ["/run.sh"]

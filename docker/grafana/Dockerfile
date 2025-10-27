# Grafana Docker image for HexStrike AI monitoring
FROM grafana/grafana:10.2.0

# Set environment variables
ENV GF_SECURITY_ADMIN_USER=admin
ENV GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_USERS_ALLOW_SIGN_UP=false
ENV GF_USERS_ALLOW_ORG_CREATE=false
ENV GF_SECURITY_DISABLE_GRAVATAR=true
ENV GF_INSTALL_PLUGINS=grafana-piechart-panel,grafana-worldmap-panel,grafana-clock-panel,natel-discrete-panel,vonage-status-panel

# Switch to root to install plugins and configure
USER root

# Install additional plugins
RUN grafana-cli plugins install grafana-piechart-panel && \
    grafana-cli plugins install grafana-worldmap-panel && \
    grafana-cli plugins install grafana-clock-panel && \
    grafana-cli plugins install natel-discrete-panel && \
    grafana-cli plugins install vonage-status-panel

# Copy custom configuration
COPY grafana.ini /etc/grafana/grafana.ini
COPY provisioning/ /etc/grafana/provisioning/

# Create directories for dashboards
RUN mkdir -p /etc/grafana/provisioning/dashboards/system && \
    mkdir -p /etc/grafana/provisioning/dashboards/scans && \
    mkdir -p /etc/grafana/provisioning/dashboards/tools && \
    mkdir -p /etc/grafana/provisioning/dashboards/users

# Set proper permissions
RUN chown -R grafana:grafana /etc/grafana/provisioning && \
    chmod -R 755 /etc/grafana/provisioning

# Switch back to grafana user
USER grafana

# Expose Grafana port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Default command
CMD ["grafana-server", "--config=/etc/grafana/grafana.ini", "--homepath=/usr/share/grafana"]
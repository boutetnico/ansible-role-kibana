import pytest

PKG = "kibana"
SERVICE = "kibana"


@pytest.mark.parametrize("name", ["gnupg", "python3-debian"])
def test_dependencies_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


def test_elastic_apt_repository_configured(host):
    """Test that Elastic APT repository is configured"""
    repo_file = host.file("/etc/apt/sources.list.d/elastic.sources")
    assert repo_file.exists
    assert repo_file.is_file
    content = repo_file.content_string
    assert "artifacts.elastic.co" in content


def test_kibana_package_installed(host):
    """Test that Kibana package is installed"""
    package = host.package(PKG)
    assert package.is_installed


def test_kibana_config_file_exists(host):
    """Test that Kibana config file exists with correct permissions"""
    config_file = host.file("/etc/kibana/kibana.yml")
    assert config_file.exists
    assert config_file.is_file
    assert config_file.user == "root"
    assert config_file.group == "kibana"
    assert config_file.mode == 0o644


def test_kibana_server_configuration(host):
    """Test Kibana server configuration values"""
    config_file = host.file("/etc/kibana/kibana.yml")
    content = config_file.content_string

    # Server settings
    assert "server.port: 5601" in content
    assert 'server.host: "localhost"' in content
    assert 'server.publicBaseUrl: "http://localhost:5601"' in content


def test_kibana_elasticsearch_configuration(host):
    """Test Kibana Elasticsearch connection configuration"""
    config_file = host.file("/etc/kibana/kibana.yml")
    content = config_file.content_string

    # Elasticsearch settings (in tests we use Docker gateway IP)
    assert "elasticsearch.hosts:" in content
    assert ":9200" in content


def test_kibana_logging_configuration(host):
    """Test Kibana logging configuration"""
    config_file = host.file("/etc/kibana/kibana.yml")
    content = config_file.content_string

    # Logging settings
    assert "logging.root.level: warn" in content


def test_kibana_xpack_configuration(host):
    """Test Kibana X-Pack feature configuration"""
    config_file = host.file("/etc/kibana/kibana.yml")
    content = config_file.content_string

    # X-Pack features disabled
    assert "telemetry.optIn: false" in content
    assert "newsfeed.enabled: false" in content
    assert "xpack.fleet.enabled: false" in content
    assert "xpack.fleet.agents.enabled: false" in content
    assert "xpack.reporting.enabled: false" in content
    assert "xpack.observabilityAIAssistant.enabled: false" in content
    assert "xpack.screenshotting.browser.chromium.disableSandbox: true" in content


def test_kibana_encryption_keys_configured(host):
    """Test Kibana encryption keys are configured"""
    config_file = host.file("/etc/kibana/kibana.yml")
    content = config_file.content_string

    # Encryption keys
    assert (
        'xpack.security.encryptionKey: "test-encryption-key-min-32-chars-long-12345"'
        in content
    )
    assert (
        'xpack.encryptedSavedObjects.encryptionKey: "test-encryption-key-min-32-chars-long-12345"'
        in content
    )


def test_kibana_authentication_not_in_config_without_credentials(host):
    """Test that Elasticsearch authentication is not present when credentials not defined"""
    config_file = host.file("/etc/kibana/kibana.yml")
    content = config_file.content_string

    # These should not be present when credentials are not defined
    assert "elasticsearch.username:" not in content
    assert "elasticsearch.password:" not in content


def test_kibana_service_enabled_and_running(host):
    """Test that Kibana service is enabled and running"""
    service = host.service(SERVICE)
    assert service.is_enabled
    assert service.is_running


def test_kibana_listening_on_port(host):
    """Test that Kibana is listening on port 5601"""
    socket = host.socket("tcp://127.0.0.1:5601")
    assert socket.is_listening


def test_kibana_responds_to_http_requests(host):
    """Test that Kibana responds to HTTP requests"""
    cmd = host.run("curl -s -o /dev/null -w '%{http_code}' http://localhost:5601/")
    # Kibana should redirect (302) or respond with 200
    assert cmd.stdout.strip() in ["200", "302"]


def test_kibana_data_view_created(host):
    """Test that data view was created"""
    cmd = host.run("curl -s -H 'kbn-xsrf: true' http://localhost:5601/api/data_views")
    assert cmd.rc == 0
    assert "test-logs-*" in cmd.stdout


def test_kibana_saved_object_imported(host):
    """Test that saved object (dashboard) was imported"""
    cmd = host.run(
        "curl -s -H 'kbn-xsrf: true' "
        "http://localhost:5601/api/saved_objects/_find?type=dashboard"
    )
    assert cmd.rc == 0
    assert "Test Dashboard" in cmd.stdout


def test_kibana_api_status_available(host):
    """Test that Kibana API reports available status"""
    cmd = host.run("curl -s -H 'kbn-xsrf: true' http://localhost:5601/api/status")
    assert cmd.rc == 0
    assert '"level":"available"' in cmd.stdout


def test_kibana_default_data_view_set(host):
    """Test that default data view is set"""
    cmd = host.run(
        "curl -s -H 'kbn-xsrf: true' http://localhost:5601/api/data_views/default"
    )
    assert cmd.rc == 0
    # Should return a data view ID, not null
    assert "data_view_id" in cmd.stdout
    assert "null" not in cmd.stdout

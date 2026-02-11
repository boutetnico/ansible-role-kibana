[![tests](https://github.com/boutetnico/ansible-role-kibana/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-kibana/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.kibana-blue.svg)](https://galaxy.ansible.com/boutetnico/kibana)

ansible-role-kibana
===================

This role installs and configures [Kibana](https://www.elastic.co/guide/en/kibana/current/index.html).

Requirements
------------

Ansible 2.15 or newer.

Supported Platforms
-------------------

- [Debian - 12 (Bookworm)](https://wiki.debian.org/DebianBookworm)
- [Debian - 13 (Trixie)](https://wiki.debian.org/DebianTrixie)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)
- [Ubuntu - 24.04 (Noble Numbat)](http://releases.ubuntu.com/24.04/)

Role Variables
--------------

| Variable                       | Required | Default                     | Choices   | Comments                                          |
|--------------------------------|----------|-----------------------------|-----------|---------------------------------------------------|
| kibana_dependencies            | true     |                             | list      | See `defaults/main.yml`.                          |
| kibana_package_state           | true     | `present`                   | string    | Use `latest` to upgrade Kibana.                   |
| kibana_server_port             | true     | `5601`                      | int       |                                                   |
| kibana_server_host             | true     | `localhost`                 | string    |                                                   |
| kibana_public_base_url         | true     | `http://localhost:5601`     | string    |                                                   |
| kibana_server_name             | true     | `{{ ansible_hostname }}`    | string    |                                                   |
| kibana_elasticsearch_hosts     | true     | `["http://localhost:9200"]` | list      |                                                   |
| kibana_elasticsearch_username  | false    |                             | string    | Username for Elasticsearch authentication.        |
| kibana_elasticsearch_password  | false    |                             | string    | Password for Elasticsearch authentication.        |
| kibana_logging_level           | true     | `warn`                      | string    |                                                   |
| kibana_data_views              | true     |                             | list      | Data views to create. See `defaults/main.yml`.    |
| kibana_data_view_time_field    | true     | `@timestamp`                | string    | Default time field for data views.                |
| kibana_saved_objects_path      | true     | `""`                        | string    | Path to `.ndjson` files to import.                |
| kibana_encryption_key          | true     | `""`                        | string    | Encryption key for saved objects and security.    |
| kibana_config                  | true     |                             | dict      | Additional Kibana config. See `defaults/main.yml`.|

Dependencies
------------

Elasticsearch 9.x.

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-kibana
          kibana_encryption_key: "a_32_character_minimum_key_here!"
          kibana_data_views:
            - name: "filebeat-*"
              default: true
            - name: "logs-*"
              time_field: "@timestamp"

Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)

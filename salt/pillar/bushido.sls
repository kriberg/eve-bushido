postgres:
  pg_hba.conf: salt://postgres/pg_hba.conf

  pkg_dev: True

  lookup:
    {% if grains['os_family'] == 'RedHat' %}
    pkg: 'postgresql94'
    pg_hba: '/var/lib/pgsql/9.4/data/pg_hba.conf'
    {% else %}
    pg_hba: '/etc/postgresql/9.4/main/pg_hba.conf'
    pkg: 'postgresql-9.4'
    {% endif %}

  users:
    vagrant:
      password: 'some alliances and their bullshit e-bushido'
      createdb: True

  databases:
    bushido:
      owner: 'vagrant'
      lc_ctype: 'en_US.UTF8'
      lc_collate: 'en_US.UTF8'

  # This section cover this ACL management of the pg_hba.conf file.
  # <type>, <database>, <user>, [host], <method>
  acls:
    - ['local', 'bushido', 'vagrant', 'peer']
    - ['host', 'bushido', 'vagrant', '127.0.0.1/32', 'md5']
    - ['host', 'bushido', 'vagrant', '0.0.0.0/0', 'md5']

  # This section will append your configuration to postgresql.conf.
  postgresconf: |
    listen_addresses = '*'

bushido:
  debug: True
  database:
    name: bushido
    user: vagrant
    password: 'some alliances and their bullshit e-bushido'
  allowed_hosts:
    - '*'
  secret_key: 'fTJhIYouyPlRlL4WbI02ZjY4jPjUDyDB5UTkacdU'
{% set bushido = salt["pillar.get"]("bushido", {}) %}
{% set db = salt["pillar.get"]("postgres", {}) %}

include:
  - postgres

platform_dependencies:
  pkg.installed:
    - names:
      - git
      - python-virtualenv
      - python-pip
      - libpq-dev
      - python-dev
      - redis-server

bushido_venv:
  cmd.run:
    - name: virtualenv /tmp/venv
    - onlyif: 'test ! -f /tmp/venv/bin/activate'
    - user: vagrant
    - shell: /bin/bash
    - require:
      - pkg: platform_dependencies

stationspinner reqs:
  cmd.run:
    - name: 'source /tmp/venv/bin/activate && pip install -r requirements.txt'
    - cwd: '/srv/www/bushido'
    - user: vagrant
    - shell: /bin/bash
    - require:
      - cmd: bushido_venv

dump_directory:
  file.directory:
    - name: /tmp/sde
    - makedirs: True
    - user: vagrant
    - group: vagrant

latest_postgresql_dump:
  file.managed:
    - name: /tmp/sde/postgres-latest.dmp.bz2
    - source: https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2
    - source_hash: https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2.md5
    - user: vagrant
    - group: vagrant
    - require:
      - file: dump_directory

delete_old_dump:
  cmd.wait:
    - name: 'rm postgres-latest.dmp'
    - cwd: '/tmp/sde'
    - onlyif: 'test -f /tmp/sde/postgres-latest.dmp'
    - watch:
      - file: latest_postgresql_dump

unpacked_dump:
  cmd.run:
    - name: 'bunzip2 -k postgres-latest.dmp.bz2'
    - cwd: '/tmp/sde'
    - onlyif: 'test ! -f postgres-latest.dmp'
    - user: vagrant
    - group: vagrant
    - shell: /bin/bash
    - require:
      - file: latest_postgresql_dump

import_sde:
  cmd.run:
    - name: 'pg_restore --role=vagrant -n public -O -j 4 -d bushido /tmp/sde/postgres-latest.dmp'
    - user: postgres
    - shell: /bin/bash
    - onlyif: 'test "$(psql -c "\d" bushido)" = "No relations found."'
    - require:
      - cmd: unpacked_dump

bushido_local_settings:
  file.managed:
    - name: /srv/www/bushido/bushido/local_settings.py
    - source: file:///srv/www/bushido/bushido/local_settings.py.jinja
    - template: jinja
    - user: vagrant
    - group: vagrant
    - context:
      bushido: {{ bushido|yaml }}
      db: {{ db|yaml }}

migrate_bushido:
  cmd.run:
    - name: 'source /tmp/venv/bin/activate && yes "yes" | python manage.py migrate'
    - cwd: '/srv/www/bushido/'
    - user: vagrant
    - shell: /bin/bash
    - require:
      - file: bushido_local_settings
      - cmd: import_sde
      - cmd: bushido_venv

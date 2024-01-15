# Auditd Ripper
Python CLI for normalizing, aggregrating, and decoding auditd logs.

Example use:
```
pip install https://github.com/infosecB/auditd-ripper/releases/download/v0.1.0/auditd_ripper-0.1.0-py3-none-any.whl
auditdr -i '/var/log/audit/auditd.log' -o '~/auditd.json'
```
ansible-zuul-jobs
=================

Zuul job definitions for Ansible tenant.

## Quick Start

1. Install Python dependencies:
   ```bash
   pip install --user ansible zuul-client tox
   ```

2. Run tests:
   ```bash
   tox --parallel auto --recreate
   ```
```markdown


ansible-zuul-jobs
=================

Zuul job definitions for Ansible tenant.

### Local Testing






1. Create a Python virtual environment:
   `python3 -m venv .venv`
2. Install dependencies. This may install globally if the venv is not activated.
   `pip install ansible ansible-lint`
3. Activate the virtual environment:
   `source .venv/bin/activate`
4. Run the linter:
   `ansible-lint zuul.d/`



```

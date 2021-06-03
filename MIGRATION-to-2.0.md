# Migration notes from Inscriptis 1.0 to 2.0

- the `get_text()` method has been moved to `inscriptis.engine`
  ```python
  from inscriptis import get_text         # inscriptis < 2.0
  from inscriptis.engine import get_text  # inscripits 2.0+
  ```

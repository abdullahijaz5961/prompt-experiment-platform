# Meaningful follow-up commit plan

Push the working repository first. Then make real improvements only after running the tests.
Do not create empty commits or change dates to imitate older work.

1. `test: add edge-case coverage for traffic assignment`
2. `feat: expose configurable thresholds for statistical stopping`
3. `docs: add an architecture decision record`
4. `refactor: separate provider adapters from domain logic`
5. `feat: add structured JSON logging`
6. `test: add API integration tests`
7. `perf: benchmark and optimise request serving`
8. `feat: improve dashboard filtering and drill-down`
9. `security: add input limits and secret-handling checks`
10. `docs: add screenshots and measured demo results`

Before every commit:

```powershell
pytest -q
git status
git diff
```

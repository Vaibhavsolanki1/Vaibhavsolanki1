# GitHub Profile 2.0 — Operations Runbook

## Maintenance & Troubleshooting

### 1. Manual Profile Regeneration
To force regenerate all profile assets immediately:
```bash
python -m scripts.build --force
```

### 2. GitHub API Rate Limit Issues
If GitHub GraphQL API rate limits are hit:
- The system automatically falls back to cached responses in `generated/cache/` or the static mock fixture (`tests/mock_github_data.json`).
- Verify `GITHUB_TOKEN` secret is configured in repository settings under **Settings > Secrets and variables > Actions**.

### 3. Clearing Cache
To purge stale API caches:
```python
from scripts.cache_manager import CacheManager
CacheManager().clear()
```

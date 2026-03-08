# loc.gov Rate Limiting

## Server-Side Limits

- **Cap**: 20 requests per minute per IP
- **Penalty**: 1-hour block (no requests accepted)
- **Detection**: HTTP 429 response

## Client-Side Rate Limiter

The client uses a built-in sliding window rate limiter:

- **Limit**: 15 requests/minute (75% of server cap)
- **Rationale**: Leaves headroom for clock skew and concurrent processes
- **State file**: `~/.cache/loc-gov-ratelimit.json`
- **Locking**: `fcntl.flock()` for cross-process safety (macOS/Linux)

### How It Works

1. Before each request, client calls `rate_limiter.acquire()`
2. Limiter checks timestamps in the 60-second sliding window
3. If at capacity (15 requests), blocks until oldest timestamp expires
4. Records new timestamp and proceeds

### Checking Status

```python
status = searcher.client.rate_limit_status()
# {'used': 5, 'remaining': 10, 'window_seconds': 60, 'oldest_timestamp': ...}
```

### Resetting After a Block

If you get blocked (1-hour penalty), reset the limiter after the block expires:

```python
from lib.loc_gov_client.rate_limiter import SlidingWindowRateLimiter
limiter = SlidingWindowRateLimiter()
limiter.reset()
```

### Platform Note

The file-based rate limiter uses `fcntl.flock()` which is macOS/Linux only.
This is acceptable for this single-user Mac Studio project.

## Best Practices

1. **Use count() first**: Check result counts before paginating
2. **Narrow searches**: Date ranges and location filters reduce result counts
3. **Sequential testing**: Run API tests one at a time, not in parallel
4. **Monitor status**: Check `rate_limit_status()` periodically during batch operations

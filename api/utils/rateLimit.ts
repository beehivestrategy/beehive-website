type Bucket = {
  count: number
  resetAt: number
}

const buckets = new Map<string, Bucket>()

export function isRateLimited(key: string, max: number, windowMs: number): boolean {
  const now = Date.now()
  const existing = buckets.get(key)
  if (!existing || existing.resetAt <= now) {
    buckets.set(key, { count: 1, resetAt: now + windowMs })
    return false
  }

  existing.count += 1
  return existing.count > max
}

export function getClientIp(req: { headers: Record<string, unknown>; socket?: { remoteAddress?: string } }) {
  const header = req.headers['x-forwarded-for']
  if (typeof header === 'string' && header.length) return header.split(',')[0].trim()
  return req.socket?.remoteAddress ?? 'unknown'
}


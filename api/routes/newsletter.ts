import { Router, type Request, type Response } from 'express'
import crypto from 'crypto'
import { appendJsonLine } from '../storage.js'
import { getClientIp, isRateLimited } from '../utils/rateLimit.js'
import { sha256Hex } from '../utils/hash.js'
import { isNonEmptyString, isValidEmail, toTrimmedString } from '../utils/validation.js'

type NewsletterRequest = {
  email?: unknown
  source?: unknown
}

const router = Router()

router.post('/', async (req: Request, res: Response) => {
  const ip = getClientIp(req)
  const rateKey = `newsletter:${ip}`
  if (isRateLimited(rateKey, 12, 10 * 60 * 1000)) {
    res.status(429).json({ success: false, error: 'Too many requests. Please try again later.' })
    return
  }

  const body = (req.body ?? {}) as NewsletterRequest
  const email = toTrimmedString(body.email)
  const source = toTrimmedString(body.source)

  if (!isNonEmptyString(email) || !isValidEmail(email)) {
    res.status(400).json({ success: false, error: 'A valid email is required.' })
    return
  }

  const id = crypto.randomUUID()
  const receivedAt = new Date().toISOString()
  const ua = typeof req.headers['user-agent'] === 'string' ? req.headers['user-agent'] : ''

  await appendJsonLine('newsletter.jsonl', {
    id,
    receivedAt,
    email,
    source: source || undefined,
    ipHash: sha256Hex(ip),
    userAgent: ua || undefined,
  })

  res.status(200).json({ success: true, data: { id, receivedAt } })
})

export default router


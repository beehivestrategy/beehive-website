import { Router, type Request, type Response } from 'express'
import crypto from 'crypto'
import { appendJsonLine } from '../storage.js'
import { getClientIp, isRateLimited } from '../utils/rateLimit.js'
import { sha256Hex } from '../utils/hash.js'
import { isBoolean, isNonEmptyString, isValidEmail, toTrimmedString } from '../utils/validation.js'

type LeadTopic =
  | 'data-enablement'
  | 'analytics'
  | 'transformation'
  | 'ai-enablement'
  | 'governance'
  | 'other'

type CreateLeadRequest = {
  fullName?: unknown
  workEmail?: unknown
  company?: unknown
  role?: unknown
  topic?: unknown
  message?: unknown
  consent?: unknown
  website?: unknown
  source?: unknown
}

const router = Router()

router.post('/', async (req: Request, res: Response) => {
  const ip = getClientIp(req)
  const rateKey = `leads:${ip}`
  if (isRateLimited(rateKey, 8, 10 * 60 * 1000)) {
    res.status(429).json({ success: false, error: 'Too many requests. Please try again later.' })
    return
  }

  const body = (req.body ?? {}) as CreateLeadRequest
  const fullName = toTrimmedString(body.fullName)
  const workEmail = toTrimmedString(body.workEmail)
  const company = toTrimmedString(body.company)
  const role = toTrimmedString(body.role)
  const topic = toTrimmedString(body.topic) as LeadTopic
  const message = toTrimmedString(body.message)
  const consent = body.consent
  const website = toTrimmedString(body.website)
  const source = toTrimmedString(body.source)

  if (website) {
    res.status(400).json({ success: false, error: 'Invalid submission.' })
    return
  }

  if (!isNonEmptyString(fullName)) {
    res.status(400).json({ success: false, error: 'Full name is required.' })
    return
  }
  if (!isNonEmptyString(workEmail) || !isValidEmail(workEmail)) {
    res.status(400).json({ success: false, error: 'A valid work email is required.' })
    return
  }
  if (!isNonEmptyString(company)) {
    res.status(400).json({ success: false, error: 'Company is required.' })
    return
  }
  if (!isNonEmptyString(message)) {
    res.status(400).json({ success: false, error: 'Message is required.' })
    return
  }
  if (!isBoolean(consent) || consent !== true) {
    res.status(400).json({ success: false, error: 'Consent is required.' })
    return
  }

  const id = crypto.randomUUID()
  const receivedAt = new Date().toISOString()
  const ua = typeof req.headers['user-agent'] === 'string' ? req.headers['user-agent'] : ''

  await appendJsonLine('leads.jsonl', {
    id,
    receivedAt,
    fullName,
    workEmail,
    company,
    role: role || undefined,
    topic: topic || 'other',
    message,
    source: source || undefined,
    ipHash: sha256Hex(ip),
    userAgent: ua || undefined,
  })

  res.status(200).json({ success: true, data: { id, receivedAt } })
})

export default router


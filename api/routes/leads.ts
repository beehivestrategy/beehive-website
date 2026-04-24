import { Router, type Request, type Response } from 'express'
import crypto from 'crypto'
import { appendJsonLine } from '../storage.js'
import { getClientIp, isRateLimited } from '../utils/rateLimit.js'
import { sha256Hex } from '../utils/hash.js'
import { isBoolean, isNonEmptyString, isValidEmail, toTrimmedString } from '../utils/validation.js'
import nodemailer from 'nodemailer'

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
const transporter = process.env.GMAIL_USER && process.env.GMAIL_APP_PASSWORD
  ? nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD,
      },
    })
  : null;

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

  try {
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
  } catch (e) {
    console.error("Failed to write to leads.jsonl:", e);
  }

  if (transporter) {
    try {
      const emailHtml = `
        <h2>New Lead from Website</h2>
        <p><strong>Name:</strong> ${fullName}</p>
        <p><strong>Email:</strong> ${workEmail}</p>
        <p><strong>Company:</strong> ${company}</p>
        <p><strong>Role:</strong> ${role || 'N/A'}</p>
        <p><strong>Topic:</strong> ${topic}</p>
        <p><strong>Source:</strong> ${source || 'Direct'}</p>
        <hr />
        <h3>Message:</h3>
        <p>${message.replace(/\n/g, '<br/>')}</p>
      `;

      await transporter.sendMail({
        from: `"Beehive Website" <${process.env.GMAIL_USER}>`,
        to: process.env.CONTACT_EMAIL || process.env.GMAIL_USER,
        replyTo: workEmail,
        subject: `New Contact Request: ${fullName} from ${company}`,
        html: emailHtml,
      });
    } catch (e) {
      console.error("Failed to send email via Gmail:", e);
    }
  }

  res.status(200).json({ success: true, data: { id, receivedAt } })
})

export default router


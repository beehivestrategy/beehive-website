/**
 * This is a API server
 */

import express, {
  type Request,
  type Response,
} from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import authRoutes from './routes/auth.js'
import leadsRoutes from './routes/leads.js'
import newsletterRoutes from './routes/newsletter.js'

// load env
dotenv.config()

const app: express.Application = express()

const allowList = (process.env.CORS_ORIGIN ?? '')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean)

app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin) {
        callback(null, true)
        return
      }
      if (allowList.length === 0) {
        callback(null, origin.startsWith('http://localhost:'))
        return
      }
      callback(null, allowList.includes(origin))
    },
  }),
)
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

/**
 * API Routes
 */
app.use('/api/auth', authRoutes)
app.use('/api/leads', leadsRoutes)
app.use('/api/newsletter', newsletterRoutes)

/**
 * health
 */
app.use(
  '/api/health',
  (req: Request, res: Response): void => {
    res.status(200).json({
      success: true,
      message: 'ok',
    })
  },
)

/**
 * error handler middleware
 */
app.use((error: Error, req: Request, res: Response, _next: unknown) => {
  res.status(500).json({
    success: false,
    error: 'Server internal error',
  })
})

/**
 * 404 handler
 */
app.use((req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    error: 'API not found',
  })
})

export default app

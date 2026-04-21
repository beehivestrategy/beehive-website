import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'
import { services } from '../src/content/services'
import { industries } from '../src/content/industries'
import { caseStudies } from '../src/content/caseStudies'
import { insights } from '../src/content/insights'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const rootDir = path.join(__dirname, '..')
const publicDir = path.join(rootDir, 'public')

function getSiteUrl() {
  const fromEnv = process.env.SITE_URL ?? process.env.VITE_SITE_URL ?? ''
  const trimmed = fromEnv.trim()
  if (!trimmed) return 'https://example.com'
  return trimmed.replace(/\/$/, '')
}

function toUrlEntry(siteUrl: string, route: string) {
  const loc = `${siteUrl}${route}`
  return `  <url><loc>${loc}</loc></url>`
}

async function main() {
  const siteUrl = getSiteUrl()

  const routes = [
    '/',
    '/services',
    ...services.map((s) => `/services/${s.slug}`),
    '/industries',
    ...industries.map((i) => `/industries/${i.slug}`),
    '/case-studies',
    ...caseStudies.map((c) => `/case-studies/${c.slug}`),
    '/insights',
    ...insights.map((p) => `/insights/${p.slug}`),
    '/about',
    '/contact',
    '/privacy',
    '/accessibility',
  ]

  const xml =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    routes.map((r) => toUrlEntry(siteUrl, r)).join('\n') +
    `\n</urlset>\n`

  const robots = `User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`

  await fs.mkdir(publicDir, { recursive: true })
  await fs.writeFile(path.join(publicDir, 'sitemap.xml'), xml, 'utf8')
  await fs.writeFile(path.join(publicDir, 'robots.txt'), robots, 'utf8')
}

main()


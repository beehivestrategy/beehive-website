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
  if (!trimmed) return 'https://www.beehivestrategy.com'
  return trimmed.replace(/\/$/, '')
}

function toUrlEntry(siteUrl: string, route: string, lastmod?: string) {
  const loc = `${siteUrl}${route}`
  const lastmodTag = lastmod ? `\n    <lastmod>${lastmod}</lastmod>` : ''
  return `  <url>\n    <loc>${loc}</loc>${lastmodTag}\n  </url>`
}

async function main() {
  const siteUrl = getSiteUrl()

  // Generate dynamic routes with lastmod if available
  const serviceRoutes = services.map((s) => ({ route: `/services/${s.slug}` }))
  const industryRoutes = industries.map((i) => ({ route: `/industries/${i.slug}` }))
  const caseStudyRoutes = caseStudies.map((c) => ({ route: `/case-studies/${c.slug}` }))
  
  // Use publishedAt for insights if available
  const insightRoutes = insights.map((p) => {
    let lastmod: string | undefined;
    if (p.publishedAt) {
      try {
        // Format to YYYY-MM-DD if valid date
        lastmod = new Date(p.publishedAt).toISOString().split('T')[0]
      } catch (e) {
        // ignore invalid dates
      }
    }
    return { route: `/insights/${p.slug}`, lastmod }
  })

  const staticRoutes = [
    '/',
    '/services',
    '/industries',
    '/case-studies',
    '/insights',
    '/about',
    '/contact',
    '/privacy',
    '/accessibility',
  ].map(route => ({ route }))

  const allRoutes = [
    ...staticRoutes,
    ...serviceRoutes,
    ...industryRoutes,
    ...caseStudyRoutes,
    ...insightRoutes,
  ]

  const xml =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    allRoutes.map((r) => toUrlEntry(siteUrl, r.route, r.lastmod)).join('\n') +
    `\n</urlset>\n`

  const robots = `User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`

  await fs.mkdir(publicDir, { recursive: true })
  await fs.writeFile(path.join(publicDir, 'sitemap.xml'), xml, 'utf8')
  await fs.writeFile(path.join(publicDir, 'robots.txt'), robots, 'utf8')
}

main()

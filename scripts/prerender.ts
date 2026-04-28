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
const distDir = path.join(rootDir, 'dist')

function getSiteUrl() {
  return 'https://www.beehivestrategy.com'
}

const defaultTitle = "Beehive Strategy | Data, Analytics & AI Transformation"
const defaultDesc = "Data enablement, analytics, transformation, and AI enablement consulting. Build trusted data foundations, accelerate insight delivery, and operationalize AI with governance."
const defaultImage = "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=editorial%20corporate%20hero%20image%2C%20abstract%20data%20lattice%20lines%20and%20nodes%20on%20a%20near-black%20background%2C%20subtle%20grain%20texture%2C%20teal%20and%20signal-orange%20accent%20glow%2C%20high-end%20technology%20consulting%20aesthetic%2C%20clean%20negative%20space%2C%20no%20text%2C%20photoreal%20lighting%2C%20ultra%20detailed%2C%20sharp%20focus&image_size=landscape_16_9"

async function main() {
  const indexHtmlPath = path.join(distDir, 'index.html')
  let template = ''
  try {
    template = await fs.readFile(indexHtmlPath, 'utf8')
  } catch (e) {
    console.error('Could not find dist/index.html. Did you build the project?')
    process.exit(1)
  }

  const siteUrl = getSiteUrl()

  const routes: Array<{ route: string, title: string, desc: string, type?: string, publishedAt?: string }> = [
    { route: '/', title: defaultTitle, desc: defaultDesc },
    { route: '/services', title: `Services | ${defaultTitle}`, desc: "Explore our data, analytics, and AI services." },
    { route: '/industries', title: `Industries | ${defaultTitle}`, desc: "Industry-specific data and AI solutions." },
    { route: '/case-studies', title: `Case Studies | ${defaultTitle}`, desc: "Real-world data and AI transformation stories." },
    { route: '/insights', title: `Insights | ${defaultTitle}`, desc: "Latest thinking on data, analytics, and AI." },
    { route: '/about', title: `About | ${defaultTitle}`, desc: "About Beehive Strategy." },
    { route: '/contact', title: `Contact | ${defaultTitle}`, desc: "Get in touch with our experts." },
    { route: '/privacy', title: `Privacy Policy | ${defaultTitle}`, desc: "Our privacy policy." },
    { route: '/accessibility', title: `Accessibility | ${defaultTitle}`, desc: "Our accessibility statement." },
  ]

  services.forEach(s => routes.push({ route: `/services/${s.slug}`, title: `${s.title} | ${defaultTitle}`, desc: s.summary }))
  industries.forEach(i => routes.push({ route: `/industries/${i.slug}`, title: `${i.title} | ${defaultTitle}`, desc: i.summary }))
  caseStudies.forEach(c => routes.push({ route: `/case-studies/${c.slug}`, title: `${c.title} | ${defaultTitle}`, desc: c.summary }))
  insights.forEach(p => routes.push({ route: `/insights/${p.slug}`, title: `${p.title} | ${defaultTitle}`, desc: p.summary, type: 'article', publishedAt: p.publishedAt }))

  for (const { route, title, desc, type, publishedAt } of routes) {
    let html = template
    
    // Replace title
    html = html.replace(/<title>.*?<\/title>/, `<title>${title}</title>`)
    
    // Replace meta tags roughly
    html = html.replace(/<meta\s+name="description"\s+content=".*?"\s*\/>/s, `<meta name="description" content="${desc}" />`)
    html = html.replace(/<meta\s+property="og:title"\s+content=".*?"\s*\/>/s, `<meta property="og:title" content="${title}" />`)
    html = html.replace(/<meta\s+property="og:description"\s+content=".*?"\s*\/>/s, `<meta property="og:description" content="${desc}" />`)
    
    // Insert Canonical URL
    const canonical = `${siteUrl}${route}`
    html = html.replace('</head>', `  <link rel="canonical" href="${canonical}" />\n  <meta property="og:url" content="${canonical}" />\n  </head>`)

    // Insert Article tags if it's an insight
    if (type === 'article') {
      html = html.replace(/<meta\s+property="og:type"\s+content="website"\s*\/>/s, `<meta property="og:type" content="article" />`)
      if (publishedAt) {
        html = html.replace('</head>', `  <meta property="article:published_time" content="${publishedAt}" />\n  </head>`)
      }
    }

    // Determine output path
    let outPath = ''
    if (route === '/') {
      outPath = path.join(distDir, 'index.html')
    } else {
      outPath = path.join(distDir, route, 'index.html')
      await fs.mkdir(path.join(distDir, route), { recursive: true })
    }

    await fs.writeFile(outPath, html, 'utf8')
    console.log(`Prerendered: ${route}`)
  }
}

main()

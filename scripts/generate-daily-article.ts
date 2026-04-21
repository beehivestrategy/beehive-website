import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Replace with your actual API Key or pass it via environment variable in your CI/CD
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;

if (!OPENROUTER_API_KEY) {
  console.error('Missing OPENROUTER_API_KEY environment variable. Exiting.');
  process.exit(1);
}

const currentDate = new Date().toISOString().split('T')[0];

const prompt = `
You are a top-tier enterprise Data & AI consultant. Write a highly professional, compelling, and actionable insight article for the "Beehive Data & AI Consulting" blog.
The article should be about modern data foundations, AI operationalization, metric governance, or data transformation.

Generate the article structure in pure JSON format (NO markdown blocks, NO backticks) matching this interface exactly:

{
  "slug": "kebab-case-title-of-the-article",
  "title": "Article Title",
  "summary": "A 2-sentence executive summary of the article.",
  "readingMinutes": 5,
  "topics": ["data enablement", "ai enablement", "strategy"],
  "sections": [
    {
      "heading": "Section 1 Heading",
      "paragraphs": ["Paragraph 1...", "Paragraph 2..."]
    }
  ],
  "faqs": [
    {
      "question": "Relevant FAQ Question?",
      "answer": "Clear, professional answer."
    }
  ]
}

Ensure there are at least 3 detailed sections and 2 FAQs. The tone must be authoritative, objective, and aimed at enterprise leaders.
Return ONLY valid JSON.
`;

async function generateContent() {
  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
      'HTTP-Referer': 'https://beehive.consulting', // Replace with your actual site URL
      'X-Title': 'Beehive Data & AI Consulting', // Replace with your actual site name
    },
    body: JSON.stringify({
      model: 'anthropic/claude-3.5-sonnet', // or your preferred OpenRouter model
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7,
    }),
  });

  if (!response.ok) {
    throw new Error(`OpenRouter API Error: ${response.statusText}`);
  }

  const data = await response.json();
  let content = data.choices[0].message.content.trim();
  
  if (content.startsWith('\`\`\`json')) {
    content = content.replace(/^\`\`\`json\n?/, '').replace(/\n?\`\`\`$/, '');
  } else if (content.startsWith('\`\`\`')) {
    content = content.replace(/^\`\`\`\n?/, '').replace(/\n?\`\`\`$/, '');
  }

  return JSON.parse(content);
}

async function translateContent(articleJson: any, targetLang: string) {
  const translatePrompt = `
You are an expert technical translator. Translate the following JSON article object into ${targetLang}.
Maintain the EXACT JSON structure, keys, and formatting. ONLY translate the string values for "title", "summary", "topics", "heading", "paragraphs", "question", and "answer". Do NOT translate the "slug" or "readingMinutes".

Article JSON:
${JSON.stringify(articleJson, null, 2)}

Return ONLY valid JSON without markdown formatting.
`;

  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
      'HTTP-Referer': 'https://beehive.consulting',
      'X-Title': 'Beehive Data & AI Consulting',
    },
    body: JSON.stringify({
      model: 'anthropic/claude-3.5-sonnet',
      messages: [{ role: 'user', content: translatePrompt }],
      temperature: 0.3,
    }),
  });

  if (!response.ok) {
    throw new Error(`OpenRouter Translation Error: ${response.statusText}`);
  }

  const data = await response.json();
  let content = data.choices[0].message.content.trim();
  
  if (content.startsWith('\`\`\`json')) {
    content = content.replace(/^\`\`\`json\n?/, '').replace(/\n?\`\`\`$/, '');
  } else if (content.startsWith('\`\`\`')) {
    content = content.replace(/^\`\`\`\n?/, '').replace(/\n?\`\`\`$/, '');
  }

  return JSON.parse(content);
}

async function run() {
  try {
    console.log('Generating English article...');
    const enArticle = await generateContent();
    
    console.log(`Generated article: ${enArticle.title}`);
    enArticle.publishedAt = currentDate;

    console.log('Translating to Simplified Chinese (zh-CN)...');
    const zhCnArticle = await translateContent(enArticle, 'Simplified Chinese (zh-CN)');

    console.log('Translating to Traditional Chinese (zh-TW)...');
    const zhTwArticle = await translateContent(enArticle, 'Traditional Chinese (zh-TW)');

    // 1. Update src/content/insights.ts
    const insightsPath = path.resolve(__dirname, '../src/content/insights.ts');
    let insightsFile = fs.readFileSync(insightsPath, 'utf8');
    
    const newInsightSkeleton = `  {
    slug: "${enArticle.slug}",
    title: "${enArticle.title.replace(/"/g, '\\"')}",
    summary: "${enArticle.summary.replace(/"/g, '\\"')}",
    publishedAt: "${currentDate}",
    readingMinutes: ${enArticle.readingMinutes},
    topics: ${JSON.stringify(enArticle.topics)},
    sections: [],
    faqs: []
  },`;

    insightsFile = insightsFile.replace('export const insights: Insight[] = [', 'export const insights: Insight[] = [\n' + newInsightSkeleton);
    fs.writeFileSync(insightsPath, insightsFile);

    // 2. Update Locales
    const updateLocale = (localeName: string, translatedData: any) => {
      const localePath = path.resolve(__dirname, '../src/locales/' + localeName + '.json');
      const localeObj = JSON.parse(fs.readFileSync(localePath, 'utf8'));
      
      localeObj.insights = localeObj.insights || {};
      localeObj.insights[translatedData.slug] = {
        title: translatedData.title,
        summary: translatedData.summary,
        topics: translatedData.topics,
        sections: translatedData.sections,
        faqs: translatedData.faqs
      };

      fs.writeFileSync(localePath, JSON.stringify(localeObj, null, 2));
    };

    updateLocale('en', enArticle);
    updateLocale('zh-CN', zhCnArticle);
    updateLocale('zh-TW', zhTwArticle);

    console.log('Successfully generated and injected daily article!');

  } catch (error) {
    console.error('Error generating daily article:', error);
    process.exit(1);
  }
}

run();

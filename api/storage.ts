import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const dataDir = path.join(__dirname, 'data')

type JsonValue = Record<string, unknown>

let queue: Promise<void> = Promise.resolve()

async function ensureDataDir() {
  await fs.mkdir(dataDir, { recursive: true })
}

export function getDataDirPath() {
  return dataDir
}

export async function appendJsonLine(filename: string, obj: JsonValue) {
  const line = `${JSON.stringify(obj)}\n`
  queue = queue.then(async () => {
    await ensureDataDir()
    const filePath = path.join(dataDir, filename)
    await fs.appendFile(filePath, line, 'utf8')
  })
  return queue
}


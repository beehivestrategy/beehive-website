export async function run(_sql: string, _params: readonly unknown[] = []): Promise<void> {
  throw new Error('Database adapter not configured')
}

export async function get<T>(_sql: string, _params: readonly unknown[] = []): Promise<T | undefined> {
  throw new Error('Database adapter not configured')
}

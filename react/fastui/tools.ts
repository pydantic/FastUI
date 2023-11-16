interface Request {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  // defaults to 200
  expectedStatus?: number[]
  body?: Record<string, any>
  headers?: Record<string, string>
}

class RequestError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
    this.name = 'RequestError'
  }
}

export async function request({ url, method, headers, body, expectedStatus }: Request): Promise<any> {
  const init: RequestInit = {}
  if (method) {
    init.method = method
  }

  if (body) {
    init.body = JSON.stringify(body)
    headers = headers ?? {}
    headers['Content-Type'] = 'application/json'
  }

  if (headers) {
    init.headers = headers
  }

  let response
  try {
    response = await fetch(url, init)
  } catch (e) {
    throw new RequestError('fetch failed', 0)
  }

  const { status } = response
  if (!responseOk(response, expectedStatus)) {
    let detail: null | string = null
    const content = await response.text()
    try {
      const jsonData = JSON.parse(content)
      console.warn(`${url} -> ${status} JSON:`, jsonData)
      if (typeof jsonData.detail === 'string') {
        detail = jsonData.detail
      }
    } catch (e) {
      console.warn(`${url} -> ${status} content:`, content)
      detail = content
    }
    const msg = `${detail || response.statusText} (${status})`
    throw new RequestError(msg, status)
  }

  let data
  try {
    data = await response.json()
  } catch (e) {
    console.warn(`${url} -> ${status} response not valid JSON`)
    throw new RequestError('Response not valid JSON', status)
  }
  console.debug(`${url} -> ${status} JSON:`, data)
  return data
}

function responseOk(response: Response, expectedStatus?: number[]) {
  if (expectedStatus) {
    return expectedStatus.includes(response.status)
  } else {
    return response.ok
  }
}

export function unreachable(msg: string, unexpectedValue: never, args?: any) {
  console.warn(msg, { unexpectedValue }, args)
}

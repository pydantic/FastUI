interface Request {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  // defaults to 200
  expectedStatus?: number[]
  json?: Record<string, any>
  formData?: FormData
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

export async function request({
  url,
  method,
  headers,
  json,
  expectedStatus,
  formData,
}: Request): Promise<[number, any]> {
  const init: RequestInit = {}

  let contentType = null
  if (json) {
    init.body = JSON.stringify(json)
    contentType = 'application/json'
    method = method ?? 'POST'
  } else if (formData) {
    // don't set content-type, let the browser set it
    init.body = formData
    method = method ?? 'POST'
  }

  headers = headers ?? {}
  if (contentType && !headers['Content-Type']) {
    headers['Content-Type'] = contentType
  }

  if (method) {
    init.method = method
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
  return [status, data]
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

export enum DisplayChoices {
  auto = 'auto',
  plain = 'plain',
  datetime = 'datetime',
  date = 'date',
  duration = 'duration',
  as_title = 'as_title',
  markdown = 'markdown',
  json = 'json',
  inline_code = 'inline_code',
}

// usage as_title('what_ever') > 'What Ever'
export const asTitle = (s: string): string => s.replace(/[_-]/g, ' ').replace(/(_|\b)\w/g, (l) => l.toUpperCase())

module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'standard',
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs', 'demo/vite.config.ts'],
  parser: '@typescript-eslint/parser',
  plugins: ['react', '@typescript-eslint', 'react-refresh', 'simple-import-sort'],
  rules: {
    'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    '@typescript-eslint/no-explicit-any': 'off',
    'no-use-before-define': 'off',
    'import/order': [
      'error',
      {
        'newlines-between': 'always',
        groups: ['builtin', 'external', 'internal', 'object', 'type', 'parent', 'index', 'sibling'],
        pathGroups: [
          {
            pattern: '@/**',
            group: 'internal',
          },
          {
            pattern: './../**',
            group: 'parent',
          },
        ],
      },
    ],
  },
}

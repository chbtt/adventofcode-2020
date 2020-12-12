module.exports = {
  env: {
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'eslint-config-semistandard'
  ],
  parserOptions: { ecmaVersion: 12 },
  rules: {
    'no-console': 'off',
    // space before and after curly braces
    'object-curly-spacing': [
      'error',
      'always'
    ],
    // space before and after array brackets
    'array-bracket-spacing': [
      'error',
      'always'
    ],
    // individual lines for array elements if more than one
    'array-bracket-newline': [
      'error',
      { minItems: 2 }
    ],
    'array-element-newline': [
      'error',
      { minItems: 2 }
    ],
    // individual lines for object properties if more than one
    'object-curly-newline': [
      'error',
      { minProperties: 2 }
    ],
    'object-property-newline': [
      'error',
      { allowAllPropertiesOnSameLine: false }
    ],
    // blank line before return
    'padding-line-between-statements': [
      'error',
      {
        blankLine: 'always',
        prev: '*',
        next: 'return'
      }
    ],
    // newline at end of file
    'eol-last': [
      'error',
      'always'
    ]
  }
};

/**
 * Unit tests for validation utilities
 */

describe('Email Validation', () => {
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  it('should validate correct email formats', () => {
    expect(validateEmail('user@example.com')).toBe(true)
    expect(validateEmail('test.user@domain.co.uk')).toBe(true)
    expect(validateEmail('name+tag@company.com')).toBe(true)
  })

  it('should reject invalid email formats', () => {
    expect(validateEmail('invalid')).toBe(false)
    expect(validateEmail('user@')).toBe(false)
    expect(validateEmail('@domain.com')).toBe(false)
    expect(validateEmail('user @domain.com')).toBe(false)
  })
})

describe('Password Validation', () => {
  const validatePassword = (password: string): boolean => {
    return password.length >= 6
  }

  it('should accept passwords with minimum length', () => {
    expect(validatePassword('123456')).toBe(true)
    expect(validatePassword('password123')).toBe(true)
  })

  it('should reject passwords below minimum length', () => {
    expect(validatePassword('12345')).toBe(false)
    expect(validatePassword('abc')).toBe(false)
    expect(validatePassword('')).toBe(false)
  })
})

describe('Date Validation', () => {
  const isValidDate = (dateString: string): boolean => {
    const date = new Date(dateString)
    return date instanceof Date && !isNaN(date.getTime())
  }

  it('should validate correct date formats', () => {
    expect(isValidDate('2024-01-01')).toBe(true)
    expect(isValidDate('2023-12-31')).toBe(true)
  })

  it('should reject invalid dates', () => {
    expect(isValidDate('invalid-date')).toBe(false)
    expect(isValidDate('2024-13-01')).toBe(false)
  })
})

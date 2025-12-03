/**
 * Unit tests for auth server actions
 */

// Mock next/headers and next/navigation
jest.mock('next/headers', () => ({
  cookies: jest.fn(() => ({
    set: jest.fn(),
    delete: jest.fn(),
  })),
}))

jest.mock('next/navigation', () => ({
  redirect: jest.fn((url: string) => {
    throw { digest: 'NEXT_REDIRECT', url }
  }),
}))

// Mock fetch globally
global.fetch = jest.fn()

import { login, register } from '@/app/actions/auth'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

describe('Auth Actions', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(global.fetch as jest.Mock).mockClear()
  })

  describe('login', () => {
    it('should successfully login with valid credentials', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          access_token: 'test-token',
          token_type: 'bearer'
        }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const formData = new FormData()
      formData.append('email', 'test@example.com')
      formData.append('password', 'password123')

      await expect(login(undefined, formData)).rejects.toMatchObject({
        digest: 'NEXT_REDIRECT',
        url: '/dashboard'
      })

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/login'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        })
      )
    })

    it('should return error for invalid credentials', async () => {
      const mockResponse = {
        ok: false,
        json: async () => ({
          detail: 'Invalid credentials'
        }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const formData = new FormData()
      formData.append('email', 'test@example.com')
      formData.append('password', 'wrongpassword')

      const result = await login(undefined, formData)

      expect(result).toEqual({ error: 'Invalid credentials' })
    })

    it('should handle network errors', async () => {
      ;(global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

      const formData = new FormData()
      formData.append('email', 'test@example.com')
      formData.append('password', 'password123')

      const result = await login(undefined, formData)

      expect(result).toEqual({ error: 'An unexpected error occurred' })
    })
  })

  describe('register', () => {
    it('should successfully register and auto-login', async () => {
      // Mock registration response
      const registerResponse = {
        ok: true,
        json: async () => ({
          id: '123',
          email: 'newuser@example.com'
        }),
      }

      // Mock login response
      const loginResponse = {
        ok: true,
        json: async () => ({
          access_token: 'test-token',
          token_type: 'bearer'
        }),
      }

      ;(global.fetch as jest.Mock)
        .mockResolvedValueOnce(registerResponse)
        .mockResolvedValueOnce(loginResponse)

      const formData = new FormData()
      formData.append('email', 'newuser@example.com')
      formData.append('password', 'password123')
      formData.append('full_name', 'New User')

      await expect(register(undefined, formData)).rejects.toMatchObject({
        digest: 'NEXT_REDIRECT',
        url: '/dashboard'
      })

      expect(global.fetch).toHaveBeenCalledTimes(2)
    })

    it('should return error for duplicate email', async () => {
      const mockResponse = {
        ok: false,
        json: async () => ({
          detail: 'Email already registered'
        }),
      }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse)

      const formData = new FormData()
      formData.append('email', 'existing@example.com')
      formData.append('password', 'password123')
      formData.append('full_name', 'Existing User')

      const result = await register(undefined, formData)

      expect(result).toEqual({ error: 'Email already registered' })
    })

    it('should handle registration errors', async () => {
      ;(global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Server error'))

      const formData = new FormData()
      formData.append('email', 'test@example.com')
      formData.append('password', 'password123')
      formData.append('full_name', 'Test User')

      const result = await register(undefined, formData)

      expect(result).toEqual({ error: 'An unexpected error occurred' })
    })
  })
})

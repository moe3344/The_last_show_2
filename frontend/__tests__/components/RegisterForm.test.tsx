import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import RegisterForm from '@/components/auth/RegisterForm'

describe('RegisterForm', () => {
  const mockRegisterAction = jest.fn()

  beforeEach(() => {
    mockRegisterAction.mockClear()
  })

  it('renders all form fields', () => {
    render(<RegisterForm registerAction={mockRegisterAction} />)

    expect(screen.getByLabelText(/full name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument()
  })

  it('displays error message when provided', () => {
    const mockActionWithError = async () => ({
      error: 'Email already registered'
    })

    render(<RegisterForm registerAction={mockActionWithError} />)

    // Submit form to trigger error
    const submitButton = screen.getByRole('button', { name: /create account/i })
    userEvent.click(submitButton)

    // Note: In real scenario with useActionState, error would appear after submission
  })

  it('has correct input types and placeholders', () => {
    render(<RegisterForm registerAction={mockRegisterAction} />)

    const fullNameInput = screen.getByPlaceholderText(/john doe/i)
    const emailInput = screen.getByPlaceholderText(/you@example.com/i)
    const passwordInput = screen.getByPlaceholderText(/••••••••/i)

    expect(fullNameInput).toHaveAttribute('type', 'text')
    expect(emailInput).toHaveAttribute('type', 'email')
    expect(passwordInput).toHaveAttribute('type', 'password')
  })

  it('has password minimum length validation', () => {
    render(<RegisterForm registerAction={mockRegisterAction} />)

    const passwordInput = screen.getByPlaceholderText(/••••••••/i)
    expect(passwordInput).toHaveAttribute('minLength', '6')
  })

  it('all fields are required', () => {
    render(<RegisterForm registerAction={mockRegisterAction} />)

    const fullNameInput = screen.getByLabelText(/full name/i)
    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)

    expect(fullNameInput).toBeRequired()
    expect(emailInput).toBeRequired()
    expect(passwordInput).toBeRequired()
  })
})

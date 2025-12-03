import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import LoginForm from '@/components/auth/LoginForm'

describe('LoginForm', () => {
  const mockLoginAction = jest.fn()

  beforeEach(() => {
    mockLoginAction.mockClear()
  })

  it('renders email and password fields', () => {
    render(<LoginForm loginAction={mockLoginAction} />)

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
  })

  it('has correct input types', () => {
    render(<LoginForm loginAction={mockLoginAction} />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)

    expect(emailInput).toHaveAttribute('type', 'email')
    expect(passwordInput).toHaveAttribute('type', 'password')
  })

  it('displays error message when provided', () => {
    const mockActionWithError = async () => ({
      error: 'Invalid credentials'
    })

    render(<LoginForm loginAction={mockActionWithError} />)

    const submitButton = screen.getByRole('button', { name: /sign in/i })
    userEvent.click(submitButton)
  })

  it('both fields are required', () => {
    render(<LoginForm loginAction={mockLoginAction} />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)

    expect(emailInput).toBeRequired()
    expect(passwordInput).toBeRequired()
  })

  it('has correct placeholders', () => {
    render(<LoginForm loginAction={mockLoginAction} />)

    expect(screen.getByPlaceholderText(/you@example.com/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/••••••••/i)).toBeInTheDocument()
  })
})

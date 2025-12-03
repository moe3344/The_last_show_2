# Testing Guide

This document describes the testing setup and how to run tests for both backend and frontend.

## Backend Tests

### Setup

1. Install test dependencies:
```bash
cd backend
pip install -r requirements-dev.txt
```

### Running Tests

Run all tests:
```bash
cd backend
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_auth_service.py
```

Run with verbose output:
```bash
pytest -v
```

### Test Structure

- `tests/conftest.py` - Shared fixtures and test configuration
- `tests/test_auth_service.py` - Authentication service unit tests
- `tests/test_user_service.py` - User service unit tests
- `tests/test_auth_routes.py` - Authentication API integration tests
- `tests/test_obituary_service.py` - Obituary service unit tests
- `tests/test_api_health.py` - Health check endpoint tests

### Test Coverage

The project aims for 70%+ test coverage. View the coverage report after running tests:

```bash
# Terminal report
pytest --cov=app --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Frontend Tests

### Setup

1. Install test dependencies:
```bash
cd frontend
npm install
```

### Running Tests

Run all tests:
```bash
cd frontend
npm test
```

Run tests with coverage:
```bash
npm run test:coverage
```

Run tests in watch mode:
```bash
npm run test:watch
```

### Test Structure

- `__tests__/components/` - Component unit tests
  - `RegisterForm.test.tsx` - Registration form component tests
  - `LoginForm.test.tsx` - Login form component tests
  - `Button.test.tsx` - Button component tests
- `__tests__/actions/` - Server action tests
  - `auth.test.ts` - Authentication action tests
- `__tests__/utils/` - Utility function tests
  - `validation.test.ts` - Validation function tests

### Test Configuration

- `jest.config.ts` - Jest configuration
- `jest.setup.ts` - Test environment setup and global mocks

## Continuous Integration

### GitHub Actions Workflows

Tests run automatically on pull requests and pushes to main/master/develop branches.

#### Backend CI (`.github/workflows/backend-tests.yml`)
- Runs on Python 3.11 and 3.12
- Executes all pytest tests
- Generates coverage reports
- Runs linting with Ruff
- Coverage threshold: 70%

#### Frontend CI (`.github/workflows/frontend-tests.yml`)
- Runs on Node.js 20.x and 22.x
- Executes all Jest tests
- Generates coverage reports
- Runs ESLint linting
- Performs TypeScript type checking
- Validates production build

### Viewing CI Results

1. Navigate to the "Actions" tab in GitHub
2. Click on a workflow run to see detailed results
3. Coverage reports are uploaded to Codecov (if configured)

## Best Practices

### Backend Testing
- Use fixtures from `conftest.py` for database and test client setup
- Mark tests with `@pytest.mark.unit` or `@pytest.mark.integration`
- Test both success and failure scenarios
- Mock external services (AI, Lambda, etc.)
- Test authentication and authorization

### Frontend Testing
- Use React Testing Library for component tests
- Test user interactions, not implementation details
- Mock server actions and API calls
- Test accessibility (labels, roles)
- Test error states and loading states

### Writing New Tests

#### Backend Example
```python
@pytest.mark.unit
def test_new_feature(db, test_user):
    # Arrange
    data = {"key": "value"}

    # Act
    result = my_function(db, data)

    # Assert
    assert result.status == "success"
```

#### Frontend Example
```typescript
it('should handle user interaction', async () => {
  // Arrange
  const handleClick = jest.fn()
  render(<MyComponent onClick={handleClick} />)

  // Act
  await userEvent.click(screen.getByRole('button'))

  // Assert
  expect(handleClick).toHaveBeenCalled()
})
```

## Troubleshooting

### Backend
- **Database errors**: Check that test database is being created/destroyed properly
- **Import errors**: Ensure all dependencies are installed from `requirements-dev.txt`
- **Token errors**: Verify `SECRET_KEY` is set in test environment

### Frontend
- **Module not found**: Run `npm install` to ensure all dependencies are installed
- **Jest config errors**: Check `jest.config.ts` and `jest.setup.ts`
- **Next.js errors**: Ensure Next.js mocks are properly configured in `jest.setup.ts`

## Running Tests Locally Before PR

Before submitting a pull request, run:

### Backend
```bash
cd backend
pytest --cov=app --cov-report=term-missing
ruff check app/ tests/
ruff format --check app/ tests/
```

### Frontend
```bash
cd frontend
npm test -- --coverage --watchAll=false
npm run lint
npx tsc --noEmit
npm run build
```

This ensures your code will pass CI checks.

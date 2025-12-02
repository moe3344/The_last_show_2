// Axios error structure
export interface APIError {
  response?: {
    data?: {
      detail?:
        | string
        | Array<{
            loc: string[];
            msg: string;
            type: string;
          }>;
    };
    status?: number;
  };
  message?: string;
}

// Helper function to extract error message
export function getErrorMessage(error: unknown): string {
  // Handle Axios errors
  if (typeof error === "object" && error !== null && "response" in error) {
    const apiError = error as APIError;
    const detail = apiError.response?.data?.detail;

    // FastAPI validation errors (422)
    if (Array.isArray(detail)) {
      return detail.map((err) => err.msg).join(", ");
    }

    // Simple error message (400, 401, etc.)
    if (typeof detail === "string") {
      return detail;
    }
  }

  // Generic error with message
  if (error instanceof Error) {
    return error.message;
  }

  // Fallback
  return "An unexpected error occurred";
}

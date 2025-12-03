
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_obituary_text(name: str, birth_date: str, death_date: str) -> str:
    """
    Generate obituary text using Groq (free!)
      Args:
          name: Full name of the deceased
          birth_date: Birth date in YYYY-MM-DD format
          death_date: Death date in YYYY-MM-DD format

      Returns:
          Generated obituary text
      """
    prompt = f"""Write a respectful and heartfelt obituary for a fictional character named {name}.

  Details:
  - Born: {birth_date}
  - Passed away: {death_date}

  Write a 1 paragraph obituary that:
  1. Announces their passing with dignity
  2. Mentions a few fictional life achievements or positive characteristics
  3. Includes survived by family members (fictional)
  4. Ends with funeral service details (fictional)

  Keep the tone dignified, compassionate, and touching. Make it feel genuine and respectful."""

    try:
          chat_completion = client.chat.completions.create(
              messages=[
                  {
                      "role": "system",
                      "content": "You are a professional obituary writer. Write respectful, heartfelt, and dignified obituaries that honor the deceased with compassion and care."
                  },
                  {
                      "role": "user",
                      "content": prompt
                  }
              ],
              model="llama-3.3-70b-versatile",  # Best free model
              temperature=0.7,
              max_tokens=600,
          )

          obituary_text = chat_completion.choices[0].message.content.strip()
          return obituary_text

    except Exception as e:
          print(f"Error generating obituary with Groq: {e}")
          # Fallback if Groq API fails
          return f"{name} was born on {birth_date} and passed away on {death_date}. They will be deeply missed by family and friends. A memorial service will be held to celebrate their life and legacy."
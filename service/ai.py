import os
import re
import time
from google import genai

# Automatically uses GEMINI_API_KEY from environment (loaded by dotenv)
client = genai.Client()

def get_gemini_move(board_str: str, valid_columns: list[int], ai_piece: str) -> int:
    """
    Sends the board state to Gemini and returns a valid column (0-indexed).
    valid_columns: list of 0-indexed columns that are not full, e.g. [0, 1, 3, 4]
    """
    human_columns = [c + 1 for c in valid_columns]  # 1-7 for human readability

    prompt = f"""
You are playing Connect 4 as piece '{ai_piece}'.
Current board (1 to 7 are columns):
{board_str}

Available columns you can play in: {human_columns}

Instructions:
1. If you can win immediately in 1 move, play that column!
2. If the opponent can win on their next turn, BLOCK them!
3. Otherwise, pick the best tactical column (prefer the center: column 4, then 3 and 5).

Output ONLY the single digit of the column (one of {human_columns}). Do not write any explanations or other words.
"""
    models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash-lite","gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model= model_name,
                contents=prompt,
            )
            text = response.text.strip()
            # Find any number 1-7 in the response
            match = re.search(r"[1-7]", text)
            if match:
                col_1_based = int(match.group())
                col_0_based = col_1_based - 1
                if col_0_based in valid_columns:
                    return col_0_based
        except Exception as e:
            # If 503 or 404, log and immediately try the next model
            print(f"[AI] {model_name} failed ({type(e).__name__}): {e}. Trying next...")
            time.sleep(0.5)

    # Fallback: if API fails or picks a full column, pick center or first valid column
    if 3 in valid_columns:
        return 3
    return valid_columns[0]
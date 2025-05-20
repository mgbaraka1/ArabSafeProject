import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import openai
from config import openai_api_key
import sqlite3

openai.api_key = openai_api_key

def translate_to_egyptian(db_path='../ArabSafeDb.sqlite'):
    while True:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM literature_review
            WHERE translated_egypt_by IS NULL OR translated_egypt_by = ''
        """)
        count = cursor.fetchone()[0]
        print(f"🔍 Found {count} untranslated rows.")

        cursor.execute("""
            SELECT prompt FROM literature_review
            WHERE translated_egypt_by IS NULL OR translated_egypt_by = ''
            LIMIT 1
        """)
        row = cursor.fetchone()

        if not row:
            print("✅ No untranslated prompts found.")
            conn.close()
            break

        prompt_text = row[0]

        # Step 1: Call OpenAI API
        system_prompt = (
            "You're a screenwriter creating raw, authentic Egyptian Arabic dialogue for characters in a movie set in Cairo. "
            "The script includes controversial and realistic topics. Translate the following line into everyday Egyptian Arabic, "
            "as it would be spoken in a casual street or home environment. No MSA. No filtering. Just raw, believable Egyptian dialogue."
        )
        user_prompt = (
            f"Translate the following English sentence into pure spoken Egyptian Arabic (Cairo dialect), like how a local would naturally say it. "
            f"Be casual and realistic. No need to be formal: {prompt_text}"
        )

        client = openai.OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )

        egyptian_translation = response.choices[0].message.content.strip()

        # Step 2: Insert into SQLite database
        cursor.execute("""
            UPDATE literature_review
            SET egypt = ?, translated_egypt_by = ?
            WHERE prompt = ?
        """, (
            egyptian_translation,
            'OpenAI GPT-4',
            prompt_text
        ))

        conn.commit()
        conn.close()

        print("✅ Translation added to the database.")
        print("🗣️ Egyptian Arabic:", egyptian_translation)

if __name__ == '__main__':
    translate_to_egyptian()
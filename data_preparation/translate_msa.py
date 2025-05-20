import sqlite3
import time
from APIs.deepl import translate_by_deepl

def translate_msa_by_deepl():
    conn = sqlite3.connect("ArabSafeDb.sqlite")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, prompt, language_name
            FROM Literature_Review
            WHERE language_name != 'Arabic' AND (MSA IS NULL OR MSA = '');
        """)
        rows = cursor.fetchall()
        print(f"Found {len(rows)} rows to translate.")

        count = 0
        max_rows = 3000

        for row in rows:
            row_id, prompt, language_name = row
            print(f"Translating Row ID {row_id}: '{prompt}'")

            try:
                translated_text = translate_by_deepl(prompt, target_language="AR")
            except Exception as api_error:
                print(f"Error translating Row ID {row_id}: {api_error}")
                continue

            try:
                cursor.execute("""
                    UPDATE Literature_Review
                    SET MSA = ?, translated_MSA_by = ?
                    WHERE id = ?
                """, (translated_text, 'deepl', row_id))
                conn.commit()  # Commit after each update
                print(f"Row ID {row_id} updated successfully.")
                count += 1

                if count >= max_rows:
                    print(f"Processed {max_rows} rows. Stopping as per limit.")
                    break

            except Exception as db_error:
                print(f"Database error for Row ID {row_id}: {db_error}")
                continue

            time.sleep(0.1)

        print(f"Processed {count} rows successfully. All changes saved.")

    except Exception as e:
        print(f"An error occurred during translation: {e}")

    finally:
        if conn:
            conn.commit()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    translate_msa_by_deepl()
import sqlite3
from datetime import datetime, timezone, timedelta

db_path = "../ArabSafeDb.sqlite"

def update_final_dataset():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Fetch finalized reviewed records from Literature_Review
            cursor.execute("""
                SELECT id, prompt, MSA, egypt_reviewed, saudi_reviewed
                FROM literature_review
                WHERE is_final = 1
                AND is_reviewed = 'true'
                AND taken != 1
            """)
            records = cursor.fetchall()

            for record in records:
                translation_id, original_prompt, msa_prompt, egypt_prompt, saudi_prompt = record

                # Check if the translation_id exists in final_dataset
                cursor.execute("SELECT id FROM final_dataset WHERE translation_id = ?", (translation_id,))
                exists = cursor.fetchone()

                if not exists:
                    try:
                        # Get current Riyadh time (+3 GMT)
                        riyadh_time = datetime.now(timezone.utc) + timedelta(hours=3)
                        formatted_time = riyadh_time.strftime('%Y-%m-%d %H:%M:%S')

                        # Insert new record into final_dataset
                        cursor.execute("""
                            INSERT INTO final_dataset 
                            (translation_id, original_prompt, msa_prompt, egypt_prompt, saudi_prompt, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (translation_id, original_prompt, msa_prompt, egypt_prompt, saudi_prompt, formatted_time))

                        print(f"Inserted translation_id {translation_id} into final_dataset.")

                    except Exception as e:
                        print(f"Error inserting translation_id {translation_id}: {e}")

            conn.commit()
            print("Update process completed successfully.")

    except Exception as e:
        print(f"Database connection error: {e}")

# Run the function
if __name__ == "__main__":
    update_final_dataset()
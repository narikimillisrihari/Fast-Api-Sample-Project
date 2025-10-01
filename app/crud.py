from app.database import get_connection

def create_or_update_quote(quote):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if quote exists
    cursor.execute("SELECT id FROM quotes WHERE url = ?", (quote.url,))
    row = cursor.fetchone()

    if row:
        # Update existing
        cursor.execute("""
            UPDATE quotes
            SET text = ?, author = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
            WHERE url = ?
        """, (quote.text, quote.author, ",".join(quote.tags), quote.url))
        conn.commit()
        conn.close()
        return row["id"], "updated"
    else:
        # Insert new
        cursor.execute("""
            INSERT INTO quotes (url, text, author, tags)
            VALUES (?, ?, ?, ?)
        """, (quote.url, quote.text, quote.author, ",".join(quote.tags)))
        conn.commit()
        quote_id = cursor.lastrowid
        conn.close()
        return quote_id, "created"

def get_quotes(skip=0, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_quote(quote_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

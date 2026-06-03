from config.database import get_db_connection


def create_business_profile(nombre_negocio: str, rubro: str, ciudad: str) -> int:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO business_profiles (
            nombre_negocio,
            rubro,
            ciudad
        )
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (
            nombre_negocio,
            rubro,
            ciudad,
        )
    )

    profile_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return profile_id


def get_business_profiles() -> list[dict]:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, nombre_negocio, rubro, ciudad, created_at
        FROM business_profiles
        ORDER BY id DESC;
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "nombre_negocio": row[1],
            "rubro": row[2],
            "ciudad": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]
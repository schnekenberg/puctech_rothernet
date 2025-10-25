import psycopg2

DATABASE_URL = "postgresql://postgres.blimgsurygysauhqsmsn:RestaurantProject@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"
try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)

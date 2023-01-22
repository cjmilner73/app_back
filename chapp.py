from chalice import Chalice
import psycopg2

app = Chalice(app_name='test')
db_user = 'test'
db_pass = 'password'
db_host = 'https://.....'
db_port = 5432

@app.route('/save_data', methods=["POST"])
def save_data():
    with psycopg2.connect(user=db_user, password=db_pass, ...) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (1,2))

@app.route('/get_data')
def get_data():
    with psycopg2.connect(user=db_user, password=db_pass, ...) as conn:
        with conn.cursor() as cur:    
            cur.execute("SELECT * FROM test")


@app.route('/something')
def something():
    with psycopg2.connect(user=db_user, password=db_pass, ...) as conn:
        with conn.cursor() as cur:    
            cur.execute(....)  # some other query

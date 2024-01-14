import sqlite3
class Database_Settings:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    def get_user(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM users WHERE chat_id={chat_id}").fetchone()

    def create_table(self):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        phone_number TEXT,
        latitude TEXT,
        longitude TEXT,
        chat_id INTEGER
        )
        """)

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS admins(
        chat_id TEXT
        )
        """)
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS matematika(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        a TEXT,
        b TEXT,
        d TEXT,
        true_variant TEXT
        )
        """)

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS biologiya(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        a TEXT,
        b TEXT,
        d TEXT,
        true_variant TEXT
        )
        """)
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS ona_tili(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        a TEXT,
        b TEXT,
        d TEXT,
        true_variant TEXT
        )
        """)

        self.conn.commit()

    def insert_new_user(self, data: dict):
        try:
            chat_idsi = data["chat_id"]
            tel_nomer = data["phone_number"]
            long = data["longitude"]
            lati = data["latitude"]
            ism = data["full_name"]
            self.cursor.execute(
                f"INSERT INTO users (full_name, phone_number, latitude, longitude, chat_id) VALUES (?,?,?,?,?)",
                (ism, tel_nomer, lati, long, chat_idsi))
            self.conn.commit()
            return True
        except Exception as exc:
            print(exc)
            return False


    def insert_question(self, data: dict, fan):
        try:
            self.cursor.execute(f"INSERT INTO '{fan}' (question, a, b, d, true_variant) VALUES (?,?,?,?,?)", (data[fan]["savol"], data[fan]["a"], data[fan]["b"], data[fan]["d"], data[fan]["true"]))
            self.conn.commit()
            return True
        except Exception as exc:
            print(exc)
            return False


    def insert_admin(self):
        self.cursor.execute("INSERT INTO admins (chat_id) VALUES (?)", ("5596277119",))
        self.cursor.execute("INSERT INTO admins (chat_id) VALUES (?)", ("5968397844",))
        self.conn.commit()
        return True

    def is_admin(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM admins WHERE chat_id={chat_id}").fetchone()

    def select_question(self, fan, idsi):
        return self.cursor.execute(f"SELECT * FROM '{fan}' WHERE id={idsi}").fetchall()

    def select_quest(self, idsi, fan, true):
        return self.cursor.execute(f"SELECT * FROM '{fan}' WHERE id={idsi} AND true_variant='{true}'").fetchone()

    def add_admin(self, chat_id):
        try:
            self.cursor.execute(f"INSERT INTO admins (chat_id) VALUES (?)", (chat_id,))
            self.conn.commit()
            return True
        except Exception as exc:
            print(exc)
            return False
    # def delelete_admin(self, chat_id):
    #     self.cursor.execute(f"DELETE FROM admins WHERE chat_id={chat_id}")
    #     self.conn.commit()
    #     return True

    def delete_admins(self):
        self.cursor.execute(f"DROP TABLE admins")
        return True

    def create_table_subject_result(self, chat_id):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{chat_id}_subject'(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        score INTEGER
        )
        """)
        self.conn.commit()
        return True

    def insert_table_sub(self, data: dict, chat_id):
        self.cursor.execute(f"INSERT INTO '{chat_id}_subject' (subject, score) VALUES (?,?)", (data["fan"], 0))
        self.conn.commit()
        return True

    def update_score(self, chat_id):
        score = self.cursor.execute(f"SELECT score FROM '{chat_id}_subject'").fetchone()
        self.cursor.execute(f"UPDATE '{chat_id}_subject' SET score={score[0] + 10}")
        self.conn.commit()
        return True

    def is_accepted(self, chat_id):
        return self.cursor.execute(f"SELECT score FROM '{chat_id}_subject' WHERE score>=65").fetchone()

    def select_admin(self):
        return self.cursor.execute(f"SELECT * FROM admins").fetchall()

    def select_user(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM users WHERE chat_id={chat_id}").fetchone()
    def select_65_score(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM '{chat_id}_subject'").fetchone()

    def select_score(self, chat_id):
        return self.cursor.execute(f"SELECT score FROM '{chat_id}_subject'").fetchone()

    def delete_user(self, chat_id):
        self.cursor.execute(f"DROP TABLE '{chat_id}_subject'")
        self.conn.commit()
        return True
    def is_admin(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM admins WHERE chat_id={chat_id}").fetchone()

    def get_class(self, class_num):
        try:
            return self.cursor.execute(f"SELECT * FROM '{class_num}'").fetchall()
        except Exception as exc:
            return False

    def create_class(self, class_num):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{class_num}' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        phone_number TEXT,
        location TEXT
        )
        """)
        self.conn.commit()
        return True

    def max_son(self, class_num):
        try:
            son = self.cursor.execute(f"SELECT MAX(id) FROM '{class_num}'").fetchone()
            return son
        except Exception as exc:
            return False

    def add_student(self, data: dict):
        try:
            self.cursor.execute(f"INSERT INTO '{data['class']}' (full_name, phone_number, location) VALUES (?,?,?)", (data["full_name"], data["phone_number"], data["location"]))
            self.conn.commit()
            return True
        except Exception as exc:
            print(exc)
            return False
    # def delete_table(self, chat_id):
    #     self.cursor.execute(f"DROP TABLE '{chat_id}_subject'")
    #     self.conn.commit()
    #     return True

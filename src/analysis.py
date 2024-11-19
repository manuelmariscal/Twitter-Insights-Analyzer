# analysis.py

from colorama import Fore, Style
import sqlite3
import traceback

class Analyzer:
    def __init__(self, sqlite_db, neo4j_db):
        self.sqlite_db = sqlite_db
        self.neo4j_db = neo4j_db

    def run_analysis(self):
        print(Fore.BLUE + "Iniciando análisis de datos..." + Style.RESET_ALL)
        self.sentiment_analysis()
        self.top_influential_users()
        self.trend_over_time()

    def sentiment_analysis(self):
        try:
            cursor = self.sqlite_db.connection.cursor()
            query = """
            SELECT sentimiento FROM tweets
            """
            cursor.execute(query)
            sentiments = [row[0] for row in cursor.fetchall()]
            if len(sentiments) > 0:
                avg_sentiment = sum(sentiments) / len(sentiments)
                print(Fore.CYAN + f"Sentimiento promedio: {avg_sentiment:.2f}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "No hay suficientes datos para calcular el sentimiento promedio." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error en análisis de sentimiento: {e}" + Style.RESET_ALL)
            traceback.print_exc()

    def top_influential_users(self):
        try:
            cursor = self.sqlite_db.connection.cursor()
            query = """
            SELECT nombre_usuario, seguidores FROM usuarios
            ORDER BY seguidores DESC
            LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print(Fore.CYAN + "Usuarios más influyentes:" + Style.RESET_ALL)
                for row in results:
                    print(f"- {row[0]} con {row[1]} seguidores")
            else:
                print(Fore.YELLOW + "No se encontraron usuarios influyentes." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error en análisis de usuarios influyentes: {e}" + Style.RESET_ALL)
            traceback.print_exc()

    def trend_over_time(self):
        try:
            cursor = self.sqlite_db.connection.cursor()
            query = """
            SELECT substr(fecha_hora, 1, 10) as date, COUNT(*) as count FROM tweets
            GROUP BY date
            ORDER BY date
            """
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print(Fore.CYAN + "Tendencia de tweets en el tiempo:" + Style.RESET_ALL)
                for row in results:
                    print(f"- {row[0]}: {row[1]} tweets")
            else:
                print(Fore.YELLOW + "No hay datos suficientes para mostrar tendencia en el tiempo." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error en análisis temporal: {e}" + Style.RESET_ALL)
            traceback.print_exc()

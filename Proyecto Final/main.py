# main.py

import sys
import argparse
from twitter_api import TwitterAPI
from sqlite_db import SQLiteDatabase
from neo4j_db import Neo4jDatabase
from analysis import Analyzer
from openai_analysis import OpenAIAnalysis
from utils import Utils
from colorama import Fore, Style
import traceback
import os
import json

def main():
    parser = argparse.ArgumentParser(description='Herramienta de Análisis de Datos de Twitter')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--fetch', action='store_true', help='Recolectar tweets desde la API de Twitter')
    group.add_argument('--load', type=str, help='Cargar tweets desde un archivo JSON en el directorio data/')
    args = parser.parse_args()

    try:
        # Inicialización de utilidades
        utils = Utils()

        if args.fetch:
            # Solicitar nombres de usuario al usuario
            usernames = utils.get_usernames()

            # Verificar que hay al menos un nombre de usuario
            if not usernames:
                print(Fore.YELLOW + "No se proporcionaron nombres de usuario. Terminando el programa." + Style.RESET_ALL)
                sys.exit()

            # Limitar a un usuario para evitar exceder los límites de tasa
            usernames = usernames[:1]

            # Inicialización de la API de Twitter
            twitter_api = TwitterAPI()

            # Obtener tweets de los usuarios especificados
            tweets_data = twitter_api.get_users_tweets(usernames)

            if not tweets_data:
                print(Fore.YELLOW + "No se pudieron obtener tweets. Por favor, verifica los nombres de usuario y los límites de tasa." + Style.RESET_ALL)
                sys.exit()

            # Guardar tweets en un archivo para análisis posterior
            utils.save_tweets_to_file(tweets_data, 'tweets.json')
        elif args.load:
            json_file = args.load
            json_path = os.path.join('data', json_file)
            if not os.path.exists(json_path):
                print(Fore.RED + f"El archivo JSON '{json_file}' no existe en el directorio 'data/'." + Style.RESET_ALL)
                sys.exit(1)
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    tweets_data = json.load(f)
                print(Fore.GREEN + f"Datos de tweets cargados desde '{json_path}' exitosamente." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error al cargar el archivo JSON: {e}" + Style.RESET_ALL)
                traceback.print_exc()
                sys.exit(1)

        # Conexión a la base de datos SQLite
        sqlite_db = SQLiteDatabase()
        sqlite_db.create_tables()
        sqlite_db.insert_data(tweets_data)

        # Conexión a la base de datos Neo4j
        neo4j_db = Neo4jDatabase()
        neo4j_db.create_constraints()
        neo4j_db.insert_data(tweets_data)

        # Análisis de datos
        analyzer = Analyzer(sqlite_db, neo4j_db)
        analyzer.run_analysis()

        # Análisis con OpenAI
        openai_analysis = OpenAIAnalysis()
        summary = openai_analysis.singularity(tweets_data)

        if summary:
            if args.fetch:
                # Publicar el resumen en Twitter
                twitter_api.post_tweet(summary)
                print(Fore.GREEN + "El resumen se ha publicado en Twitter exitosamente." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "El resumen se ha generado, pero no se publicará automáticamente porque se cargaron datos desde un archivo." + Style.RESET_ALL)
                print(Fore.CYAN + "Resumen:" + Style.RESET_ALL)
                print(summary)
        else:
            print(Fore.YELLOW + "No se pudo generar el resumen con OpenAI." + Style.RESET_ALL)

        # Cerrar conexiones
        if args.fetch:
            twitter_api.close_connection()
        sqlite_db.close_connection()
        neo4j_db.close_connection()

        print(Fore.GREEN + "Análisis completado exitosamente." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Ocurrió un error en el programa principal: {e}" + Style.RESET_ALL)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

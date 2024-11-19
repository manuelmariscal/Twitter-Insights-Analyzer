# neo4j_db.py

from neo4j import GraphDatabase
from utils import Utils
from textblob import TextBlob
from colorama import Fore, Style
import os
from dotenv import load_dotenv
import traceback

class Neo4jDatabase:
    def __init__(self):
        self.utils = Utils()
        self.driver = self.connect()

    def connect(self):
        try:
            # Cargar variables de entorno
            load_dotenv()
            uri = "bolt://localhost:7687"
            user = "neo4j"
            password = os.getenv('NEO4J_PASSWORD')

            if not password:
                print(Fore.RED + "Error: La contraseña de Neo4j no está configurada." + Style.RESET_ALL)
                raise Exception("Contraseña de Neo4j no configurada")

            driver = GraphDatabase.driver(uri, auth=(user, password))
            print(Fore.GREEN + "Conectado a la base de datos Neo4j exitosamente." + Style.RESET_ALL)
            return driver
        except Exception as e:
            print(Fore.RED + f"Error al conectar a Neo4j: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            raise

    def create_constraints(self):
        try:
            with self.driver.session() as session:
                # Constraints para unicidad con la sintaxis actualizada
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:Usuario) REQUIRE u.usuario_id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tweet) REQUIRE t.tweet_id IS UNIQUE")
            print(Fore.GREEN + "Constraints creados en Neo4j." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al crear constraints en Neo4j: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            raise

    def insert_data(self, tweets_data):
        try:
            if not tweets_data:
                print(Fore.YELLOW + "No hay datos de tweets para insertar en Neo4j." + Style.RESET_ALL)
                return
            with self.driver.session() as session:
                for data in tweets_data:
                    if 'tweet' in data and 'user' in data:
                        # Datos provenientes de la API
                        tweet = data['tweet']
                        user = data['user']

                        if not user:
                            print(Fore.YELLOW + "No se encontró información del usuario para un tweet. Saltando..." + Style.RESET_ALL)
                            continue  # Saltar si no hay información de usuario

                        # Procesar datos del usuario
                        seguidores = user.public_metrics.get('followers_count', 0) if hasattr(user, 'public_metrics') and user.public_metrics else 0
                        verificado = user.verified if hasattr(user, 'verified') and user.verified is not None else False
                        ubicacion = user.location if hasattr(user, 'location') else None
                        nombre_usuario = user.username if hasattr(user, 'username') else None

                        session.run("""
                            MERGE (u:Usuario {usuario_id: $usuario_id})
                            SET u.nombre_usuario = $nombre_usuario,
                                u.seguidores = $seguidores,
                                u.ubicacion = $ubicacion,
                                u.verificado = $verificado
                        """, usuario_id=str(user.id),
                             nombre_usuario=nombre_usuario,
                             seguidores=seguidores,
                             ubicacion=ubicacion,
                             verificado=verificado)
                        # Análisis de sentimiento
                        analysis = TextBlob(tweet.text)
                        sentiment = analysis.sentiment.polarity

                        # Procesar datos del tweet
                        retweets = tweet.public_metrics.get('retweet_count', 0) if hasattr(tweet, 'public_metrics') and tweet.public_metrics else 0
                        likes = tweet.public_metrics.get('like_count', 0) if hasattr(tweet, 'public_metrics') and tweet.public_metrics else 0

                        session.run("""
                            MERGE (t:Tweet {tweet_id: $tweet_id})
                            SET t.contenido = $contenido,
                                t.fecha_hora = $fecha_hora,
                                t.retweets = $retweets,
                                t.likes = $likes,
                                t.sentimiento = $sentimiento
                        """, tweet_id=str(tweet.id),
                             contenido=tweet.text,
                             fecha_hora=tweet.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(tweet, 'created_at') else None,
                             retweets=retweets,
                             likes=likes,
                             sentimiento=sentiment)
                        # Relación PUBLICA
                        session.run("""
                            MATCH (u:Usuario {usuario_id: $usuario_id}), (t:Tweet {tweet_id: $tweet_id})
                            MERGE (u)-[:PUBLICA]->(t)
                        """, usuario_id=str(user.id), tweet_id=str(tweet.id))
                    else:
                        # Datos provenientes de archivos JSON
                        tweet_id = data.get('tweet_id')
                        usuario_id = data.get('usuario_id')
                        nombre_usuario = data.get('nombre_usuario')
                        contenido = data.get('contenido')
                        fecha_hora = data.get('fecha_hora')
                        retweets = data.get('retweets', 0)
                        likes = data.get('likes', 0)
                        seguidores = data.get('seguidores', 0)
                        ubicacion = data.get('ubicacion')
                        verificado = data.get('verificado', False)
                        sentimiento = TextBlob(contenido).sentiment.polarity  # Recalcular sentimiento

                        # MERGE Usuario
                        session.run("""
                            MERGE (u:Usuario {usuario_id: $usuario_id})
                            SET u.nombre_usuario = $nombre_usuario,
                                u.seguidores = $seguidores,
                                u.ubicacion = $ubicacion,
                                u.verificado = $verificado
                        """, usuario_id=usuario_id,
                             nombre_usuario=nombre_usuario,
                             seguidores=seguidores,
                             ubicacion=ubicacion,
                             verificado=verificado)
                        # MERGE Tweet
                        session.run("""
                            MERGE (t:Tweet {tweet_id: $tweet_id})
                            SET t.contenido = $contenido,
                                t.fecha_hora = $fecha_hora,
                                t.retweets = $retweets,
                                t.likes = $likes,
                                t.sentimiento = $sentimiento
                        """, tweet_id=tweet_id,
                             contenido=contenido,
                             fecha_hora=fecha_hora,
                             retweets=retweets,
                             likes=likes,
                             sentimiento=sentimiento)
                        # MERGE Relación PUBLICA
                        session.run("""
                            MATCH (u:Usuario {usuario_id: $usuario_id}), (t:Tweet {tweet_id: $tweet_id})
                            MERGE (u)-[:PUBLICA]->(t)
                        """, usuario_id=usuario_id, tweet_id=tweet_id)
            print(Fore.GREEN + "Datos insertados en Neo4j exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al insertar datos en Neo4j: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            raise

    def close_connection(self):
        self.driver.close()
        print(Fore.GREEN + "Conexión a Neo4j cerrada." + Style.RESET_ALL)

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
                # Constraints para unicidad
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:Usuario) REQUIRE u.nombre_usuario IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tweet) REQUIRE t.tweet_id IS UNIQUE")
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (h:Hashtag) REQUIRE h.texto IS UNIQUE")
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
                        tweet = data['tweet']
                        user = data['user']

                        if not user:
                            print(Fore.YELLOW + "No se encontró información del usuario para un tweet. Saltando..." + Style.RESET_ALL)
                            continue

                        # Procesar datos del usuario
                        nombre_usuario = user.username if hasattr(user, 'username') else None

                        # Verificar que public_metrics no sea None
                        seguidores = user.public_metrics.get('followers_count', 0) if hasattr(user, 'public_metrics') and user.public_metrics else 0
                        retweets = tweet.public_metrics.get('retweet_count', 0) if hasattr(tweet, 'public_metrics') and tweet.public_metrics else 0
                        likes = tweet.public_metrics.get('like_count', 0) if hasattr(tweet, 'public_metrics') and tweet.public_metrics else 0

                        # Crear nodo de usuario
                        session.run("""
                            MERGE (u:Usuario {nombre_usuario: $nombre_usuario})
                            SET u.seguidores = $seguidores,
                                u.verificado = $verificado,
                                u.ubicacion = $ubicacion
                        """, nombre_usuario=nombre_usuario,
                             seguidores=seguidores,
                             verificado=user.verified if hasattr(user, 'verified') else False,
                             ubicacion=user.location if hasattr(user, 'location') else None)

                        # Análisis de sentimiento
                        analysis = TextBlob(tweet.text)
                        sentiment = analysis.sentiment.polarity

                        # Crear nodo de tweet
                        session.run("""
                            MERGE (t:Tweet {tweet_id: $tweet_id})
                            SET t.contenido = $contenido,
                                t.fecha_hora = $fecha_hora,
                                t.retweets = $retweets,
                                t.likes = $likes,
                                t.sentimiento = $sentimiento
                        """, tweet_id=str(tweet.id),
                             contenido=tweet.text,
                             fecha_hora=tweet.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(tweet, 'created_at') and tweet.created_at else None,
                             retweets=retweets,
                             likes=likes,
                             sentimiento=sentiment)

                        # Relación de Publicación
                        session.run("""
                            MATCH (u:Usuario {nombre_usuario: $nombre_usuario}), (t:Tweet {tweet_id: $tweet_id})
                            MERGE (u)-[:PUBLICA]->(t)
                        """, nombre_usuario=nombre_usuario, tweet_id=str(tweet.id))

                        # Detectar menciones (si existen)
                        if tweet.text and '@' in tweet.text:
                            mentions = [word.strip('@') for word in tweet.text.split() if word.startswith('@')]
                            for mention in mentions:
                                session.run("""
                                    MATCH (u:Usuario {nombre_usuario: $nombre_usuario}), (m:Usuario {nombre_usuario: $mention})
                                    MERGE (u)-[:MENTIONA]->(m)
                                """, nombre_usuario=nombre_usuario, mention=mention)

                        # Detectar retweets y crear relaciones
                        if hasattr(tweet, 'referenced_tweets') and tweet.referenced_tweets:
                            for ref_tweet in tweet.referenced_tweets:
                                session.run("""
                                    MATCH (t:Tweet {tweet_id: $tweet_id}), (rt:Tweet {tweet_id: $ref_tweet_id})
                                    MERGE (t)-[:RETWEETEA]->(rt)
                                """, tweet_id=str(tweet.id), ref_tweet_id=ref_tweet.id)

                        # Crear relaciones basadas en hashtags
                        hashtags = [word.strip('#') for word in tweet.text.split() if word.startswith('#')]
                        for hashtag in hashtags:
                            session.run("""
                                MERGE (h:Hashtag {texto: $hashtag})
                                MERGE (t:Tweet {tweet_id: $tweet_id})
                                MERGE (t)-[:TRATA_DE]->(h)
                            """, hashtag=hashtag, tweet_id=str(tweet.id))

            print(Fore.GREEN + "Datos insertados en Neo4j exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al insertar datos en Neo4j: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            raise

    def close_connection(self):
        self.driver.close()
        print(Fore.GREEN + "Conexión a Neo4j cerrada." + Style.RESET_ALL)

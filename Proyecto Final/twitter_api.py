# twitter_api.py

import tweepy
from tweepy.errors import TooManyRequests, Forbidden, TweepyException
from utils import Utils
from colorama import Fore, Style
import os
from dotenv import load_dotenv
import traceback
import time

class TwitterAPI:
    def __init__(self):
        self.utils = Utils()
        self.client, self.api_v1 = self.authenticate()

    def authenticate(self):
        try:
            # Cargar variables de entorno
            load_dotenv()
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

            # Claves para autenticación OAuth 1.0a (necesarias para publicar tweets)
            consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
            consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

            if not all([bearer_token, consumer_key, consumer_secret, access_token, access_token_secret]):
                print(Fore.RED + "Error: Las credenciales de la API de Twitter no están completas." + Style.RESET_ALL)
                raise Exception("Credenciales de Twitter incompletas")

            # Cliente para lectura (API v2)
            client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=False  # Desactivamos espera automática para manejar manualmente
            )

            # Autenticación para publicar tweets (API v1.1)
            auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
            api_v1 = tweepy.API(auth)

            print(Fore.GREEN + "Autenticado con la API de Twitter exitosamente." + Style.RESET_ALL)
            return client, api_v1
        except Exception as e:
            print(Fore.RED + f"Error al autenticar con Twitter API: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            raise

    def get_users_tweets(self, usernames):
        tweets_data = []
        for username in usernames:
            while True:
                try:
                    print(Fore.BLUE + f"Obteniendo tweets del usuario @{username}..." + Style.RESET_ALL)
                    # Obtener el ID del usuario
                    user_response = self.client.get_user(username=username)
                    if not user_response.data:
                        print(Fore.RED + f"No se encontró al usuario @{username}." + Style.RESET_ALL)
                        break
                    user_id = user_response.data.id

                    # Obtener los tweets del usuario
                    response = self.client.get_users_tweets(
                        id=user_id,
                        max_results=5,
                        tweet_fields=['created_at', 'text', 'public_metrics', 'lang'],
                        user_fields=['username', 'public_metrics', 'verified', 'location']
                    )

                    if response.errors:
                        print(Fore.RED + f"Errores al obtener tweets del usuario @{username}: {response.errors}" + Style.RESET_ALL)
                        break

                    tweets = response.data if response.data else []

                    for tweet in tweets:
                        tweets_data.append({
                            'tweet': tweet,
                            'user': user_response.data  # Información del usuario
                        })

                    print(Fore.GREEN + f"Se obtuvieron {len(tweets)} tweets del usuario @{username}." + Style.RESET_ALL)
                    break  # Salir del bucle while si se obtuvo la información correctamente
                except Forbidden as e:
                    print(Fore.RED + f"No tienes acceso para obtener los tweets del usuario @{username}. Verifica si el usuario es privado o si tienes los permisos necesarios." + Style.RESET_ALL)
                    traceback.print_exc()
                    break
                except TooManyRequests as e:
                    print(Fore.RED + f"Se ha excedido el límite de tasa para el usuario @{username}. Debes esperar antes de volver a intentarlo." + Style.RESET_ALL)
                    # Esperar hasta que se restablezca el límite
                    reset_time = int(e.response.headers.get('x-rate-limit-reset', time.time() + 900))
                    wait_time = max(reset_time - int(time.time()), 0)
                    print(Fore.YELLOW + f"Esperando {wait_time + 5} segundos antes de continuar..." + Style.RESET_ALL)
                    time.sleep(wait_time + 5)  # Agregar 5 segundos adicionales por seguridad
                except TweepyException as e:
                    print(Fore.RED + f"Error de Tweepy al obtener tweets del usuario @{username}: {e}" + Style.RESET_ALL)
                    traceback.print_exc()
                    break
                except Exception as e:
                    print(Fore.RED + f"Error inesperado al obtener tweets del usuario @{username}: {e}" + Style.RESET_ALL)
                    traceback.print_exc()
                    break
        return tweets_data

    def post_tweet(self, text):
        try:
            # Publicar el tweet
            self.api_v1.update_status(status=text)
            print(Fore.GREEN + "Tweet publicado exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al publicar el tweet: {e}" + Style.RESET_ALL)
            traceback.print_exc()

    def close_connection(self):
        # No es necesario cerrar conexiones explícitamente
        pass

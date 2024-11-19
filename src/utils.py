# utils.py

from colorama import Fore, Style, init
import json
import os
import traceback

class Utils:
    def __init__(self):
        init(autoreset=True)

    def get_usernames(self):
        try:
            usernames_input = input(Fore.BLUE + "Ingrese los nombres de usuario de Twitter separados por comas (máximo 1 usuario): " + Style.RESET_ALL)
            usernames_list = [uname.strip().lstrip('@') for uname in usernames_input.split(',') if uname.strip()]
            if not usernames_list:
                print(Fore.RED + "Debe ingresar al menos un nombre de usuario." + Style.RESET_ALL)
                exit()
            return usernames_list
        except Exception as e:
            print(Fore.RED + f"Error al obtener nombres de usuario: {e}" + Style.RESET_ALL)
            exit()

    def save_tweets_to_file(self, tweets_data, filename):
        try:
            # Crear directorio 'data' si no existe
            if not os.path.exists('data'):
                os.makedirs('data')

            existing_tweets = []
            file_path = os.path.join('data', filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_tweets = json.load(f)
                    if not isinstance(existing_tweets, list):
                        existing_tweets = []
                        print(Fore.YELLOW + f"El archivo '{filename}' no es una lista válida. Se creará una nueva lista." + Style.RESET_ALL)

            # Procesar nuevos tweets
            for data in tweets_data:
                if 'tweet' in data and 'user' in data:
                    # Datos provenientes de la API
                    tweet = data['tweet']
                    user = data['user']

                    # Verificar si 'public_metrics' existe y no es None para el usuario
                    if hasattr(user, 'public_metrics') and user.public_metrics:
                        seguidores = user.public_metrics.get('followers_count', 0)
                    else:
                        seguidores = 0
                        print(Fore.YELLOW + f"No se encontraron 'public_metrics' para el usuario @{user.username}. Asignando 0 seguidores." + Style.RESET_ALL)

                    # Verificar si 'public_metrics' existe y no es None para el tweet
                    if hasattr(tweet, 'public_metrics') and tweet.public_metrics:
                        retweets = tweet.public_metrics.get('retweet_count', 0)
                        likes = tweet.public_metrics.get('like_count', 0)
                    else:
                        retweets = 0
                        likes = 0
                        print(Fore.YELLOW + f"No se encontraron 'public_metrics' para el tweet ID {tweet.id}. Asignando 0 retweets y 0 likes." + Style.RESET_ALL)

                    existing_tweets.append({
                        'tweet_id': str(tweet.id),
                        'usuario_id': str(user.id),
                        'nombre_usuario': user.username if hasattr(user, 'username') else None,
                        'contenido': tweet.text,
                        'fecha_hora': tweet.created_at.isoformat() if hasattr(tweet, 'created_at') and tweet.created_at else None,
                        'retweets': retweets,
                        'likes': likes,
                        'seguidores': seguidores,
                        'ubicacion': user.location if hasattr(user, 'location') else None,
                        'verificado': user.verified if hasattr(user, 'verified') else False,
                        'lang': tweet.lang if hasattr(tweet, 'lang') else None
                    })
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
                    lang = data.get('lang')

                    existing_tweets.append({
                        'tweet_id': tweet_id,
                        'usuario_id': usuario_id,
                        'nombre_usuario': nombre_usuario,
                        'contenido': contenido,
                        'fecha_hora': fecha_hora,
                        'retweets': retweets,
                        'likes': likes,
                        'seguidores': seguidores,
                        'ubicacion': ubicacion,
                        'verificado': verificado,
                        'lang': lang
                    })

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_tweets, f, ensure_ascii=False, indent=4)
            print(Fore.GREEN + f"Tweets guardados en 'data/{filename}' exitosamente." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error al guardar tweets en archivo: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            exit()

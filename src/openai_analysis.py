# openai_analysis.py

import os
import time
import requests
import json
import re
from utils import Utils
from colorama import Fore, Style
import traceback

MAX_RETRIES = 5  # Número máximo de reintentos
INITIAL_WAIT_TIME = 2  # Tiempo inicial de espera en segundos

class OpenAIAnalysis:
    def __init__(self):
        self.utils = Utils()
        self.api_key = self.load_api_key()

    def load_api_key(self):
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print(Fore.RED + "Error: La clave de API de OpenAI no está configurada." + Style.RESET_ALL)
                raise Exception("Clave de API de OpenAI no configurada")
            print(Fore.GREEN + "API de OpenAI configurada exitosamente." + Style.RESET_ALL)
            return api_key
        except Exception as e:
            print(Fore.RED + f"Error al configurar la API de OpenAI: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            raise

    def ask_singularity(self, prompt, max_tokens=4000, retry_count=0):
        if not self.api_key:
            raise Exception("La variable de entorno OPENAI_API_KEY no se ha configurado.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",  # Modelo corregido
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.5
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
            else:
                # Manejo de errores específicos basados en el código de estado
                error_response = response.json()
                if response.status_code == 500 and error_response.get("error", {}).get("code") == "request_timeout":
                    if retry_count < MAX_RETRIES:
                        wait_time = INITIAL_WAIT_TIME * (2 ** retry_count)
                        print(f"Tiempo de espera agotado. Reintentando {retry_count + 1} en {wait_time} segundos.")
                        time.sleep(wait_time)
                        return self.ask_singularity(prompt, max_tokens, retry_count + 1)
                    else:
                        raise Exception(f"Tiempo de espera agotado después de {MAX_RETRIES} reintentos.")
                else:
                    raise Exception(f"Error en la API: {response.status_code}, {response.text}")

        except requests.exceptions.RequestException as e:
            if retry_count < MAX_RETRIES:
                wait_time = INITIAL_WAIT_TIME * (2 ** retry_count)
                print(f"Error de solicitud: {str(e)}. Reintentando {retry_count + 1} en {wait_time} segundos.")
                time.sleep(wait_time)
                return self.ask_singularity(prompt, max_tokens, retry_count + 1)
            else:
                raise Exception(f"Error de solicitud no resuelto después de {MAX_RETRIES} reintentos. Error: {str(e)}")

    def singularity(self, tweets_data):
        try:
            if not tweets_data:
                print(Fore.YELLOW + "No hay datos de tweets para analizar con OpenAI." + Style.RESET_ALL)
                return None
            print(Fore.BLUE + "Realizando análisis con OpenAI..." + Style.RESET_ALL)
            # Preparar el contenido para enviar a OpenAI
            if all('tweet' in data and 'user' in data for data in tweets_data):
                # Datos provenientes de la API
                tweets_text = [data['tweet'].text for data in tweets_data if 'tweet' in data and data['tweet']]
            else:
                # Datos provenientes de archivos JSON
                tweets_text = [data.get('contenido', '') for data in tweets_data]

            combined_text = "\n\n".join(tweets_text)

            # Crear el prompt para OpenAI
            prompt = (
                f"Analiza los siguientes tweets y proporciona un resumen de las tendencias, sentimientos y temas principales:\n\n"
                f"   {combined_text}\n\n"
                f"Lo que harás es redactar un tweet con esta información para compartir con otros usuarios. Mencionando que el análisis fue realizado por OpenAI utilizando herramientas programáticas y bases de datos para la materia de Modelado de Datos de la Maestría en Cómputo Aplicado como proyecto final de esa materia.\n\n"
                f"Debes de utilizar forzozamente emojis, hashtags y menciones para hacerlo más interesante y atractivo para los lectores.\n\n"
            )

            # Enviar la solicitud a OpenAI usando ask_singularity
            analysis_text = self.ask_singularity(prompt)

            print(Fore.CYAN + "Análisis de OpenAI completado:" + Style.RESET_ALL)
            print(analysis_text)

            return analysis_text

        except Exception as e:
            print(Fore.RED + f"Error en el análisis con OpenAI: {e}" + Style.RESET_ALL)
            traceback.print_exc()
            return None 

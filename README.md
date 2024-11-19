# 📊 **Análisis de Datos de Twitter: Transformando la Información en Insights Valiosos** 🐦💡

En el dinámico entorno de las redes sociales, comprender y analizar el comportamiento de los usuarios es fundamental para empresas, investigadores y profesionales del marketing. Twitter, con su flujo constante de tweets, ofrece una mina de oro de información que, si se analiza adecuadamente, puede revelar tendencias, sentimientos y patrones de interacción. Este proyecto está diseñado para extraer, analizar y generar **insights valiosos** de los datos de Twitter, proporcionando herramientas prácticas para la toma de decisiones informadas.

## 🚀 **Objetivo del Proyecto**

El proyecto tiene como objetivo analizar los datos obtenidos de Twitter y generar insights valiosos mediante el **análisis de sentimientos**, la **identificación de usuarios influyentes**, la **detección de tendencias** y la **visualización de relaciones entre usuarios y temas**. Utiliza una combinación de **modelos de datos relacionales** y **basados en grafos** para ofrecer un enfoque robusto y detallado.

### **Descripción del Problema que se Resuelve**

Las organizaciones enfrentan múltiples desafíos cuando intentan extraer valor de los datos generados en Twitter:

1. **📈 Gestión de Grandes Volúmenes de Datos**: La gran cantidad de tweets generados constantemente.
2. **😊 Análisis de Sentimientos**: Determinar el tono emocional de los tweets para evaluar la percepción pública.
3. **👥 Identificación de Influencers**: Reconocer a los usuarios con mayor impacto y seguidores.
4. **🔍 Detección de Tendencias**: Identificar temas emergentes y su evolución temporal.
5. **🕸️ Visualización de Relaciones**: Entender cómo interactúan los usuarios y cómo se conectan los temas.

Este proyecto soluciona estos problemas mediante la recolección de datos, el análisis y la visualización de los resultados, utilizando **SQLite** y **Neo4j** para almacenar y analizar los datos.

## 🎯 **Preguntas de Valor que Responde el Proyecto**

1. **📊 ¿Cuál es el sentimiento promedio de los tweets sobre un tema específico?**
   
   El análisis de sentimiento se realiza utilizando herramientas de procesamiento de lenguaje natural, como **TextBlob**. El sentimiento de cada tweet se evalúa en una escala de -1 a 1, y el resultado promedio se calcula para determinar si la conversación en torno a un tema es positiva, negativa o neutral. Este análisis es crucial para entender cómo se perciben temas, productos, o eventos en la plataforma.

2. **👑 ¿Quiénes son los usuarios más influyentes en una red específica?**
   
   Los usuarios más influyentes se determinan a partir de su número de seguidores, interacciones (como retweets y likes), y su nivel de verificación. Se realiza un análisis mediante la base de datos **SQLite**, donde se identifican los usuarios más seguidos y los que generan más interacciones. Este análisis permite a las marcas y organizaciones enfocar sus esfuerzos de marketing en los usuarios que tienen mayor capacidad de generar impacto.

3. **📈 ¿Cómo han evolucionado las tendencias de conversación a lo largo del tiempo?**
   
   El análisis temporal de los tweets permite identificar cómo cambian los temas y la intensidad de la conversación a lo largo del tiempo. Mediante consultas en **SQLite**, se pueden agrupar los tweets por fecha, lo que permite visualizar picos de actividad relacionados con ciertos eventos o tendencias, proporcionando información valiosa para ajustar estrategias en tiempo real.

4. **👥 ¿Existen comunidades de usuarios que interactúan frecuentemente entre sí?**
   
   El modelo de **grafos** en **Neo4j** permite explorar cómo los usuarios interactúan entre sí. Identificando grupos de usuarios que se mencionan, retuitean o responden a tweets de otros, se pueden visualizar comunidades de interés. Esta información es útil para segmentar audiencias y generar campañas dirigidas a grupos específicos que ya están interactuando activamente sobre ciertos temas.

5. **🔗 ¿Qué relaciones existen entre diferentes temas de conversación?**
   
   Utilizando el modelo de grafos, se pueden visualizar las conexiones entre diferentes temas y cómo se relacionan entre sí a través de hashtags, menciones o contenido similar. Esto facilita la identificación de patrones de conversación complejos, mostrando cómo un tema puede derivar en otro y cómo los usuarios se mueven de un tema a otro, lo que ayuda a identificar tendencias emergentes.

## 🤔 **Reflexión sobre la Idoneidad de Cada Modelo de Datos en el Proyecto**

En este proyecto, se utiliza un enfoque de **modelado de datos** que combina dos tipos de bases de datos, cada una ideal para diferentes aspectos del análisis. La elección de estos modelos facilita la extracción de insights complejos de una manera organizada.

### **Modelo Relacional (SQLite)**

El modelo **relacional** se utiliza principalmente para almacenar y organizar datos estructurados sobre tweets y usuarios. Gracias a su capacidad para manejar grandes volúmenes de datos y realizar consultas estructuradas con SQL, es ideal para realizar análisis estadísticos y agregaciones, como el cálculo del sentimiento promedio o la identificación de los usuarios más influyentes.

**Ventajas:**
- Permite consultas rápidas y eficientes para obtener estadísticas y promedios.
- Asegura la integridad y organización de los datos mediante claves primarias y foráneas.

**Limitaciones:**
- No es tan eficiente para representar relaciones complejas o explorar interacciones entre entidades, algo que se resuelve con el modelo de grafos.

### **Modelo Basado en Grafos (Neo4j)**

El modelo **basado en grafos** es crucial para representar las relaciones dinámicas entre usuarios y tweets. En Twitter, las interacciones entre usuarios, como menciones o retweets, pueden ser representadas de manera natural como un grafo, donde los usuarios son nodos y sus interacciones son las relaciones. Esto permite realizar un análisis más profundo de las redes sociales y detectar patrones de influencia y difusión de temas.

**Ventajas:**
- Permite visualizar y explorar relaciones complejas entre usuarios y temas.
- Facilita la detección de comunidades de usuarios y la propagación de tendencias en la red.

**Limitaciones:**
- Requiere herramientas especializadas, como **Neo4j**, y conocimientos adicionales en teoría de grafos y su consulta con **Cypher**.

## 🏁 **Pasos para Ejecutar el Proyecto**

### **1. Crear un Entorno Virtual (Virtualenv)**

Para evitar conflictos con otras dependencias, es recomendable crear un entorno virtual.

```bash
# Instalar virtualenv si no lo tienes
pip install virtualenv

# Crear un entorno virtual llamado 'twitter-analysis-env'
virtualenv twitter-analysis-env

# Activar el entorno virtual
# En Linux/Mac:
source twitter-analysis-env/bin/activate
# En Windows:
twitter-analysis-env\Scripts\activate
```

### **2. Instalar Dependencias**

Instala las dependencias necesarias desde el archivo `requirements.txt` o ejecutando el siguiente comando:

```bash
# Crear el archivo requirements.txt con las dependencias necesarias
pip install -r requirements.txt
```

Dependencias principales:

- `tweepy`: Para interactuar con la API de Twitter.
- `neo4j`: Para trabajar con la base de datos basada en grafos.
- `textblob`: Para realizar análisis de sentimiento.
- `colorama`: Para mejorar la salida en la terminal.
- `python-dotenv`: Para gestionar variables de entorno.
- `openai`: Para procesar y generar resúmenes e insights.
- `requests-oauthlib`: Para la autenticación con OAuth 2.0.

### **3. Obtener las API Keys de Twitter**

Para acceder a los datos de Twitter, necesitas las **API keys**. Sigue estos pasos:

1. Dirígete a [Twitter Developer Portal](https://developer.twitter.com/en/apps).
2. Crea una nueva aplicación de Twitter.
3. Obtén las siguientes claves y tokens:
   - `TWITTER_CONSUMER_KEY`
   - `TWITTER_CONSUMER_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
   - `TWITTER_OAUTH_ID`
   - `TWITTER_OAUTH_SECRET`
   - `TWITTER_BEARER_TOKEN`

Añade estas variables a tu archivo `.env` de configuración:

```ini
## OAuth 1.0a KEYS (Solo si las necesitas)
TWITTER_CONSUMER_KEY="tu_consumer_key"
TWITTER_CONSUMER_SECRET="tu_consumer_secret"
TWITTER_ACCESS_TOKEN="tu_access_token"
TWITTER_ACCESS_TOKEN_SECRET="tu_access_token_secret"

## OAuth 2.0 KEYS
TWITTER_OAUTH_ID="tu_oauth_id"
TWITTER_OAUTH_SECRET="tu_oauth_secret"
TWITTER_REDIRECT_URI="https://x.com/"
TWITTER_SCOPES="tweet.read tweet.write users.read offline.access"

## Bearer Token (Opcional para algunas operaciones)
TWITTER_BEARER_TOKEN="tu_bearer_token"

## Neo4j Database Credentials
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="tu_neo4j_password"

## OPEN AI 
OPENAI_API_KEY="sk-tu_openai_api_key"
```

### **4. Ejecutar el Código**

Con las dependencias instaladas y las claves configuradas, puedes proceder a ejecutar el análisis. El flujo del código incluirá la recolección de datos, análisis de sentimientos, y exploración de relaciones con el modelo de grafos. A continuación se muestra cómo ejecutar el script principal.

```bash
# Ejecuta el script de análisis
python main.py --fetch
```

O si ya tienes un archivo JSON con datos de tweets

:

```bash
# Cargar tweets desde un archivo JSON
python main.py --load tweets.json
```

### **5. Visualización de Resultados**

El análisis se realiza en dos bases de datos:

1. **SQLite**: Se utiliza para almacenar los datos estructurados, permitiendo realizar análisis estadísticos y consultas estructuradas.
2. **Neo4j**: Se usa para explorar relaciones entre usuarios y tweets, visualizando la interacción en una red de grafos.

El análisis generado incluye:
- **Análisis de Sentimiento**: Promedio de sentimientos de los tweets.
- **Usuarios Influyentes**: Los usuarios con más seguidores e interacciones.
- **Tendencias Temporales**: Análisis de la evolución de los temas de conversación a lo largo del tiempo.

Además, se genera un **resumen de los datos utilizando OpenAI**, el cual puede ser publicado en Twitter si se ejecuta en el modo de recolección (`--fetch`).

## 🧩 **Resumen**

Este proyecto proporciona una solución eficiente para transformar los datos de Twitter en insights valiosos para diversas aplicaciones, desde el análisis de sentimientos hasta la identificación de tendencias emergentes. Con el uso de modelos relacionales y basados en grafos, el proyecto ofrece un enfoque detallado y robusto para analizar interacciones entre usuarios y temas.

Sigue estos pasos para ejecutar el código y obtener insights de Twitter en tus propios proyectos. ¡Aprovecha el poder de los datos y lleva tus análisis al siguiente nivel! 🚀📊
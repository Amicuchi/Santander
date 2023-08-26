import pandas as pd
import requests 
import json
import openai

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
openai_api_key = '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'

# EXTRACT => Extraindo os IDs dos usuários
df = pd.read_csv('users.csv')
user_ids = df['UserID'].tolist()
# print(user_ids)

# Obter os dados dos usuários usando a API da Santander Dev Week
def get_user(id):
    # Consumir o endpoint para obter os dados de cada cliente
    # GET https://sdw-2023-prd.up.railway.app/users/{id}
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
# print(json.dumps(users, indent=4))

# TRANSFORM
openai.api_key = openai_api_key

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {  
                "role": "system", 
                "content": "Você é um especialista em marketing bancário"
            },
            {
                "role": "user", 
                "content": f"Crie uma mensagem para {user['name']} sobre a importancia de investimentos (máximo de 100 caracteres)"
            }
        ]
    )

    return completion.choices[0].message.content.strip('\"')

for user in users:
    news = generate_ai_news(user)
    # print(news)
    user['news'].append({
        "description": news
    })

# LOAD => Atualizar a lista de NEWS de cada usuário.
def update_user(user):
    response = requests.put(f'{sdw2023_api_url}/users/{id}', json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}")
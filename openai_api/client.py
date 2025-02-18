from openai import OpenAI
from openai import OpenAIError, RateLimitError

client = OpenAI(
    api_key='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'
)

def get_car_ai_bio(model, brand, year):
    message = ''''
    Me mostre uma descrição de venda para o carro {} {} {} em apenas 250 caracteres. Fale coisas específicas desse modelo.
    '''
    message =  message.format(brand, model, year)
    try: 
        response = client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': message
                }
            ],
            max_tokens= 1000,
            model='gpt-4o-mini',
        )
        return response['choices'][0]['text']

    except RateLimitError:
        return "Você atingiu o limite de uso da API. Tente novamente mais tarde."
    
    except OpenAIError as e:
        return f"Ocorreu um erro ao gerar a descrição: {str(e)}"
    
    except Exception as e:
        return f"Erro inesperado: {str(e)}"
import boto3
import io
from PIL import Image
from datetime import datetime
import logging

# Configurar logs detalhados
logging.basicConfig(level=logging.DEBUG)

# Cliente AWS configurado diretamente (usar IAM Role é mais seguro para produção)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = "samuelcollegeworkbucket"
    destination_bucket = "samuelcollegeworkbucketdestination"
    new_size = (200, 200)  # Tamanho da imagem redimensionada: 200x200 pixels

    logs = []

    # Itera pelos registros do evento (simulados ou reais)
    for record in event['Records']:
        # Corrigindo o acesso à chave: ela vem no campo "key"
        object_key = record['s3']['object']['key']

        try:
            print(f"[{datetime.now()}] Baixando {object_key} do bucket {source_bucket}")
            # Baixa a imagem do bucket de origem
            response = s3.get_object(Bucket=source_bucket, Key=object_key)
            image = Image.open(io.BytesIO(response['Body'].read()))

            # Redimensiona a imagem
            image = image.resize(new_size)

            # Salva a nova imagem em um buffer em memória
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)

            # Define o nome do novo objeto
            new_key = f"resized-{object_key}"
            print(f"[{datetime.now()}] Enviando {new_key} para {destination_bucket}")
            # Envia a imagem redimensionada para o bucket de destino
            s3.put_object(
                Bucket=destination_bucket,
                Key=new_key,
                Body=buffer,
                ContentType="image/jpeg"
            )

            msg = f"Imagem {object_key} redimensionada e salva como {new_key}"
            print(msg)
            logs.append(msg)

        except Exception as e:
            msg = f"Erro ao processar {object_key}: {str(e)}"
            print(msg)
            logs.append(msg)

    return {
        "status": "finalizado",
        "detalhes": logs
    }

# Para testes locais, você pode incluir o seguinte bloco:
if __name__ == "__main__":
    # Evento simulado: altere "imagem.jpg" para o nome de um arquivo que exista no seu bucket de origem
    test_event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": "imagem.jpg"
                    }
                }
            }
        ]
    }
    resultado = lambda_handler(test_event, None)
    print("Resultado:", resultado)

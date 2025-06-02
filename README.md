# AWS Lambda - Redimensionador de Imagens

## 📌 Visão Geral
Essa função **AWS Lambda** processa imagens enviadas para um **bucket S3**, redimensiona para **200x200 pixels**, e armazena a versão editada em outro **bucket de destino**. O código usa a biblioteca **Pillow** para manipulação de imagens.

---

## 🚀 Tecnologias Utilizadas
- **AWS Lambda** - Execução serverless
- **Amazon S3** - Armazenamento de objetos
- **Boto3** - SDK para AWS em Python
- **Pillow (PIL)** - Processamento de imagens
- **Logging** - Rastreamento de execução

---

## 🛠️ Configuração
Antes de utilizar esse código, certifique-se de:
- Ter permissões apropriadas no AWS IAM.
- Criar os **buckets S3** (`samuelcollegeworkbucket` e `samuelcollegeworkbucketdestination`).
- Definir permissões de **leitura/escrita** para o Lambda acessar os buckets.

---

## 🔄 Fluxo de Execução
1. O evento do **Amazon S3** aciona a função Lambda quando um objeto é enviado.
2. A função baixa a **imagem original** do bucket de origem.
3. Redimensiona a imagem para **200x200 pixels** usando **Pillow**.
4. A imagem processada é armazenada no **bucket de destino** com o prefixo `"resized-"`.

---

## 🔧 Estrutura do Código

```python
import boto3
import io
from PIL import Image
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = "samuelcollegeworkbucket"
    destination_bucket = "samuelcollegeworkbucketdestination"
    new_size = (200, 200)

    logs = []

    for record in event['Records']:
        object_key = record['s3']['object']['key']

        try:
            response = s3.get_object(Bucket=source_bucket, Key=object_key)
            image = Image.open(io.BytesIO(response['Body'].read()))

            image = image.resize(new_size)

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)

            new_key = f"resized-{object_key}"
            s3.put_object(
                Bucket=destination_bucket,
                Key=new_key,
                Body=buffer,
                ContentType="image/jpeg"
            )

            logs.append(f"Imagem {object_key} redimensionada e salva como {new_key}")

        except Exception as e:
            logs.append(f"Erro ao processar {object_key}: {str(e)}")

    return {
        "status": "finalizado",
        "detalhes": logs
    }
🧪 Testes Locais
Para testar fora da AWS, utilize o seguinte código:

python
if __name__ == "__main__":
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
```

⚠️ Considerações de Segurança
IAM Role: Evite credenciais hardcoded, utilize permissões IAM seguras.

Validação de Imagens: Certifique-se de validar o formato do arquivo antes do processamento.

Logging: O uso de logs detalhados pode ajudar na depuração.

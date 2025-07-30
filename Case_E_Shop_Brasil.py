{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyN2OrJkEqv58M1lAHh4yguF",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/erickalmeiida/Case---Advances-databases/blob/main/Case_E_Shop_Brasil.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "kEAFb167q9Nu",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "9621d1a7-3963-4932-c88a-c632688ea42c"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m33.9/33.9 MB\u001b[0m \u001b[31m32.6 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m1.9/1.9 MB\u001b[0m \u001b[31m34.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ],
      "source": [
        "!pip install mysql-connector-python faker matplotlib seaborn -q"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install pymongo -q"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "xSpQOMkTQk4_",
        "outputId": "c6774e81-d7a1-4b25-e5af-3bd56fe3f33a"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/1.4 MB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[91m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[90m╺\u001b[0m\u001b[90m━━━\u001b[0m \u001b[32m1.3/1.4 MB\u001b[0m \u001b[31m38.5 MB/s\u001b[0m eta \u001b[36m0:00:01\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m1.4/1.4 MB\u001b[0m \u001b[31m25.6 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h\u001b[?25l   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m0.0/313.6 kB\u001b[0m \u001b[31m?\u001b[0m eta \u001b[36m-:--:--\u001b[0m\r\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m313.6/313.6 kB\u001b[0m \u001b[31m19.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import mysql.connector\n",
        "from mysql.connector import Error\n",
        "from pymongo import MongoClient\n",
        "from faker import Faker\n",
        "import uuid\n",
        "import random\n",
        "import pandas as pd\n",
        "import seaborn as sns\n",
        "import matplotlib.pyplot as plt\n",
        "from datetime import datetime, timedelta"
      ],
      "metadata": {
        "id": "qAdYPajUQX_Q"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "MYSQL_CONFIG = {\n",
        "    \"host\": \"localhost\",\n",
        "    \"user\": \"root\",\n",
        "    \"password\": \"root\",\n",
        "    \"database\": \"ecommerce\"\n",
        "}\n",
        "\n",
        "MONGODB_CONFIG = {\n",
        "    \"host\": \"localhost\",\n",
        "    \"port\": 27017\n",
        "}\n",
        "\n",
        "MONGODB_DB = \"ecommerce\"\n",
        "MONGODB_COLLECTION = \"Pedidos\""
      ],
      "metadata": {
        "id": "-uWj4osYQssu"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def conectar_mysql():\n",
        "    return mysql.connector.connect(**MYSQL_CONFIG)"
      ],
      "metadata": {
        "id": "o9GuV6UJRh21"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def conectar_mongo():\n",
        "    client = MongoClient(MONGODB_URI)\n",
        "    return client[MONGODB_DB][MONGODB_COLLECTION]"
      ],
      "metadata": {
        "id": "pYW7tgoSRk1N"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def criar_tabela_mysql():\n",
        "    try:\n",
        "        conn = mysql.connector.connect(**MYSQL_CONFIG)\n",
        "        cursor = conn.cursor()\n",
        "        cursor.execute(\"\"\"\n",
        "        CREATE TABLE IF NOT EXISTS pedidos (\n",
        "          id VARCHAR(36) PRIMARY KEY,\n",
        "          nome_cliente VARCHAR(100),\n",
        "          data_pedido DATE,\n",
        "          valor_produto DECIMAL(10,2),\n",
        "          categoria (VARCHAR 40),\n",
        "          cidade (VARCHAR 60),\n",
        "          produto (VARCHAR 45)\n",
        "        )\n",
        "        \"\"\")\n",
        "        conn.commit()\n",
        "        print(\"Tabela criada com sucesso\")\n",
        "    except Error as e:\n",
        "        print(\"Não foi possível criar tabela SQL\")"
      ],
      "metadata": {
        "id": "JQpNdgeHSNdN"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def gerar_pedidos(n = 70):\n",
        "  fake = Faker(\"pt_BR\")\n",
        "  categorias = {\n",
        "      \"Escola\": [\"Mochila\", \"Estojo\", \"Caderno\", \"Canetas\", \"Lápis\"],\n",
        "      \"Construção\": [\"Martelo\", \"Serrote\", \"Fita métrica\", \"Chave de fenda\", \"Furadeira\"],\n",
        "      \"Higiene\": [\"Pasta de dente\", \"Escova de dente\", \"Fio dental\"],\n",
        "      \"Eletrodomésicos\": [\"Geladeira\", \"Fogão\", \"Máquina de lavar\", \"Micro-ondas\"],\n",
        "      \"Eletrônicos\": [\"Smartphone\", \"Tablet\", \"Notebook\", \"Câmera digital\"],\n",
        "      \"Moda\": [\"Camiseta\", \"Calça\", \"Saia\", \"Meia\", \"Bolsa\"],\n",
        "  }\n",
        "  cidades = [\"Cuiabá\", \"São Luís\", \"Rio Branco\", \"Florianópolis\", \"São Paulo\", \"Curitiba\", \"Vitória\"]\n",
        "\n",
        "  pedidos = []\n",
        "  for _ in range(n):\n",
        "    categoria = random.choice(list(categorias.keys()))\n",
        "    produto = random.choice(categorias[categoria])\n",
        "    pedido = {\n",
        "        \"id_pedido\": str(uuid.uuid4()),\n",
        "        \"nome_cliente\": fake.name(),\n",
        "        \"produto\": produto,\n",
        "        \"categoria\": categoria,\n",
        "        \"cidade\": random.choice(cidades),\n",
        "        \"valor_produto\": round(random.uniform(10, 1000), 2),\n",
        "        \"data_pedido\": datetime.now() - timedelta(days=random.randint(1, 30)).date()\n",
        "    }\n",
        "    pedidos.append(pedido)\n",
        "  return pedidos"
      ],
      "metadata": {
        "id": "-NLn4AY_UCHm"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def inserir_pedidos_mysql(pedidos):\n",
        "    try:\n",
        "        conn = mysql.connector.connect(**MYSQL_CONFIG)\n",
        "        cursor = conn.cursor()\n",
        "        sql = \"\"\"\n",
        "        INSERT INTO pedidos (id, nome_cliente, data_pedido, valor_produto, categoria, cidade, produto)\n",
        "        VALUES (%s, %s, %s, %s, %s, %s, %s)\n",
        "        \"\"\"\n",
        "        data = [(pedido[\"id_pedido\"], pedido[\"nome_cliente\"], pedido[\"data_pedido\"], pedido[\"valor_produto\"], pedido[\"categoria\"], pedido[\"cidade\"], pedido[\"produto\"]) for pedido in pedidos]\n",
        "        cursor.executemany(sql, data)\n",
        "        conn.commit()\n",
        "        print(\"Pedidos inseridos com sucesso\")\n",
        "        cursor.close()\n",
        "        conn.close()\n",
        "    except Error as e:\n",
        "        print(\"Não foi possível inserir pedidos\")"
      ],
      "metadata": {
        "id": "0hb_hivTl7AF"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def inserir_pedidos_mongodb(pedidos):\n",
        "    try:\n",
        "        client = MongoClient(MONGODB_URI)\n",
        "        db = client[MONGODB_DB]\n",
        "        collection = db[MONGODB_COLLECTION]\n",
        "        collection.insert_many(pedidos)\n",
        "        print(\"Pedidos inseridos no MongoDB\")\n",
        "    except Exception as e:\n",
        "        print(\"Não foi possível inserir pedidos no MongoDB\")"
      ],
      "metadata": {
        "id": "_ZV-0dron1iU"
      },
      "execution_count": 1,
      "outputs": []
    }
  ]
}
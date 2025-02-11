from flask import Flask, request, jsonify
import pandas as pd
import ollama
import os

app = Flask(__name__)

csv_path = "jogadores_brasileirao.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")

df = pd.read_csv(csv_path, encoding='utf-8')

def gerar_contexto():
    colunas_relevantes = ["nome", "clube", "posicao", "idade", "gols", "assistencias", "valor de mercado"]
    if not all(col in df.columns for col in colunas_relevantes):
        raise ValueError("O CSV não contém todas as colunas esperadas.")
    
    contexto = df[colunas_relevantes].to_json(orient="records")
    return contexto

@app.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.json
    pergunta = data.get("pergunta")

    if not pergunta:
        return jsonify({"erro": "Pergunta não fornecida"}), 400

    contexto = gerar_contexto()

    try:
        resposta = ollama.chat(
            model="deepseek-r1",
            messages=[
            {"role": "user", "content": "Please reason step by step, and put your final answer within \\boxed{}. You are an expert assistant on Brasileirão players. ANSWER BASED ONLY ON THE PROVIDED DATA. ANSWER ONLY IN ENGLISH. Here is the data of the players:\n\n" + contexto + "\n\n Answer: " + pergunta}
            ],
            options={"temperature": 0.6, "num_ctx": 4096}
        )
        resposta_texto = resposta.get('message', {}).get('content', 'Erro ao gerar resposta.')
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    return jsonify({"resposta": resposta_texto})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

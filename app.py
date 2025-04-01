from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
ARQUIVO_TAREFAS = 'static/tasks.json'

def carregar_tarefas():
    if not os.path.exists(ARQUIVO_TAREFAS):
        return []
    with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_tarefas(tarefas):
    with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)

@app.route('/')
def inicio():
    tarefas = carregar_tarefas()
    total = len(tarefas)
    concluidas = sum(1 for t in tarefas if t['concluida'])
    return render_template('index.html', 
                         tarefas=tarefas,
                         total_tasks=total,
                         completed_tasks=concluidas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nova_tarefa = {
        'id': len(carregar_tarefas()) + 1,
        'texto': request.json.get('texto'),
        'concluida': False
    }
    tarefas = carregar_tarefas()
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    return jsonify({'status': 'sucesso'})

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    tarefas = carregar_tarefas()
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefa['concluida'] = not tarefa['concluida']
            break
    salvar_tarefas(tarefas)
    return jsonify({'status': 'sucesso'})

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    tarefas = [t for t in carregar_tarefas() if t['id'] != id]
    salvar_tarefas(tarefas)
    return jsonify({'status': 'sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
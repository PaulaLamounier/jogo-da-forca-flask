import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'dev' # Necessário para usar sessões

# Lista de palavras (pode ser movida para um arquivo separado, se preferir)
LISTA_PALAVRAS = ['Casa', 'Sol', 'Livro', 'Rua', 'Flor', 'Tatu', 'Caju', 'Lobo', 'Pai', 'Celular']

def inicializar_jogo():
    palavra_secreta = random.choice(LISTA_PALAVRAS).lower()
    session['palavra_secreta'] = palavra_secreta
    session['gabarito_forca'] = ['_' for _ in palavra_secreta]
    session['vidas'] = 10
    session['erros'] = 0
    session['letras_tentadas'] = []
    session['mensagem'] = "Bem-vindo ao Jogo da Forca!"
    session['jogo_terminado'] = False

@app.route('/')
def index():
    if 'palavra_secreta' not in session:
        inicializar_jogo()
    return render_template('index.html',
                           gabarito=session['gabarito_forca'],
                           vidas=session['vidas'],
                           letras_tentadas=session['letras_tentadas'],
                           mensagem=session['mensagem'],
                           jogo_terminado=session['jogo_terminado'],
                           palavra_final=session.get('palavra_secreta', '').capitalize(),
                           erros=session['erros'])

@app.route('/jogar', methods=['POST'])
def jogar():
    if session.get('jogo_terminado'):
        return redirect(url_for('index'))

    letra = request.form['letra'].lower().strip()
    session['mensagem'] = "" # Limpa a mensagem anterior

    if not letra.isalpha() or len(letra) != 1:
        session['mensagem'] = "Entrada inválida. Por favor, digite apenas uma letra."
    elif letra in session['letras_tentadas']:
        session['mensagem'] = "Você já tentou essa letra. Tente outra."
    else:
        session['letras_tentadas'].append(letra)

        if letra in session['palavra_secreta']:
            session['mensagem'] = "Isso aí! Você acertou uma letra."
            for i, char in enumerate(session['palavra_secreta']):
                if char == letra:
                    session['gabarito_forca'][i] = letra
        else:
            session['mensagem'] = "Que pena! Essa letra não está na palavra."
            session['vidas'] -= 1
            session['erros'] += 1

    # Verifica se o jogo terminou
    if '_' not in session['gabarito_forca']:
        session['mensagem'] = f"PARABÉNS! Você venceu! A palavra era '{session['palavra_secreta'].capitalize()}'."
        session['jogo_terminado'] = True
    elif session['vidas'] <= 0:
        session['mensagem'] = f"FIM DE JOGO! Você perdeu. A palavra era '{session['palavra_secreta'].capitalize()}'."
        session['jogo_terminado'] = True

    return redirect(url_for('index'))

@app.route('/reiniciar')
def reiniciar():
    inicializar_jogo()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) # debug=True para desenvolvimento, desative em produção

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
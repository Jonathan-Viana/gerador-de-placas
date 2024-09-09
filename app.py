from flask import Flask, render_template_string, request
import itertools
import string

app = Flask(__name__)

# Função para gerar as possibilidades da placa
def gerar_possibilidades(parte_da_placa):
    letras = string.ascii_uppercase  # Todas as letras de A a Z
    numeros = '0123456789'           # Todos os números de 0 a 9
    
    possibilidades = []
    
    for caractere in parte_da_placa:
        if caractere == '*':
            if len(possibilidades) < 3:  # Os 3 primeiros caracteres são sempre letras
                possibilidades.append(letras)
            elif len(possibilidades) == 4 or len(possibilidades) >= 6:  # 4º, 6º e 7º caracteres são números
                possibilidades.append(numeros)
            else:
                # O 5º caractere pode ser letra ou número
                possibilidades.append(letras + numeros)
        else:
            possibilidades.append(caractere)
    
    todas_as_possibilidades = list(itertools.product(*possibilidades))
    resultado = [''.join(p) for p in todas_as_possibilidades]
    
    return resultado

# Página inicial
@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gerador de Placas</title>
    </head>
    <body>
        <h1>Gerador de Possibilidades de Placas</h1>
        <form action="/resultado" method="POST">
            <label for="parte_da_placa">Digite a parte da placa (use '*' para os caracteres desconhecidos):</label>
            <input type="text" id="parte_da_placa" name="parte_da_placa" maxlength="7" required>
            <button type="submit">Gerar</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html)

# Página de resultado
@app.route('/resultado', methods=['POST'])
def resultado():
    parte_da_placa = request.form['parte_da_placa']
    resultados = gerar_possibilidades(parte_da_placa)
    
    html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resultados da Placa</title>
    </head>
    <body>
        <h1>Possibilidades para a placa '{{ parte_da_placa }}'</h1>
        <ul>
            {% for resultado in resultados %}
                <li>{{ resultado }}</li>
            {% endfor %}
        </ul>
        <a href="/">Gerar outra placa</a>
    </body>
    </html>
    '''
    return render_template_string(html, parte_da_placa=parte_da_placa, resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)

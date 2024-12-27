import tkinter as tk #OFICIAL
from tkinter import messagebox #x**3 - 9*x + 3
import sympy as sp
import numpy as np


# Função de cálculo de raízes
def calcular_raizes(funcao_str):
    try:
        x = sp.symbols('x')
        funcao = sp.sympify(funcao_str)  # Converter string para expressão simbólica
        derivada = sp.diff(funcao, x)  # Calcular derivada da função

        valores_x = np.arange(-10, 10, 0.01)  # Aumentando a resolução para 0.01
        valores_f = avaliar_funcao(funcao, x, valores_x)  # Avaliar f(x)

        intervalos = encontrar_intervalos(valores_x, valores_f)  # Encontrar intervalos de mudança de sinal
        raizes_encontradas = []

        for intervalo in intervalos:
            x_inicial = sum(intervalo) / 2  # Ponto médio do intervalo
            raiz = newton_raphson(funcao, derivada, x_inicial, x)
            if raiz is not None:
                raizes_encontradas.append(raiz)

        return raizes_encontradas, intervalos

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular raízes: {str(e)}")
        return [], []


# Avaliar a função para uma lista de valores de x
def avaliar_funcao(funcao, x, valores):
    f_lambdified = sp.lambdify(x, funcao, "numpy")
    return f_lambdified(valores)


# Encontrar intervalos de mudança de sinal
def encontrar_intervalos(valores_x, valores_f):
    intervalos = []
    for i in range(1, len(valores_x)):
        if valores_f[i - 1] * valores_f[i] < 0:
            intervalo = [valores_x[i - 1], valores_x[i]]
            # Ajustando os limites do intervalo para serem inteiros
            intervalo[0] = np.floor(intervalo[0])
            intervalo[1] = np.ceil(intervalo[1])
            intervalos.append(intervalo)
    return list(set(tuple(intervalo) for intervalo in intervalos))  # Remove duplicatas


# Método de Newton-Raphson adaptado
def newton_raphson(funcao, derivada, x_inicial, x, tolerancia=1e-6, max_iteracoes=100):
    f_lambdified = sp.lambdify(x, funcao, "numpy")
    f_deriv_lambdified = sp.lambdify(x, derivada, "numpy")

    x_atual = x_inicial
    for i in range(max_iteracoes):
        fx = f_lambdified(x_atual)
        fpx = f_deriv_lambdified(x_atual)

        if fpx == 0:
            print(f"Derivada nula. O método falhou na iteração {i}.")
            return None

        # Aplicando a fórmula de Newton-Raphson
        x_proximo = x_atual - fx / fpx

        # Verificar se o valor encontrado é suficientemente próximo de zero
        if abs(f_lambdified(x_proximo)) < tolerancia:
            return x_proximo

        x_atual = x_proximo

    print("Número máximo de iterações atingido.")
    return x_atual


# Função para o botão 'Calcular'
def on_calcular():
    funcao_str = entrada_funcao.get()  # Obter a função do campo de entrada
    raizes, intervalos = calcular_raizes(funcao_str)  # Calcular as raízes e intervalos

    # Exibir intervalos de mudança de sinal
    if intervalos:
        intervalos_texto = "Intervalos de mudança de sinal:\n" + "\n".join(
            [f"[{intervalo[0]}, {intervalo[1]}]" for intervalo in intervalos])
        resultado_intervalos.config(text=intervalos_texto)
    else:
        resultado_intervalos.config(text="Nenhum intervalo de mudança de sinal encontrado")

    # Exibir raízes encontradas
    if raizes:
        resultado = "Raízes encontradas:\n" + "\n".join([f"x{i + 1} = {raiz:.4f}" for i, raiz in enumerate(raizes)])
        resultado_raizes.config(text=resultado)
    else:
        resultado_raizes.config(text="Nenhuma raiz encontrada")


# Configurando a interface gráfica
janela = tk.Tk()
janela.title("Calculadora de Raízes - Método de Newton-Raphson")

# Campo de entrada para a função
tk.Label(janela, text="Digite a função f(x):").pack(pady=10)
entrada_funcao = tk.Entry(janela, width=40)
entrada_funcao.pack(pady=5)

# Botão para calcular as raízes
btn_calcular = tk.Button(janela, text="Calcular Raízes", command=on_calcular)
btn_calcular.pack(pady=10)

# Label para mostrar os intervalos de mudança de sinal
resultado_intervalos = tk.Label(janela, text="Intervalos de mudança de sinal: ")
resultado_intervalos.pack(pady=20)

# Label para mostrar o resultado das raízes
resultado_raizes = tk.Label(janela, text="Raízes encontradas: ")
resultado_raizes.pack(pady=20)

# Iniciar a janela
janela.mainloop()

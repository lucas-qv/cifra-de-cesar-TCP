import json
from socket import *

# Função para verificar se um número é primo
def primo(N):
    i = 2
    while i < N:
        if N % i == 0:
            print(f"{N} não é primo!")
            return False
        i += 1
    print(f"{N} é primo!")
    return True

# Função para aplicar a Cifra de César em um caractere específico
def shift_char(char, shift, alphabet):
    if char in alphabet:
        index = alphabet.index(char)
        shifted_index = (index + shift) % len(alphabet)
        return alphabet[shifted_index]
    return char

# Função para criptografar um texto usando a Cifra de César
def encrypt_cesar(text, shift):
    result = ""
    lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
    upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_accented = "áéíóúàèìòùâêîôûãõäëïöüñç"
    upper_accented = "ÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÄËÏÖÜÑÇ"

    for char in text:
        if char.islower():
            result += shift_char(char, shift, lower_alphabet + lower_accented)
        elif char.isupper():
            result += shift_char(char, shift, upper_alphabet + upper_accented)
        else:
            result += char  # Não modifica caracteres que não são letras
    return result

# Função para descriptografar um texto usando a Cifra de César
def decrypt_cesar(text, shift):
    return encrypt_cesar(text, -shift)  # Inverte o deslocamento para descriptografar

# Função para calcular a chave secreta K2 usando Diffie-Hellman
def diffie_hellman_k2(N, R1, y):
    return (R1 ** y) % N

# Função para coletar e validar um número primo
def get_prime_input(prompt):
    while True:
        value = int(input(prompt))
        if primo(value):
            return value

# Função para configurar e enviar os dados ao servidor
def send_data_to_server(result_json, server_name, server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)  # Cria o socket TCP
    client_socket.connect((server_name, server_port))  # Conecta ao servidor
    client_socket.send(bytes(json.dumps(result_json), "utf-8"))  # Envia os dados JSON
    return client_socket

# Função para receber e processar a resposta do servidor
def receive_and_process_response(client_socket, N, y):
    modified_sentence = client_socket.recv(65000)  # Recebe os dados do servidor
    text = str(modified_sentence, "utf-8")
    text_json = json.loads(text)

    R1 = text_json['R1']  # Valor R1 recebido do servidor
    text = text_json['text']  # Texto criptografado recebido do servidor

    K2 = diffie_hellman_k2(N, R1, y)  # Calcula a chave K2 usando Diffie-Hellman
    descriptografado = decrypt_cesar(text, K2)  # Descriptografa o texto
    print('\n\nDescriptografado: ' + descriptografado)

# Função principal do cliente
def run_client():
    G = get_prime_input("\n\nDigite o G: ")  # Coleta e valida o valor G
    N = get_prime_input("\n\nDigite o N: ")  # Coleta e valida o valor N

    y = 23  # Chave privada do cliente
    text = str(input("\n\nDigite o texto: "))  # Texto a ser criptografado
    R2 = (G ** y) % N  # Calcula R2 usando Diffie-Hellman

    result = encrypt_cesar(text, R2)  # Criptografa o texto usando a Cifra de César
    result_json = {
        'R2': R2,
        'text': result,
        'G': G,
        'N': N
    }

    print('\n\nresultJson:' + json.dumps(result_json) + '\n\n')

    server_name = "10.1.70.2"
    server_port = 1300
    client_socket = send_data_to_server(result_json, server_name, server_port)  # Envia dados ao servidor

    receive_and_process_response(client_socket, N, y)  # Recebe e processa a resposta do servidor

    client_socket.close()  # Fecha a conexão com o servidor

# Executa o cliente
if __name__ == "__main__":
    run_client()

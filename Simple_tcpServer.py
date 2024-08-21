import json
from socket import *

# Chave privada do servidor
x = 5

# Função para calcular o primeiro valor de Diffie-Hellman (R1)
def diffie_hellman_r1(n, g, x):
    return (g ** x) % n  # Calcula R1 = (g^x) % n

# Função para calcular a chave secreta K1 usando Diffie-Hellman
def diffie_hellman_k1(n, R2, x):
    return (R2 ** x) % n  # Calcula K1 = (R2^x) % n

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

# Função para configurar o servidor
def setup_server(port):
    server_socket = socket(AF_INET, SOCK_STREAM)  # Cria um socket TCP
    server_socket.bind(("", port))  # Liga o socket a uma porta específica
    server_socket.listen(5)  # Configura o servidor para ouvir conexões com uma fila máxima de 5
    print("TCP Server iniciado e aguardando conexões...\n")
    return server_socket

# Função para lidar com uma conexão de cliente
def handle_client(connection_socket):
    sentence = connection_socket.recv(65000)  # Recebe dados do cliente (até 65kB)
    received = str(sentence, "utf-8")  # Converte os dados recebidos para string
    print('Sentença recebida: ' + received)

    # Decodifica os dados JSON recebidos
    text_json = json.loads(received)
    R2 = text_json['R2']  # Valor R2 enviado pelo cliente
    text = text_json['text']  # Texto criptografado enviado pelo cliente
    g = text_json['G']  # Base G para Diffie-Hellman
    n = text_json['N']  # Módulo N para Diffie-Hellman

    # Calcula R1 e K1 usando Diffie-Hellman
    R1 = diffie_hellman_r1(n, g, x)
    K1 = diffie_hellman_k1(n, R2, x)

    # Descriptografa o texto recebido usando a cifra de César com a chave R2
    descriptografado = decrypt_cesar(text, R2)
    descriptografado_upper = descriptografado.upper()  # Processa o texto (convertendo para maiúsculas)
    print("\n\nTexto descriptografado: ", descriptografado)

    # Criptografa o texto processado usando a cifra de César com a chave K1
    criptografado = encrypt_cesar(descriptografado_upper, K1)

    # Envia o R1 e o texto criptografado de volta para o cliente
    response = json.dumps({'R1': R1, 'text': criptografado})
    connection_socket.send(bytes(response, "utf-8"))
    print("\n\nResposta enviada ao cliente: ", response)

# Função principal do servidor
def run_server(port):
    server_socket = setup_server(port)
    while True:
        try:
            connection_socket, addr = server_socket.accept()
            handle_client(connection_socket)
        except timeout:
            print("Timeout do servidor atingido. Encerrando servidor.")
            break
        except KeyboardInterrupt:
            print("Servidor interrompido manualmente.")
            break

    server_socket.close()
    print("Servidor encerrado.")

# Inicia o servidor na porta especificada
if __name__ == "__main__":
    run_server(1300)

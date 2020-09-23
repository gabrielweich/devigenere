"""
Author: Gabriel Weich
Date: 23/09/2020
Language: Python 3.7.3
"""


import sys
from typing import List
import itertools
from collections import Counter
from constants import MAX_KEY_SIZE, DICTIONARY, COINCIDENCE_INDEX, FIRST_INDEX

"""
Através do texto cifrado e da chave retorna o texto claro.
"""
def clear_text(message: str, distances: List[int]) -> str:
    text = []
    for c, d in zip(message, itertools.cycle(distances)):
        text.append(chr((ord(c) - FIRST_INDEX - d) % 26 + FIRST_INDEX))
    return ''.join(text)
        

"""
Encontra o valor da chave através da mensagem cifrada e do tamanho da chave
Retorna uma lista com as distâncias encontradas
"""
def find_key_value(message: str, key_length: int) -> List[int]:
    distances = []
    for kindex in range(key_length):
        columns = [message[i] for i in range(kindex, len(message), key_length)]
        options = Counter(columns).most_common(2)
        print(f'1 - Letra {options[0][0]} ({options[0][1]})')
        print(f'2 - Letra {options[1][0]} ({options[1][1]})')
        selected = input('Escolha uma opção para a letra da chave: ')
        final = options[1][0] if selected == '2' else options[0][0]
        dist = ord(final) - FIRST_INDEX
        distances.append(dist)
    print('\nChave: ', ''.join([chr(d + FIRST_INDEX) for d in distances]), '\n')
    return distances


"""
Encontra o tamanho da chave através da mensagem utilizando o Método de Friedman.
"""
def find_key_length(message: str) -> int:
    likely_keys = [float("inf")]*(MAX_KEY_SIZE)
    for ksize in range(1, MAX_KEY_SIZE):
        for start in range(ksize):
            substr = [message[i] for i in range(start, len(message), ksize)]
            cnt = Counter(substr)
            acc = sum(cnt[c]*(cnt[c]-1) for c in DICTIONARY)
            total = len(substr)
            coincidence = acc / (total*(total-1))
            diff = abs(coincidence - COINCIDENCE_INDEX)
            likely_keys[ksize] = min(likely_keys[ksize], diff)

    return likely_keys.index(min(likely_keys))


"""
Lê o arquivo no caminho passado por parâmetro e executa as funções responsáveis por
encontrar o tamanho da chave, encontrar o valor da chave e descriptografar o texto.
"""
def decrypt(filepath: str) -> None:
    file = open(filepath)
    message = file.readline().upper()
    key_length = find_key_length(message)
    print("Tamanho da chave: ", key_length, '\n')
    distances = find_key_value(message, key_length)
    print(clear_text(message, distances))
    file.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python decrypt <caminho do arquivo>')
        exit(1)

    decrypt(sys.argv[1])
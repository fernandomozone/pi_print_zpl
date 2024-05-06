import socket
from datetime import datetime

def criar_comando_zpl(data, hora, codigo_barras):
    zpl = f"""
    ^XA
    ^CF0,68
    ^PW800
    ^LL400
    ^FO50,70^FDData: ^FS
    ^FO50,170^FDHora: ^FS
    ^FO200,70^FH^FD{data}^FS
    ^FO200,170^FH^FD{hora}^FS
    ^BY2,3,60^FO50,250^B3N,N,100,Y,N^FD1234567^FS
    ^XZ
    """
    return zpl

def enviar_para_impressora(ip, port, dados):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(dados.encode('utf-8'))

def ler_codigo_barras():
    codigo = input("Aguardando leitura do cÃ³digo de barras: ")
    return codigo

def imprimir_etiqueta(ip='10.1.30.106', port=9100):
    while True:  # Loop infinito
        # Aguardar a leitura do cÃ³digo de barras
        codigo_barras = ler_codigo_barras()
        
        # Verificar se o cÃ³digo de barras tem exatamente 7 dÃ­gitos
        if len(codigo_barras) == 7:
            print(f"CÃ³digo de barras lido: {codigo_barras}")

            # Obter a data e hora atual formatada
            data_atual = datetime.now().strftime('%d/%m/%Y')
            hora_atual = datetime.now().strftime('%H:%M:%S')
            
            # Criar o comando ZPL incluindo a data, hora e o cÃ³digo de barras
            comando_zpl = criar_comando_zpl(data_atual, hora_atual, codigo_barras)
            
            # Enviar o comando ZPL para a impressora
            enviar_para_impressora(ip, port, comando_zpl)
            print("Etiqueta enviada para impressÃ£o.")
        else:
            print("CÃ³digo de barras incompleto. Por favor, escaneie novamente.")

if __name__ == '__main__':
    imprimir_etiqueta()

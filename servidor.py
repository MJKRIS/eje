from socket import socket, error

import nacl.utils
from nacl.public import PrivateKey, SealedBox
import getpass

skfile = PrivateKey.generate()
pkfile = skfile.public_key

sealed_box = SealedBox(pkfile)

def main():
    s = socket()
    
    #puerto 6030
    s.bind(("localhost", 6030))
    s.listen(0)
    
    conn, addr = s.accept()
    f = open("captura-recibido.png", "wb")
    
    while True:
        try:
            input_data = conn.recv(1024)
        except error:
            print("Error")
            break
        else:
            if input_data:
                if isinstance(input_data, bytes):
                    end = input_data[0] == 1
                else:
                    end = input_data == chr(1)
                if not end:
                    # Almacenar datos.
                    encrypted = sealed_box.encrypt(input_data)
                    f.write(encrypted)
                else:
                    break
    
    print("Exito")
    f.close()

if __name__ == "__main__":
    main()

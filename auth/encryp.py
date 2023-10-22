import math

def encryp(key,pwd):
    # key="10001&94dd2a8675fb779e6b9f7103698634cd400f27a154afa67af6166a43fc26417222a79506d34cacc7641946abda1785b7acf9910ad6a0978c91ec84d40b71d2891379af19ffb333e7517e390bd26ac312fe940c340466b4a5d4af1d65c3b5944078f96a1a51a5a53e4bc302818b7c9f63c4a1b07bd7d874cef1c3d4b2f5eb7871"
    split=key.split("&")
    publicKeyExponent=split[0]
    publicKeyModulus=split[1]

    m = int.from_bytes(bytearray.fromhex(publicKeyModulus), byteorder='big')
    e = int.from_bytes(bytearray.fromhex('0'+publicKeyExponent), byteorder='big')
    # js加密为反向，为保持一致原文应反向处理，所以这里原文实际为204dowls
    plaintext = f'{pwd}'.encode('utf-8')
    # 无填充加密逻辑
    input_nr = int.from_bytes(plaintext, byteorder='big')
    crypted_nr = pow(input_nr, e, m)
    keylength = math.ceil(m.bit_length() / 8)
    crypted_data = crypted_nr.to_bytes(keylength, byteorder='big')
    # print(crypted_data.hex())
    return crypted_data.hex()
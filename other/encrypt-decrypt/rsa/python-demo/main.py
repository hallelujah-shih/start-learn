import io
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


public_key_path = "../public_key.pem"
private_key_path = "../private_key.pem"


def encrypt(message, rsa_public_key):
    buf = io.BytesIO()
    message = message.encode()
    max_block_len = int(rsa_public_key.size() / 8) - 11

    cipher = PKCS1_v1_5.new(rsa_public_key)
    for i in range(0, len(message), max_block_len):
        buf.write(cipher.encrypt(message[i:i+max_block_len]))
    return base64.b64encode(buf.getvalue())


def decrypt(secret_message, rsa_private_key):
    buf = io.BytesIO()
    max_block_len = int((rsa_private_key.size()+1)/8)
    cipher = PKCS1_v1_5.new(rsa_private_key)
    secret_message = base64.b64decode(secret_message)
    for i in range(0, len(secret_message), max_block_len):
        buf.write(cipher.decrypt(secret_message[i:i+max_block_len], "decrypt_error"))
    return buf.getvalue()


if __name__ == "__main__":
    plain = 'message' * 1024 * 3
    with open(public_key_path) as pub_f, open(private_key_path) as priv_f:
        pub_key = RSA.importKey(pub_f.read())
        priv_key = RSA.importKey(priv_f.read())

    print('raw_msg_len：', len(plain))
    secret = encrypt(plain, pub_key)
    print('secret_msg_len：', len(secret))
    text = decrypt(secret, priv_key)
    print('decrypt_msg_len：', len(text))
    assert plain.encode() == text

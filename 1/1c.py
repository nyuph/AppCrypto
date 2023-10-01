def affine_encrypt(plaintext, a, b):
    result = []
    for char in plaintext:
        offset = 65 if char.isupper() else 97
        result.append(chr(((a * (ord(char) - offset) + b) % 26) + offset))
    return ''.join(result)

if __name__ == "__main__":
    a=5
    b=9
    print(affine_encrypt("CRYPTOISFUN",a,b))
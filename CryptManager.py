class CryptManager:
    HASH = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'

    def cryptPassword(self, hashKey, clave):
        # type: (str, str) -> str
        encriptado = "#1"

        for i in range(len(clave)):
            caracterClave = ord(clave[i])
            caracterKey = ord(hashKey[i])

            APass = caracterClave / 16
            AKey = caracterClave % 16

            pos1 = (APass + caracterKey) % len(self.HASH)
            pos2 = (AKey + caracterKey) % len(self.HASH)

            encriptado += self.HASH[pos1] + self.HASH[pos2]

        return encriptado

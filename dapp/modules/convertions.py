class Convertions:
    @staticmethod
    def str2hex(string):
        """
        Encode a string as an hex string
        """
        return Convertions.binary2hex(Convertions.str2binary(string))

    @staticmethod
    def str2binary(string):
        """
        Encode a string as an binary string
        """
        return string.encode("utf-8")
    
    @staticmethod
    def binary2str(binary):
        """
        Decode a binary string into a regular string
        """
        return binary.decode("utf-8")

    @staticmethod
    def binary2hex(binary):
        """
        Encode a binary as an hex string
        """
        return "0x" + binary.hex()

    @staticmethod
    def hex2binary(hexstr):
        """
        Decodes a hex string into a regular byte string
        """
        return bytes.fromhex(hexstr[2:])

    @staticmethod
    def hex2str(hexstr):
        """
        Decodes a hex string into a regular string
        """
        return Convertions.hex2binary(hexstr).decode("utf-8")

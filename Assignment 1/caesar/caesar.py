from abc import ABC, abstractmethod


class CaesarEncryptor(ABC):
    def __init__(self, step):
        """constructor

        Args:
            step (int): number of steps that a character will be shifted
        """
        self._step = step
        self._setModulo()

    @abstractmethod
    def _setModulo(self):
        """set modulo for caesar encryptor. This should be equal to the length of the dictionary in use
        For example, for basic caesar encryptor, the modulo should be 26 since the set of possible inputs
        to it is lowercase-only (or uppercase-only) alphabets.
        """
        pass

    @abstractmethod
    def _encryptCharacter(self, letter):
        """encrypt one character

        Args:
            letter (char): a character to be encrypted

        Returns:
            encrypted_letter (char): encrypted character
        """
        pass

    @abstractmethod
    def _decryptCharacter(self, letter):
        """decrypt one character

        Args:
            letter (char): a character to be decrypted

        Returns:
            decrypted_letter (char): decrypted character
        """
        pass

    def encrypt(self, msg):
        return ''.join(map(self._encryptCharacter, msg))

    def decrypt(self, msg):
        return ''.join(map(self._decryptCharacter, msg))


class BasicCaesarEncryptor(CaesarEncryptor):
    def __init__(self, step):
        super().__init__(step)

    def _setModulo(self):
        self.__load_dictionary()
        self._modulo = len(self.__dict)

    def __load_dictionary(self):
        """load all possible characters (lowercase a-z)
        """
        with open("dict.txt", "r") as f:
            self.__dict = f.read().split(",")

            # a dictionary converting character to relevant index in the dictionary (the order is zero-based).
            # For example, 'a' is in 0 position.
            self.__char2index = {char: index for index,
                                 char in enumerate(self.__dict)}

    def _encryptCharacter(self, letter):
        # character will be encrypted if it is in dictionary, and be ignored otherwise.
        return self.__dict[(self.__char2index[letter] + self._step) % self._modulo] if ord('a') <= ord(letter) <= ord('z') else letter

    def _decryptCharacter(self, letter):
        # character will be decrypted if it is in dictionary, and be ignored otherwise.
        return self.__dict[(self.__char2index[letter] - self._step) % self._modulo] if ord('a') <= ord(letter) <= ord('z') else letter


class ExtendedCaesarEncryptor(CaesarEncryptor):
    def __init__(self, step):
        super().__init__(step)

    def _setModulo(self):
        # the set of all possible input based on ascii table
        self._modulo = 0x110000

    def _encryptCharacter(self, letter):
        return chr((ord(letter) + self._step) % self._modulo)

    def _decryptCharacter(self, letter):
        return chr((ord(letter) - self._step) % self._modulo)


if __name__ == "__main__":
    encryptor = ExtendedCaesarEncryptor(step=2)
    # # comment out the following line to try orginal caesar cipher
    # encryptor = BasicCaesarEncryptor(step=2)
    print(encryptor.encrypt("h3ll0"))
    print(encryptor.decrypt(encryptor.encrypt("h3ll0")))

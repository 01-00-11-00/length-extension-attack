# ---------------------------- Libraries --------------------------- #
from tqdm import tqdm


# ---------------------------- Classes ------------------------------- #
class LengthExtensionAttack:

    def __init__(self, hash_function):
        self.hash_function = hash_function

    def perform_attack(self, hash_value: str, old_message: str, new_data: str) -> tuple[str, str] or tuple[None, None]:
        """
        Performs a length extension attack on a given hash value. It tries to find a previous state of the hash function
        that would result in the given hash value, then appends new data to the old message and calculates a new hash value.
        :param hash_value: The hash value to perform the attack on.
        :param old_message: The original message that was hashed to get the hash value.
        :param new_data: The new data to append to the old message.
        :return: A tuple containing the new message and the new hash value, or None if the attack was not successful.
        """

        print(f"Performing a length extension attack on the hash value: {hash_value}\n")

        found_state = self.__find_previous_state(hash_value)

        if found_state is not None:

            self.hash_function.set_initial_state(found_state)
            new_message = old_message + new_data
            new_hash = self.hash_function.hash(new_data)

            print("Attack successful!")
            print(f"New message: {new_message}\nNew hash: {new_hash}\n")

            return new_message, new_hash

        else:
            print("No previous state found!\nAttack failed!\n")
            return None, None

    def __find_previous_state(self, hash_value: str) -> int or None:
        """
        Tries to find a possible previous state of the hash function that would result in the given hash value.
        :param hash_value: The hash value to find the previous state for.
        :return: The found previous state as an integer, or None if no previous state was found.
        """

        max_value = 0xffffffff

        for i in tqdm(range(max_value), desc="Testing values"):

            new_hash = self.hash_function.hash_q(i)

            if new_hash == int(hash_value, 16):
                print(f"Found a possible previous state: {hex(i)}\n")
                return i

        return None

    def test(self):
        """
        Tests the perform_attack method with some predefined values and prints whether the tests passed or failed.
        """

        print("Testing the length extension attack...\n")

        try:
            assert self.perform_attack("632e4e5c", "abcd", "ef") == ("abcdef", "0f6b8802")
            assert self.perform_attack("632e4e5c", "abcd", "efghijk") == ("abcdefghijk", "2638a819")

            print("All tests passed successfully!\n")

        except AssertionError as e:
            print(e)
            print("Tests failed!")


class Hash:

    # Properties
    def __init__(self, internal_state=0x524f464c):
        self.internal_state = internal_state

    # Methods
    def set_initial_state(self, state: int):
        """
        Sets the initial internal state of the hash function.
        :param state: The initial internal state as an integer.
        """

        self.internal_state = state

    @staticmethod
    def __split_into_blocks(message, block_size=8) -> list[int]:
        """
        Converts the input message into a hexadecimal string, pads it with "f" until its length is a multiple of the block size,
        and then splits it into blocks of the specified size. Returns a list of these blocks as integers.
        :param message: The input message as a string.
        :param block_size: The size of each block. Default is 8.
        :return: A list of blocks as integers.
        """

        hex_message = message.encode('utf-8').hex()

        while len(hex_message) % block_size != 0:
            hex_message += "f"

        blocks = [int(hex_message[i:i + block_size], 16) for i in range(0, len(hex_message), block_size)]

        return blocks

    @staticmethod
    def __rotate_left(val: int, r_bits, max_bits) -> int:
        """
        Performs a left bitwise rotation on a given value.
        :param val: The value to rotate as a number.
        :param r_bits: The number of bits to rotate by.
        :param max_bits: The maximum number of bits in the value.
        :return: The rotated value as a number.
        """

        return ((val << r_bits) | (val >> (max_bits - r_bits))) & 0xFFFFFFFF

    def hash_q(self, data: int) -> int:
        """
        Performs a bitwise XOR operation on the input data and the result of a left bitwise rotation of the data.
        :param data: The input data as an integer.
        :return: The result of the XOR operation as an integer.
        """
        result = data ^ self.__rotate_left(data, 17, 32)
        return result

    def hash(self, message: str) -> str:
        """
        Splits the input message into blocks, performs the __hash_q operation on each block and the current internal_state,
        and then performs the __hash_q operation on the final internal_state. Returns the result as a hexadecimal string.
        :param message: The input message as a string.
        :return: The result of the hash operation as a hexadecimal string.
        """

        data = self.__split_into_blocks(message)
        internal_state = self.internal_state

        if len(data) != 0:
            for block in data:
                internal_state = self.hash_q(internal_state ^ block)

            result = self.hash_q(internal_state)

            return format(result, "08x")

        else:
            result = self.hash_q(internal_state)

            return format(result, "08x")

    def test(self):
        """
        Tests the hash and __hash_q methods with some predefined values and prints whether the tests passed or failed.
        """

        print("Testing the hash function...")

        try:
            assert hex(self.hash_q(self.internal_state)) == "0xded7e2d2"
            print("Test 1 successful!")
            assert hex(self.hash_q(self.hash_q(self.internal_state))) == "0x1b725f7d"
            print("Test 2 successful!")
            assert hex(self.hash_q(self.hash_q(self.hash_q(self.internal_state)))) == "0xa5886999"
            print("Test 3 successful!")

            assert self.hash("") == "ded7e2d2"
            print("Test 4 successful!")
            assert self.hash("A") == "5d725f7f"
            print("Test 5 successful!")
            assert self.hash("AB") == "5f3b5f7f"
            print("Test 6 successful!")
            assert self.hash("ABC") == "5f39137f"
            print("Test 7 successful!")
            assert self.hash("ABCD") == "5f391128"
            print("Test 8 successful!")
            assert self.hash("ABCDE") == "2f69af58"
            print("Test 9 successful!\n")

            print("All tests passed successfully!\n")

        except AssertionError as e:
            print(e)
            print("Tests failed!\n")


# ---------------------------- Functions ------------------------------- #

def main():
    """
    Main function of the program.
    :return: None
    """

    # Variables
    my_hash = Hash()
    my_attack = LengthExtensionAttack(Hash())

    # Body
    print()
    my_hash.test()
    print()
    my_attack.test()


# ------------------------------ Main ---------------------------------- #

if __name__ == "__main__":
    main()

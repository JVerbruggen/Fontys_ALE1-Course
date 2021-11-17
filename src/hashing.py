import math

class Hashing:
    hexadecimals = [str(i) for i in range(10)] + ['A', 'B', 'C', 'D', 'E', 'F']

    def get_hash(binary_string: str) -> str:
        binary_string = binary_string[::-1]
        binary_grouped = [binary_string[(i*4):((i+1)*4)] for i in range(math.ceil(len(binary_string)/4))]
        
        hash = ""
        for i in range(len(binary_grouped)):
            binary_group = binary_grouped[i]

            decimal = 0
            for j in range(len(binary_group)):
                bit = binary_group[j]
                if bit == "1": decimal += (2**j)
            hash = Hashing.hexadecimals[decimal] + hash

        return hash
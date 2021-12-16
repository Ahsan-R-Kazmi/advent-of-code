from typing import Dict, Tuple, List

HEX_BINARY_DICT: Dict[str, str] = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


def process_literal_value(start_position: int, binary_str: str) -> Tuple[int, int]:

    literal_str: str = ""
    i = start_position

    while True:
        prev_i = i
        i += 5
        chunk = binary_str[prev_i:prev_i+5]
        literal_str += chunk[1:5]
        if chunk[0] == "0":
            break

    return i, int(literal_str, 2)


def process_operator_packet():
    a = 1


def process_packet(start_position: int, binary_str: str) -> Tuple[int, int, int]:

    i = start_position

    if i >= len(binary_str) or int(binary_str[i:-1], 2) == 0:
        return -1, 0, 0

    current_version = int(binary_str[i:i+3], 2)
    i += 3
    type_id = int(binary_str[i:i+3], 2)
    i += 3
    if type_id == 4:
        i, total_value = process_literal_value(i, binary_str)
    else:
        length_type_id = int(binary_str[i:i+1], 2)
        i += 1
        results: List[Tuple[int, int, int]] = []
        if length_type_id == 0:
            length = int(binary_str[i:i+15], 2)
            i += 15
            j = i
            while i < j + length:
                i, version, value = process_packet(i, binary_str)
                if i < 0:
                    break
                results.append((i, version, value))
        else:
            number_of_subpackets = int(binary_str[i:i+11], 2)
            i += 11
            while len(results) < number_of_subpackets:
                i, version, value = process_packet(i, binary_str)
                if i < 0:
                    break

                results.append((i, version, value))

        total_value = results[0][2]
        for k in range(1, len(results)):
            value = results[k][2]
            if type_id == 0:
                total_value += value
            elif type_id == 1:
                total_value *= value
            elif type_id == 2:
                total_value = min(total_value, value)
            elif type_id == 3:
                total_value = max(total_value, value)

        if type_id == 5:
            total_value = 1 if results[0][2] > results[1][2] else 0
        elif type_id == 6:
            total_value = 1 if results[0][2] < results[1][2] else 0
        elif type_id == 7:
            total_value = 1 if results[0][2] == results[1][2] else 0

        for result in results:
            current_version += result[1]

    return i, current_version, total_value


def convert_hex_packet_to_binary_packet(hex_str: str) -> str:
    binary_str = ""
    for i in range(len(hex_str)):
        binary_str += HEX_BINARY_DICT.get(hex_str[i])

    return binary_str


def evaluate_packet(hex_str: str) -> Tuple[int, int, int]:
    binary_str: str = convert_hex_packet_to_binary_packet(hex_str)
    return process_packet(0, binary_str)


if __name__ == '__main__':
    print("ending position, version sum, final value",
          evaluate_packet("A20D6CE8F00033925A95338B6549C0149E3398DE75817200992531E25F005A18C8C8C0001849FDD43629C293004B"
                          "001059363936796973BF3699CFF4C6C0068C9D72A1231C339802519F001029C2B9C29700B2573962930298B6B524"
                          "893ABCCEC2BCD681CC010D005E104EFC7246F5EE7328C22C8400424C2538039239F720E3339940263A98029600A8"
                          "0021B1FE34C69100760B41C86D290A8E180256009C9639896A66533E459148200D5AC0149D4E9AACEF0F66B42696"
                          "194031F000BCE7002D80A8D60277DC00B20227C807E8001CE0C00A7002DC00F300208044E000E69C00B000974C00"
                          "C1003DC0089B90C1006F5E009CFC87E7E43F3FBADE77BE14C8032C9350D005662754F9BDFA32D881004B12B1964D"
                          "7000B689B03254564414C016B004A6D3A6BD0DC61E2C95C6E798EA8A4600B5006EC0008542D8690B80010D89F146"
                          "1B4F535296B6B305A7A4264029580021D1122146900043A0EC7884200085C598CF064C0129CFD8868024592FEE9D"
                          "7692FEE9D735009E6BBECE0826842730CD250EEA49AA00C4F4B9C9D36D925195A52C4C362EB8043359AE221733DB"
                          "4B14D9DCE6636ECE48132E040182D802F30AF22F131087EDD9A20804D27BEFF3FD16C8F53A5B599F4866A78D7898"
                          "C0139418D00424EBB459915200C0BC01098B527C99F4EB54CF0450014A95863BDD3508038600F44C8B90A0801098"
                          "F91463D1803D07634433200AB68015299EBF4CF5F27F05C600DCEBCCE3A48BC1008B1801AA0803F0CA1AC6200043"
                          "A2C4558A710E364CC2D14920041E7C9A7040402E987492DE5327CF66A6A93F8CFB4BE60096006E20008543A83307"
                          "80010E8931C20DCF4BFF13000A424711C4FB32999EE33351500A66E8492F185AB32091F1841C91BE2FDC53C4E801"
                          "20C8C67EA7734D2448891804B2819245334372CBB0F080480E00D4C0010E82F102360803B1FA2146D963C300BA69"
                          "6A694A501E589A6C80"))

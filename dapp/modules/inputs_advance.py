from modules.convertions import Convertions


class InputsAdvance:
    @staticmethod
    def decode_verifier_input(binary) -> dict:
        function_signature = binary[:4]
        real_world_data = binary[4:]
        verifier_data = {
            "msg_sig": Convertions.binary2hex(function_signature),
            "real_world_data": Convertions.binary2str(real_world_data),
        }
        return verifier_data

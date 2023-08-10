import logging
from modules.convertions import Convertions

logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)

class InputsAdvance:
    @staticmethod
    def decode_default_input(binary) -> dict:
        logger.info("Default input")
        return {"data": binary}

    @staticmethod
    def decode_erc20(binary) -> dict:
        ret = binary[:1]
        token_address = binary[1:21]
        depositor = binary[21:41]
        amount = int.from_bytes(binary[41:73], "big")
        data = binary[73:]
        erc20_deposit = {
            "depositor": Convertions.binary2hex(depositor),
            "token_address": Convertions.binary2hex(token_address),
            "amount": amount,
            "data": data
        }
        logger.info(erc20_deposit)
        return erc20_deposit

    @staticmethod
    def decode_erc721(binary) -> dict:
        token_address = binary[:20]
        depositor = binary[20:40]
        token_id = int.from_bytes(binary[40:72], "big")
        data = binary[72:]
        erc721_deposit = {
            "token_address": Convertions.binary2hex(token_address),
            "depositor": Convertions.binary2hex(depositor),
            "token_id": token_id,
            "data": data,
        }
        logger.info(erc721_deposit)
        return erc721_deposit

    @staticmethod
    def decode_ether(binary) -> dict:
        depositor = binary[:20]
        amount = int.from_bytes(binary[20:52], "big")
        data = binary[52:]
        ether_deposit = {
            "depositor": Convertions.binary2hex(depositor),
            "amount": amount,
            "data": data
        }
        logger.info(ether_deposit)
        return ether_deposit
    
    @staticmethod
    def decode_verifier_input(binary) -> dict:
        function_signature = binary[:4]
        real_world_data = binary[4:]
        verifier_data = {
            "msg_sig": Convertions.binary2hex(function_signature),
            "real_world_data": Convertions.binary2str(real_world_data),
        }
        logger.info(verifier_data)
        return verifier_data
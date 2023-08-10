from eth_abi import encode
from modules.convertions import Convertions


class OutputsAdvance:
    @staticmethod
    def create_erc20_transfer_voucher(ERC20_TRANSFER_FUNCTION_SELECTOR, token_address, receiver, amount) -> dict:
        data = encode(['address', 'uint256'], [receiver, amount])
        voucher_payload = Convertions.binary2hex(
            ERC20_TRANSFER_FUNCTION_SELECTOR + data)
        voucher = {"destination": token_address, "payload": voucher_payload}
        return voucher

    @staticmethod
    def create_erc721_safetransfer_voucher(ERC721_SAFETRANSFER_FUNCTION_SELECTOR, token_address, sender, receiver, token_id) -> dict:
        data = encode(['address', 'address', 'uint256'],
                      [sender, receiver, token_id])
        voucher_payload = Convertions.binary2hex(
            ERC721_SAFETRANSFER_FUNCTION_SELECTOR + data)
        voucher = {"destination": token_address, "payload": voucher_payload}
        return voucher

    @staticmethod
    def create_ether_withdrawal_voucher(ETHER_WITHDRAWAL_FUNCTION_SELECTOR, ROLLUP_ADDRESS, receiver, amount) -> dict:
        data = encode(['address', 'uint256'], [receiver, amount])
        voucher_payload = Convertions.binary2hex(
            ETHER_WITHDRAWAL_FUNCTION_SELECTOR + data)
        voucher = {"destination": ROLLUP_ADDRESS, "payload": voucher_payload}
        return voucher

    @staticmethod
    def create_verifier_voucher(INCREASE_ALLOWANCE_FUNCTION_SELECTOR, LILIUM_COMPANY_ADDRESS) -> dict:
        voucher = {"destination": LILIUM_COMPANY_ADDRESS, "payload": Convertions.binary2hex(INCREASE_ALLOWANCE_FUNCTION_SELECTOR)}
        return voucher

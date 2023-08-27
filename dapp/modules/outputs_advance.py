from modules.convertions import Convertions


class OutputsAdvance:
    @staticmethod
    def create_verifier_voucher(INCREASE_ALLOWANCE_FUNCTION_SELECTOR, LILIUM_COMPANY_ADDRESS) -> dict:
        voucher = {"destination": LILIUM_COMPANY_ADDRESS, "payload": Convertions.binary2hex(
            INCREASE_ALLOWANCE_FUNCTION_SELECTOR)}
        return voucher

from modules import Convertions
import logging
import requests


class RollupClient:
    def __init__(self, server_url):
        self.rollup_server = server_url
        self.logger = logging.getLogger(__name__)

    def send_post(self, endpoint, json_data) -> None:
        response = requests.post(
            self.rollup_server + f"/{endpoint}", json=json_data)
        self.logger.info(
            f"/{endpoint}: Received response status {response.status_code} body {response.content}")

    def send_notice(self, notice) -> None:
        self.send_post("notice", notice)

    def send_report(self, report) -> None:
        self.send_post("report", report)

    def send_voucher(self, voucher) -> None:
        self.send_post("voucher", voucher)

    def reject_input(self, input_data) -> None:
        self.send_report({"payload": Convertions.str2hex(input_data)})
        return "reject"

# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import web3
import json
import logging
import requests
import traceback
from os import environ
from ai import ImageVerifier, GaussianEnvelopPredictor
from modules import Convertions, RollupClient, InputsAdvance, OutputsAdvance


GAUSSIAN_ENVELOP = GaussianEnvelopPredictor("./ai/classification_model/model/gaussian_envelop.sav")
IMAGE_VERIFIER = ImageVerifier("./ai/computer_vision/model/object.tflite")

logging.basicConfig(level="INFO")
LOGGER = logging.getLogger(__name__)

ROLLUP_SERVER = environ["ROLLUP_HTTP_SERVER_URL"]
ROLLUP_CLIENT = RollupClient(ROLLUP_SERVER)
LOGGER.info(f"HTTP rollup_server url is {ROLLUP_SERVER}")

NETWORK = environ["NETWORK"]
LOGGER.info(f"NETWORK is {NETWORK}")

w3 = web3.Web3()

networks = json.load(open("networks.json"))

ROLLUP_ADDRESS = None
INPUTBOX_ADDRESS = networks[NETWORK]["INPUTBOX_ADDRESS"].lower()
DAPP_RELAY_ADDRESS = networks[NETWORK]["DAPP_RELAY_ADDRESS"].lower()
LILIUM_COMPANY_ADDRESS = networks[NETWORK]["LILIUM_COMPANY_ADDRESS"].lower()


###
# Selector of functions for solidity <contract>.call(<payload>)
VERIFIER_FUNCTION_SELECTOR = Convertions.hex2binary(w3.keccak(b"verifyRealWorldState(bytes)")[:4].hex())
INCREASE_ALLOWANCE_FUNCTION_SELECTOR = Convertions.hex2binary(w3.keccak(b'increaseAllowance()')[:4].hex())


###
#  Generate Voucher Functions
def process_input_and_generate_verifier_voucher(sender, payload):
    voucher = None
    global REAL_WORLD_STATE
    binary = Convertions.hex2binary(payload)

    if sender == LILIUM_COMPANY_ADDRESS:
        try:
            verifier_input = InputsAdvance.decode_verifier_input(binary)
            msg_sig = verifier_input["msg_sig"][2:]
            real_world_data = json.loads(verifier_input["real_world_data"])
        except Exception as e:
            LOGGER.error(f"Failed to decode verifier input {e}")
            ROLLUP_CLIENT.reject_input(payload)
            return "reject"
        if msg_sig == str(VERIFIER_FUNCTION_SELECTOR.hex()):
            out1 = IMAGE_VERIFIER.verify(real_world_data["base64_image"])
            out2 = GAUSSIAN_ENVELOP.predict(
                real_world_data["temperature"], real_world_data["humidity"], real_world_data["co"])
            if out1 == "Plant" and out2 == [1]:
                REAL_WORLD_STATE = "Sensors compliant with certification."
                voucher = OutputsAdvance.create_verifier_voucher(
                    INCREASE_ALLOWANCE_FUNCTION_SELECTOR, LILIUM_COMPANY_ADDRESS)
            else:
                LOGGER.error(
                    f"Change detected, real world state may have been tampered with {real_world_data}")
                REAL_WORLD_STATE = "Sensors not compliant with certification."
                ROLLUP_CLIENT.reject_input(payload)
                return "reject"
    else:
        pass
    return voucher

###
# handlers
def handle_advance(data):
    global rollup_address
    LOGGER.info(
        f"Received advance request data {data}. Current rollup_address: {rollup_address}")
    try:
        payload = data["payload"]
        voucher = None
        try:
            process_input_and_generate_verifier_voucher(
                data['metadata']['msg_sender'], payload)
        except Exception as e:
            ROLLUP_CLIENT.reject_input(Convertions.binary2str(payload))
            LOGGER.error(f"Failed to decode input {e}")
        if data['metadata']['msg_sender'] == DAPP_RELAY_ADDRESS:
            rollup_address = payload
            ROLLUP_CLIENT.send_notice({"payload": rollup_address})

        if voucher:
            LOGGER.info(f"voucher {voucher}")
            ROLLUP_CLIENT.send_voucher(voucher)

        return "accept"

    except Exception as e:
        msg = f"Error {e} processing data {data}"
        LOGGER.error(f"{msg}\n{traceback.format_exc()}")
        ROLLUP_CLIENT.send_report({"payload": Convertions.str2hex(msg)})
        return "reject"


def handle_inspect(data):
    LOGGER.info(f"Received inspect request data {data}")
    try:
        ROLLUP_CLIENT.send_notice({"payload": Convertions.str2hex(
            f'The real world state is: {REAL_WORLD_STATE}')})
        return "accept"

    except Exception as e:
        msg = f"Error {e} processing data {data}"
        LOGGER.error(f"{msg}\n{traceback.format_exc()}")
        ROLLUP_CLIENT.send_report({"payload": Convertions.str2hex(msg)})
        return "reject"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}


###
# Main Loop
finish = {"status": "accept"}

while True:
    LOGGER.info("Sending finish")
    response = requests.post(ROLLUP_SERVER + "/finish", json=finish)
    LOGGER.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        LOGGER.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])

# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import re
import json
import web3
import base64
from io import BytesIO
import logging
import requests
import traceback
from enum import Enum
from os import environ
from eth_abi import encode
from ai import ImageAnalyzer, GaussianEnvelopPredictor


class REAL_WORLD_STATE(Enum):
    SENSORS_NON_COMPLIANT = 0
    SENSORS_COMPLIANT = 1


GAUSSIAN_ENVELOP = GaussianEnvelopPredictor(
    "./ai/classification_model/model/gaussian_envelop.sav")
IMAGE_ANALYZER = ImageAnalyzer(
    "./ai/computer_vision/model/best_float32.tflite")


STATE = REAL_WORLD_STATE.SENSORS_NON_COMPLIANT


logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

NETWORK = environ["NETWORK"]
logger.info(f"NETWORK is {NETWORK}")

networks = json.load(open("networks.json"))

LILIUM_COMPANY_ADDRESS = networks[NETWORK]["LILIUM_COMPANY_ADDRESS"].lower()

w3 = web3.Web3()


###
# Aux Functions

def str2hex(string):
    """
    Encode a string as an hex string
    """
    return binary2hex(str2binary(string))


def str2binary(string):
    """
    Encode a string as an binary string
    """
    return string.encode("utf-8")


def binary2hex(binary):
    """
    Encode a binary as an hex string
    """
    return "0x" + binary.hex()


def hex2binary(hexstr):
    """
    Decodes a hex string into a regular byte string
    """
    return bytes.fromhex(hexstr[2:])


def hex2str(hexstr):
    """
    Decodes a hex string into a regular string
    """
    return hex2binary(hexstr).decode("utf-8")


def send_notice(notice: str) -> None:
    send_post("notice", notice)


def send_voucher(voucher: str) -> None:
    send_post("voucher", voucher)


def send_report(report: str) -> None:
    send_post("report", report)


def send_post(endpoint, json_data) -> None:
    response = requests.post(rollup_server + f"/{endpoint}", json=json_data)
    logger.info(
        f"/{endpoint}: Received response status {response.status_code} body {response.content}")


###
# Selector of functions for solidity <contract>.call(<payload>)
VERIFIER_FUNCTION_SIGNATURE = hex(int.from_bytes(
    w3.keccak(b"verifyRealWorldState(string)")[:4], 'big'))
INCREASE_ALLOWANCE_FUNCTION_SELECTOR = hex2binary(
    w3.keccak(b'increaseAllowance()')[:4].hex())


###
def create_verifier_voucher(INCREASE_ALLOWANCE_FUNCTION_SELECTOR, LILIUM_COMPANY_ADDRESS) -> dict:
    voucher = {"destination": LILIUM_COMPANY_ADDRESS, "payload": binary2hex(
        INCREASE_ALLOWANCE_FUNCTION_SELECTOR)}
    return voucher

# Decode Aux Functions


def verify_signature(decoded_input):
    if decoded_input["msg_sig"] != VERIFIER_FUNCTION_SIGNATURE:
        raise ValueError(
            f"Invalid signature {decoded_input['msg_sig']}, expected {VERIFIER_FUNCTION_SIGNATURE}")
    logger.info("Signature verified successfully")
    return True


def decode_verifier_input(binary):
    try:
        function_signature = binary[:4]
        real_world_data = binary[4:]
        verifier_data = {
            "msg_sig": binary2hex(function_signature),
            "real_world_data": real_world_data.decode("utf-8"),
        }
        return verifier_data
    except Exception as e:
        msg = f"Error {e} decoding verifier input {binary}"
        logger.error(f"{msg}\n{traceback.format_exc()}")
        raise Exception(msg)


def process_image_and_predict_state(real_world_data):
    buffer = BytesIO()
    annotated_image, detections = IMAGE_ANALYZER.process_image(
        real_world_data["base64_image"])
    out1 = len(detections)
    annotated_image.save(buffer, format="JPEG")
    annotated_image_base64 = base64.b64encode(
        buffer.getvalue()).decode("utf-8")
    send_notice({"payload": str2hex(annotated_image_base64)})

    out2 = GAUSSIAN_ENVELOP.predict(
        [real_world_data["humidity"], real_world_data["co"], real_world_data["temperature"]])
    logger.info(f"out1 {out1} out2 {out2}")

    return out1, out2


def verify_real_world_state(binary) -> bool:
    global STATE
    try:
        decoded_verifier_input = decode_verifier_input(binary)
        real_world_data = json.loads(
            decoded_verifier_input["real_world_data"].replace("'", '"'))

        if verify_signature(decoded_verifier_input):
            out1, out2 = process_image_and_predict_state(real_world_data)

            if out1 > 0 and out2 == [1]:
                STATE = REAL_WORLD_STATE.SENSORS_COMPLIANT
                logger.info(f"State updated to {STATE}")
                return True
            else:
                logger.info("State not compliant")
                return False
    except Exception as e:
        msg = f"Error {e} verifying real world state {decoded_verifier_input}"
        logger.error(f"{msg}\n{traceback.format_exc()}")
        return False

###
# handlers


def handle_advance(data):
    logger.info(f"Received advance request data {data}.")

    try:
        voucher = None
        payload = data["payload"]
        binary = hex2binary(payload)
        sender = data["metadata"]["msg_sender"]

        if sender == LILIUM_COMPANY_ADDRESS:
            if verify_real_world_state(binary):
                voucher = create_verifier_voucher(
                    INCREASE_ALLOWANCE_FUNCTION_SELECTOR, LILIUM_COMPANY_ADDRESS)
            else:
                send_report({"payload": str2hex(
                    f"Invalid real world state {binary}")})
        else:
            logger.info(
                f"sender {sender} is not lilium company address {LILIUM_COMPANY_ADDRESS}")
        if voucher:
            logger.info(f"voucher {voucher}")
            send_voucher(voucher)
        return "accept"
    except Exception as e:
        msg = f"Error {e} processing data {data}"
        logger.error(f"{msg}\n{traceback.format_exc()}")
        send_report({"payload": str2hex(msg)})
        return "reject"


def handle_inspect(data):
    global STATE
    logger.info(f"Received inspect request data {data}")
    data_decoded = hex2binary(data["payload"]).decode('utf-8')
    try:
        if data_decoded == "status":
            send_report({"payload": str2hex(STATE.name)})
            return "accept"
        else:
            raise Exception(
                f"Unknown payload {data['payload']}, send 'status' to get current state")

    except Exception as e:
        msg = f"Error {e} processing data {data}"
        logger.error(f"{msg}\n{traceback.format_exc()}")
        send_report({"payload": str2hex(msg)})
        return "reject"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}


###
# Main Loop

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])

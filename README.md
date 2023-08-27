# Verifier DApp

```
This works for Cartesi Rollups version 0.9.x
```

The verifier DApp works as an echo dapp, but instead it echoes assets back to the owner emitting vouchers, and also tries to emit vouchers when it receives a json object.

It is a customized DApp written in Python, which originally resembles the one provided by the sample [Echo Python DApp](https://github.com/cartesi/rollups-examples/tree/main/echo-python).
Contrary to that example, this DApp does not use shared resources from the `rollups-examples` main directory, and as such the commands for building, running and deploying it are slightly different.

The documentation below reflects the original application code, and should also be used as a basis for documenting any DApp created with this mechanism.

## Requirements

Please refer to the [rollups-examples requirements](https://github.com/cartesi/rollups-examples/tree/main/README.md#requirements).

## Building

To build the application, run the following command:

```shell
docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl --load
```

## Running

To start the application, execute the following command:

```shell
docker compose -f docker-compose.yml -f docker-compose.override.yml up
```

The application can afterwards be shut down with the following command:

```shell
docker compose -f docker-compose.yml -f docker-compose.override.yml down -v
```

### Advancing time

When executing an example, it is possible to advance time in order to simulate the passing of epochs. To do that, run:

```shell
curl --data '{"id":1337,"jsonrpc":"2.0","method":"evm_increaseTime","params":[864010]}' http://localhost:8545
```

## Running the back-end in host mode

It is possible to run the Cartesi Rollups environment in [host mode](https://github.com/cartesi/rollups-examples/tree/main/README.md#host-mode), so that the DApp's back-end can be executed directly on the host machine, allowing it to be debugged using regular development tools such as an IDE. 

One important note is that Cartesi Rollups can't generate the voucher proofs in host mode, so you wouldn't be able to execute the vouchers.

To start the application, execute the following command:
```shell
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose-host.yml up
```

The application can afterwards be shut down with the following command:
```shell
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose-host.yml down -v
```

This DApp's back-end is written in Python, so to run it in your machine you need to have `python3` installed.
In order to start the back-end, run the following commands in a dedicated terminal:

```shell
cd dapp
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 verifier.py
```

The final command will effectively run the back-end and send corresponding outputs to port `5004`.
It can optionally be configured in an IDE to allow interactive debugging using features like breakpoints.

After that, you can interact with the application normally [as explained above](#interacting-with-the-application).

## Interacting with the application

You can use the frontend web [frontend-web](https://github.com/lynoferraz/frontend-web-cartesi) application to interact with the DApp.

The DApp accepts deposits and json objects:
1. deposits (it sends vouchers to depositor with the same assets)
2. json 

   Emit the json object voucher (e.g. mint cartesi token in hardhat obtained with inpect): 
    
```json
{"destination": "0x610178dA211FEF7D417bC0e6FeD39F05609AD788", "payload": "0x40c10f19000000000000000000000000f39fd6e51aad88f6f4ce6ab8827279cfffb92266000000000000000000000000000000000000000000000000b469471f80140000"}
```
    
3. You can use inspects to get the voucher json object. For that you should send the following json to the inspect endpoint (e.g. mint cartesi token in hardhat)

```json
{"address":"0x610178dA211FEF7D417bC0e6FeD39F05609AD788",
"functionName":"mint",
"parameters":["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",13000000000000000000],
"abi":[{"name": "mint","inputs": [{"type": "address"},{"type": "uint256"}],"type": "function"}]}
```

   Optionally you can provide the function signature (in this example a ERC721 mint with a string):

```json
{"address":"0x7a20...814F",
"functionName":"mint",
"parameters":["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266","test"],
"signature":"mint(address,string)"}
```

Hint: You can use the inspect to create a voucher payload that adds Cartesi DApp as a minter and run in python using the hardhat main wallet (the one that deployed the DApp). First generate the voucher payload with 

```json
{"address":"0x610178dA211FEF7D417bC0e6FeD39F05609AD788",
"functionName":"addMinter",
"parameters":["0xF8C694fd58360De278d5fF2276B7130Bfdc0192A"],
"signature":"addMinter(address)"}
```

Which would give

```json
{"destination": "0x610178dA211FEF7D417bC0e6FeD39F05609AD788", "payload": "0x983b2d56000000000000000000000000f8c694fd58360de278d5ff2276b7130bfdc0192a"}
```

Then run the following python command in the virtual env

```shell
cd dapp
. .venv/bin/activate
python3 -c "from web3 import Web3;Web3(Web3.HTTPProvider('http://localhost:8545')).eth.send_transaction({ 'to': '0x610178dA211FEF7D417bC0e6FeD39F05609AD788', 'data': '0x983b2d56000000000000000000000000f8c694fd58360de278d5ff2276b7130bfdc0192a'})"
```

Notice that the "address" and "payload" translates to "to" and "data" (But remember that this command only work for the local hardhat because it is signing using the default account)

## Deploying to a testnet

Deploying the application to a blockchain requires creating a smart contract on that network, as well as running a validator node for the DApp.
Refer to [rollups-examples deploying dapps](https://github.com/cartesi/rollups-examples#deploying-dapps).

The first step is to set the deployment parameters in the environment variables, creating an env.testnet file using the following code to add whatever is necessary:

```shell
make env
```

Next, we should build the DApp's back-end machine, which will produce a hash that serves as a unique identifier:

```shell
docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl machine --load
```

Once the machine docker image is ready, we can use it to deploy a corresponding Rollups smart contract. This requires you to define a few environment variables to specify which network you are deploying to, which account to use, and which RPC gateway to use when submitting the deploy transaction. We suggest that you add the variables in the env.testnet file.

```bash
MNEMONIC=<user sequence of twelve words>
RPC_URL=https://eth-goerli.alchemyapi.io/v2/<USER_KEY>
WSS_URL=wss://eth-goerli.alchemyapi.io/v2/<USER_KEY>
```

With that in place, you can submit a deploy transaction to the Cartesi DApp Factory contract on the target network by executing the following command:

```shell
docker compose --env-file ./env.testnet -f ./deploy-testnet.yml up
```

This will create a file at `./deployments/<network>/verifier.json` with the deployed contract's address.
Once the command finishes, it is advisable to stop the docker compose and remove the volumes created when executing it.

```shell
docker compose --env-file ./env.testnet -f ./deploy-testnet.yml down -v
```

After that, a corresponding Cartesi Validator Node must also be instantiated in order to interact with the deployed smart contract on the target network and handle the back-end logic of the DApp. The node itself can be started by running a docker compose as follows:

```shell
docker compose --env-file ./env.testnet -f ./docker-compose-testnet.yml -f ./docker-compose.override.yml up
```

## Interacting with the deployed application

With the node running, you can interact with the deployed DApp using the [frontend-console](https://github.com/cartesi/rollups-examples/tree/main/frontend-console), as described [previously](#interacting-with-the-application).
This time, however, you need to specify the appropriate connectivity configurations. Refer to [rollups-examples Interacting with deployed DApps](https://github.com/cartesi/rollups-examples#interacting-with-deployed-dapps) for more information.

As you defined several variables in env.testnet, you can the file to load the variables

```shell
$(cat env.testnet | xargs) && yarn start input send --payload "Hello there" --addressFile path/to/verifier/deployments/sepolia/verifier.json
```

Resulting vouchers can then be retrieved by querying the local Cartesi Node, as before:

```shell
yarn start voucher list
```
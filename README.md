# Verifier DApp

```
This works for Cartesi Rollups version 0.9.x
```

The verifier DApp works as an echo dapp, but instead it echoes assets back to the owner emitting vouchers, and also tries to emit vouchers when it receives a json object.

The documentation below reflects the original application code, and should also be used as a basis for documenting any DApp created with this mechanism.

## Requirements

Please refer to the [rollups-examples requirements](https://github.com/cartesi/rollups-examples/tree/main/README.md#requirements).

## Building [Prod Mode]

To build the application, run the following command:

```shell
docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl  --load
```

## Running [Prod Mode]

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

## Running the back-end in host mode [Prod Mode]

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
ls *.py | ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" entr -r python3 verifier.py
```

The final command will effectively run the back-end and send corresponding outputs to port `5004`.
It can optionally be configured in an IDE to allow interactive debugging using features like breakpoints.

After that, you can interact with the application normally [as explained above](#interacting-with-the-application).

## Interacting with the application



## Building [ Testnet ]

The first step is to set the deployment parameters in the environment variables, creating an env.testnet file using the following code to add whatever is necessary:


```shell
docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl --load --set "*.args.NETWORK=sepolia"
```

```shell
docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl machine --load --set "*.args.NETWORK=sepolia"
```

```shell
make env
```

```shell
source env.testnet
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

```shell
docker compose --env-file ./env.testnet -f ./docker-compose-testnet.yml -f ./docker-compose.override.yml down -v
```
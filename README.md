# Verifier DApp 🌳🔍

🌱 **Compatibility:** 
```
This works for Cartesi Rollups version 0.9.1
```

🌐 **About:**
The implementation of this Cartesi machine aims to generate and trade verified carbon credits, integrating blockchain technology, IoT, and AI. The system is divided into two main components:

### 1. **Computer Vision Module (Yolov8) 📷:**
This module utilizes the YOLOv8 algorithm to process images of trees and trunks captured by IoT devices, assisting in the quantification of forest biomass and, consequently, in the generation of carbon credits.

### 2. **Environmental Analysis Module (Scikit-learn with Gaussian Envelope) 🌡️:**
Analyzes environmental data (temperature, humidity, air quality) collected by IoT devices to evaluate and corroborate the environmental quality of the monitored area.

## 🔧 Requirements

Please refer to the [rollups examples requirements](https://github.com/cartesi/rollups-examples/tree/main/README.md#requirements).

## 🚀 Building the Application for Testnet

To build the application, follow the steps below:

#### **Step 1:** Set the deployment parameters in the environment variables, creating an env.testnet file and adding the necessary details:

```shell
make env
```

```shell
source env.testnet
```

#### **Step 2:** Execute the following commands to build the application:

```shell
docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl --load --set "*.args.NETWORK=<testnet-name>"
```

```shell
docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl machine --load --set "*.args.NETWORK=<testnet-name>"
```

#### **Step 3:** With the parameters in place, you can submit a deploy transaction to the Cartesi DApp Factory contract on the target network by executing the following command:

```shell
docker compose --env-file ./env.testnet -f ./deploy-testnet.yml up
```

📝 **Note:** This will create a file at `./deployments/<network>/verifier.json` with the deployed contract's address. Once the command finishes, it is advisable to stop the docker compose and remove the volumes created when executing it.

```shell
docker compose --env-file ./env.testnet -f ./deploy-testnet.yml down -v
```

#### **Step 4:** Subsequently, a corresponding Cartesi Validator Node must also be instantiated to interact with the deployed smart contract on the target network and handle the back-end logic of the DApp. The node can be started by running a docker compose as follows:

```shell
docker compose --env-file ./env.testnet -f ./docker-compose-testnet.yml -f ./docker-compose.override.yml up
```

```shell
docker compose --env-file ./env.testnet -f ./docker-compose-testnet.yml -f ./docker-compose.override.yml down -v
```

💼 **Done!** You now have your Verifier DApp ready for testing and experimentation!
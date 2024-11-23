# Verifier DApp 🌳🔍

```
This works for Cartesi Rollups version 0.9.X 💻
```

## 🌐 **About:**
The implementation of this Cartesi machine aims to generate and trade verified carbon credits, integrating blockchain technology, IoT, and AI 💼. The system is divided into two vibrant components:

### 1. **Computer Vision Module (Yolov8) 📷:**
This module utilizes the YOLOv8 algorithm to process images of trees and trunks captured by IoT devices 🌲, assisting in the quantification of forest biomass and, consequently, in the generation of carbon credits.

### 2. **Environmental Analysis Module (Scikit-learn with Gaussian Envelope) 🌡️:**
Analyzes environmental data (temperature, humidity, air quality 💨) collected by IoT devices to evaluate and corroborate the environmental quality of the monitored area.

## 🔧 Requirements
Please refer to the [rollups examples requirements](https://github.com/cartesi/rollups-examples/tree/main/README.md#requirements) ✅.

## 🚀 Building and deploying the Application on Testnet

Follow the steps below to build the application after cloning this repo:

#### **Step 1:** Execute the following commands to build the application 🛠️:

***⚠️ If you are using a shell like bash, please run the commands below without the quotes in ```"*.args.NETWORK=<TESTNET_NAME>"```***

```shell
$ docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl --load --set "*.args.NETWORK=<TESTNET_NAME>"
```

```shell
$ docker buildx bake -f docker-bake.hcl -f docker-bake.override.hcl machine --load --set "*.args.NETWORK=<TESTNET_NAME>"
```

#### **Step 2:** Set the deployment parameters in the environment variables, creating an env.testnet file and adding the necessary details 📝:

```shell
$ make env
```

#### **Step 3:** With the parameters in place, you can submit a deploy transaction to the Cartesi DApp Factory contract on the target network by executing the following command 💫:

```shell
$ docker compose --env-file ./env.testnet -f ./deploy-testnet.yml up
```

📝 **Note:** This will create a file at `./deployments/<network>/verifier.json` with the deployed contract's address. Once the command finishes, it is advisable to stop the docker compose and remove the volumes created when executing it:

```shell
$ docker compose --env-file ./env.testnet -f ./deploy-testnet.yml down -v
```
## 🚀 Running a validator node:

Subsequently, a corresponding Cartesi Validator Node must also be instantiated to interact with the deployed smart contract on the target network and handle the back-end logic of the DApp. The node can be started by running a docker compose as follows 🖥️:

```shell
$ docker compose --env-file ./env.testnet -f ./docker-compose-testnet.yml -f ./docker-compose.override.yml up
```

#### 🔎 Once you've finished your testing or wish to stop the Verifier DApp, you can stop the Cartesi Validator Node by running the following command:

```shell
$ docker compose --env-file ./env.testnet -f ./docker-compose-testnet.yml -f ./docker-compose.override.yml down -v
```

💼 **Done!** You now have your Verifier DApp ready for testing and experimentation on testnet! 🎉

## Interacting with the Application 💻

Access the application frontend 🌐: 

### <a href="https://frontend-orcin-psi.vercel.app/" target="_blank">***Lilium WEBAPP***</a>

## ⚠️ Disclaimer

***This repository is in development and not ready for production use. The code and documentation are provided as-is, and may contain bugs or other issues. Please thoroughly test and review the code before considering it for use in a production environment. The maintainers of this repository are not responsible for any issues or damages that may occur from using the code in a production environment.***

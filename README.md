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

📝 **Note:** This will create a file at `./deployments/<network>/verifier.json` with the deployed contract's address. Once the command finishes, it is advisable to stop the docker compose and remove the volumes created when executing it. After this, you need to inform the company contract about the auction dapp address. To do this, go back to the [foundry repository](https://github.com/Lilium-DApp/foundry).

```shell
$ docker compose --env-file ./env.testnet -f ./deploy-testnet.yml down -v
```

#### **Step 4:** Subsequently, a corresponding Cartesi Validator Node must also be instantiated to interact with the deployed smart contract on the target network and handle the back-end logic of the DApp. The node can be started by running a docker compose as follows 🖥️:

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

## 🌟 Special Thanks

We would like to extend our heartfelt gratitude to a group of outstanding individuals who played a pivotal role in helping us understand the intricacies of the Cartesi environment. Their invaluable assistance has been a beacon of light in this project's journey.

- [**Gabriel Barros**](https://github.com/gbarros): Gabriel, your unparalleled assistance in helping us navigate the complex architecture of the Cartesi platform has been monumental. Your readiness to always address our queries and doubts has not only facilitated a smooth project progression but also enriched our understanding immensely. We cannot thank you enough for the depth of knowledge and clarity you brought to the team. 🌟

- [**Felipe Grael**](https://github.com/felipefg): Felipe, your dedicated assistance especially in developing the YOLOv8 model and in porting the cross-compiled libraries to riscv64 has been a cornerstone in the realization of this project. Your technical expertise and commitment were instrumental in overcoming some of the most challenging aspects of this endeavor. Thank you for being a source of guidance and support. 💡

- [**Arthur Vianna**](https://github.com/arthuravianna): Arthur, thank you for your tireless efforts and for always being willing to lend a hand. Your dedication to helping us succeed has not gone unnoticed. 🙌

- [**Lyno Ferraz**](https://github.com/lynoferraz): Lyno, your technical prowess and assistance have been a fundamental part in this project's success. Thank you for helping us navigate through the complexities of the system. 💪

- **Bruno Maia**: Bruno, your continuous support and encouragement have been an anchor, giving us the motivation and resilience to persevere through the challenges. Your faith in our potential and abilities helped to foster a nurturing environment where we could thrive and excel. Thank you for being a pillar of support and inspiration. 🌱
  
- **Payal Patel**: We would like to express our gratitude to Payal Patel, who embodies Cartesi's commitment to its developer community. Your support and engagement with the community play a crucial role in fostering innovation and collaboration. Thank you for being a beacon of guidance and support for all developers navigating the Cartesi ecosystem. 🙌

We sincerely appreciate your time, assistance, and the knowledge you have imparted to us. Here's to more collaborative success in the future! 🎉

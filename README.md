
# Yet Another Kafka (YaK)

Welcome to **Yet Another Kafka** (YaK), a mini-Kafka implementation designed to simulate a distributed publish-subscribe messaging system.

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)

## Project Overview

This project aims to build a **fully functioning Kafka system** with multiple Kafka Brokers, Producers, and Consumers, monitored by a mini-Zookeeper. The system dynamically handles **topic creation, leader election**, and **message replication** between brokers. 

As a fully customizable mini-Kafka, it offers the flexibility to define the **number of Producers and Consumers** and **manage topics** dynamically.

### Objectives

- **Deep dive into Kafka architecture**
- Understand principles like **Fault-Tolerance**, **Recovery**, and **Leader Election**
- Learn to implement a **distributed messaging system** from scratch

## Key Features

- **Dynamic Producer and Consumer Setup**: The number of Producers and Consumers can be specified by the user, with no hardcoding involved.
- **Leader Election**: A leader among Kafka Brokers is automatically elected to handle publish operations.
- **Partition Management**: Messages are partitioned dynamically, with performance evaluation of partitioning methods.
- **Message Replication**: The leader replicates logs to followers for high availability.
- **Fault-Tolerant Brokers**: When the leader broker fails, a new leader is elected, and the system continues to operate.
- **Mini-Zookeeper**: Monitors broker health and handles leader election.
- **Acknowledgement System**: Ensures reliable message delivery with acknowledgments between Producers, Consumers, and Brokers.

## Technologies Used

- **Apache Kafka**: Core message broker system.
- **Zookeeper**: Used to manage and monitor brokers and their health.
- **Python**: Implementation language for the Kafka Brokers, Producers, Consumers, and mini-Zookeeper.
- **File System**: Used for topic and partition storage.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rohan-chandrashekar/Yet-Another-Kafka.git
   cd Yet-Another-Kafka
   ```

2. **Set up environment**:
   Ensure that Python 3.x is installed, along with any necessary libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start mini-Zookeeper**:
   To start the mini-Zookeeper, run:
   ```bash
   python zookeeper_multiple.py
   ```

4. **Start Kafka Brokers**:
   Run the following command to start all Kafka Brokers:
   ```bash
   python broker.py
   ```

5. **Start Producers and Consumers**:
   To start a Producer:
   ```bash
   python producer.py
   ```
   To start a Consumer:
   ```bash
   python consumer.py
   ```

## Usage

### Configurations

- **Dynamic Topics**: Topics can be created and deleted dynamically based on the user's input.
- **Message Acknowledgements**: Producers will resend unacknowledged messages, ensuring message delivery.
- **From-Beginning Mode**: Consumers can pull all past messages from the time of topic creation by using the `--from-beginning` flag.

### Example Usage

Start a Producer that sends messages to a new topic:
```bash
python producer.py --topic my_topic --message "Hello, Kafka!"
```

Start a Consumer that reads from the beginning of the topic:
```bash
python consumer.py --topic my_topic --from-beginning
```

## Architecture

The system consists of multiple modules working together to simulate the functionality of a real-world Kafka setup.

1. **Mini-Zookeeper**: Manages the health of the Kafka Brokers and performs leader election in case of broker failure.
2. **Kafka Brokers**: Handles message publishing, partitioning, and storing, as well as topic and consumer registration.
3. **Producers**: Publishes messages to Kafka topics, ensuring delivery with acknowledgments.
4. **Consumers**: Consumes messages from Kafka topics, with the option to retrieve messages from the beginning of the topic.

### System Diagram

```plaintext
+------------------+       +-------------------+     +-------------------+
|                  |       |                   |     |                   |
|  Mini-Zookeeper  +-------> Kafka Broker 1     |     | Kafka Broker 2     |
|                  |       | (Leader)          |     | (Replica)          |
+------------------+       +-------------------+     +-------------------+
        |                           |                        |
        v                           v                        v
+------------------+       +-------------------+     +-------------------+
|                  |       |                   |     |                   |
|   Producer(s)    |       |   Consumer(s)     |     |   Consumer(s)      |
|                  |       |                   |     |                   |
+------------------+       +-------------------+     +-------------------+
```

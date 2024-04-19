import os

import dotenv

dotenv.load_dotenv()

machineId = int(os.getenv("MACHINE_ID"))
udpAddress = (os.getenv("UDP_ADDRESS"), int(os.getenv("UDP_PORT")))
cloudRunApiEndpoint = os.getenv("CLOUD_RUN_API_ENDPOINT")

debug = os.getenv("DEBUG", "False").lower() == "true"

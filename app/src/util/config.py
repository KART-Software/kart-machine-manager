import os

import dotenv

dotenv.load_dotenv()

machineId = int(os.environ["MACHINE_ID"])
udpAddress = (os.environ["UDP_ADDRESS"], int(os.environ["UDP_PORT"]))
cloudRunApiEndpoint = os.environ["CLOUD_RUN_API_ENDPOINT"]
cloudMessageApiEndpoint = os.environ["CLOUD_MESSAGE_API_ENDPOINT"]
cloudLaptimeApiEndpoint = os.environ["CLOUD_LAPTIME_API_ENDPOINT"]


debug = os.getenv("DEBUG", "False").lower() == "true"

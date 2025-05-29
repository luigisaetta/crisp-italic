"""
General configuration options
"""

#
# application configs
#
# in secs
SLEEP_TIME = 1
DEBUG = False

# OCI GenAI services configuration

# can be also INSTANCE_PRINCIPAL
AUTH_TYPE = "API_KEY"

REGION = "eu-frankfurt-1"
# REGION = "us-chicago-1"
SERVICE_ENDPOINT = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com"

# MODEL_ID = "meta.llama-3.3-70b-instruct"
MODEL_ID = "cohere.command-a-03-2025"
# for DAC
PROVIDER = "cohere"
# MODEL_ID = "ocid1.generativeaiendpoint.oc1.eu-frankfurt-1.amaaaaaa2xxap7yagnde7p532itfpampmqypuk3ofqm4vwxsi2smmkd2xlna"

MAX_TOKENS = 2048

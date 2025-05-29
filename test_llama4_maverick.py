"""
Read data file lines one by one
"""

import random
import time
from collections import defaultdict
from tqdm import tqdm
from model_factory import get_chat_model
from oci_benchmark_utils import prompt_template, parse_model_response, read_all_items

# Path to your JSONL file
FILE_PATH = "italic.jsonl"

DETAILS = False  # Set to True to print detailed information
SLEEP_TIME = 0.01
MAX_ITEMS = 5000
MERGED_LETTERS = "A, B, C, D"


#
# Main
#

# model specific parameters
PROVIDER = "meta"
# pointing to DAC
MODEL_ID = "meta.llama-4-maverick-17b-128e-instruct-fp8"
REGION = "us-chicago-1"
SERVICE_ENDPOINT = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com"
TEMPERATURE = 0.0
model = get_chat_model(model_id=MODEL_ID, provider=PROVIDER, temperature=TEMPERATURE,
                       service_endpoint=SERVICE_ENDPOINT)

#
# read the JSONL file line by line
#
items = read_all_items(FILE_PATH)

# Per-topic accuracy tracking
topic_stats = defaultdict(lambda: {"correct": 0, "total": 0})

print("")
print("All items read !")
print("Start processing items...")
print("")


# extract a sample
sampled_items = random.sample(items, MAX_ITEMS)

tot_correct = 0

for item in tqdm(sampled_items):
    time.sleep(SLEEP_TIME)

    question = item["question"]
    options = item["options"]
    answer = item["answer"]
    topic = item["category"]
    macro_category = item["macro_category"]

    # prepare the list of options:
    formatted_options = "\n".join(
        f"- {list(opt.keys())[0]}: {list(opt.values())[0]}" for opt in options
    )

    final_prompt = prompt_template.format(
        topic=topic,
        question=question,
        options=formatted_options,
        merged_letters=MERGED_LETTERS,
    )

    model_response = model.invoke(final_prompt).content

    if DETAILS:
        print(model_response)
        print("Expected answer:", answer)
        print("")
        print("")

    answer_letter = parse_model_response(model_response)
    topic_stats[topic]["total"] += 1
    if answer_letter == answer:
        tot_correct += 1
        topic_stats[topic]["correct"] += 1


# compute accuracy
accuracy = (tot_correct / MAX_ITEMS) if items else 0


print("")
print("Final summary:")
print("Total items read:", len(items))
print("Total items processed:", MAX_ITEMS)
print("Total correct answers:", tot_correct)
print("Accuracy: {:.2f}%".format(accuracy))
print("")

print("Accuracy per topic:")
sorted_topics = sorted(topic_stats.items(), key=lambda x: x[0])  # alphabetical order

for topic, stats in sorted_topics:
    topic_accuracy = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
    print(f"- {topic}: {topic_accuracy:.2f}% ({stats['correct']} / {stats['total']})")


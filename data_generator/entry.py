import argparse
import time
from datetime import datetime
import json
import os
import random
from multiprocessing import Process, Manager, Lock, Value

from generate_data.dashboard.generate_data import dashboard_batch_worker
from generate_data.organization.generate_data import organization_batch_worker
from generate_data.algorithm.generate_data import algorithm_batch_worker
from generate_data.flowchart.generate_data import flowchart_batch_worker


def worker(queue, lock, success_num, fail_num, batch_worker, args):
    while not queue.empty():
        success, fail = batch_worker(queue.get(), args)
        with lock:
            success_num.value += success
            fail_num.value += fail


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="The type of data to generate. Options: organization, algorithm, flowchart, dashboard.",
    )
    parser.add_argument(
        "--batch_dir",
        type=str,
        default="generate_data/?/data/",
        help="The directory where the batch is stored.",
    )
    parser.add_argument(
        "--seed_domains_path",
        type=str,
        default="generate_data/?/data/seeds/seeds.json",
        help="The path to the human written domains.",
    )
    parser.add_argument(
        "--num_data",
        type=int,
        default=1,
        help="Number of data to generate.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=1,
        help="Number of data for each batch.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.batch_dir = args.batch_dir.replace("?", args.type)
    args.seed_domains_path = args.seed_domains_path.replace("?", args.type)
    batch_worker = None
    if args.type == "organization":
        batch_worker = organization_batch_worker
    elif args.type == "flowchart":
        batch_worker = flowchart_batch_worker
    elif args.type == "dashboard":
        batch_worker = dashboard_batch_worker
    elif args.type == "algorithm":
        batch_worker = algorithm_batch_worker

    random.seed(os.getpid())
    start_time = datetime.now()

    entity_words = []
    with open(os.path.join(args.batch_dir, "lm_generated_seed_domains.json"), "r") as f:
        for line in f:
            data = json.loads(line)
            entity_words.extend(data["entity_words"])

    with open(args.seed_domains_path, "r") as f:
        data = json.load(f)
    entity_words.extend(data["entity_words"])

    # set sample size
    random.shuffle(entity_words)
    sampled_entity_words = random.sample(entity_words, min(1, len(entity_words)))

    success = Value("i", 0)
    fail = Value("i", 0)
    lock = Lock()

    domain_queue = []
    for domain in sampled_entity_words:
        domain_queue.append(domain)

    k = 1
    if k > len(domain_queue):
        k = len(domain_queue)

    # Create k lists, each equal to the elements in domain_queue
    sublists = []
    with Manager() as manager:
        for i in range(k):
            start_index = i * (len(domain_queue) // k)
            end_index = (i + 1) * (len(domain_queue) // k)
            # If it's not the last sublist, make sure it's not out of range
            if i < k - 1:
                sublist = domain_queue[start_index:end_index]
            else:
                # If it is the last sub-list, contains all remaining elements
                sublist = domain_queue[start_index:]

            queue = manager.Queue()
            for domain in sublist:
                queue.put(domain)

            sublists.append(queue)

        processes = []
        for i in range(k):
            time.sleep(random.randint(5, 10) / 10)
            p = Process(target=worker, args=(sublists[i], lock, success, fail, batch_worker, args))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        day = datetime.now().strftime("%Y%m%d")
        batch_dir = os.path.join(args.batch_dir, f"batch{day}")
        data_dict = []
        if os.path.exists(os.path.join(batch_dir, "lm_generated_data.json")):
            with open(os.path.join(batch_dir, "lm_generated_data.json"), "r") as fin:
                for line in fin:
                    data_dict.append(json.loads(line))

        with open(os.path.join(batch_dir, f"{day}.json"), "w") as fout:
            fout.write(json.dumps(data_dict, indent=4))

    # calculate time
    end_time = datetime.now()
    print(
        f"\033[1;34mSuccess: {success.value}, "
        f"Fail: {fail.value}, "
        f"Time used: {end_time - start_time}\033[0m"
    )

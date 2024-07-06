import argparse
import os
import random
import tqdm
import json
import gpt4_tools as gpt4
import filter as filter


random.seed(5708)


def encode_prompt(prompt_domains):
    """
    Encode prompt for new prompt domains
    """

    prompt = f"Come up with other entity words resemble {prompt_domains}.\n"
    requirements = ("Requirements:\n"
                    "Don't limit to the domains given above.\n"
                    "The data behind the entity can be generated and plotted.\n"
                    "Don't generate entity words that are similar to those already generated.\n"
                    "Don not exceed 20 entity words.\n"
                    "Do not output any other content except a string of entity words (No quotes), split by \',\'.\n"
                    )

    return prompt + requirements


def sample_lm_domains(lm_domains_list, n):
    """Sample n machine instructions from a list of machine instructions."""
    return random.sample(lm_domains_list, min(n, len(lm_domains_list)))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="The type of domains to generate. Options: organization, algorithm, flowchart, dashboard.",
    )
    parser.add_argument(
        "--batch_dir",
        type=str,
        default="../data_generator/generate_data/?/data/",
        help="The directory where the batch is stored.",
    )
    parser.add_argument(
        "--seed_domains_path",
        type=str,
        default="../data_generator/generate_data/?/data/seeds/seeds.json",
        help="The path to the human written domains.",
    )
    parser.add_argument(
        "--num_domains_to_generate",
        type=int,
        default=50,
        help="The number of domains to generate.",
    )
    parser.add_argument(
        "--num_prompt_instructions",
        type=int,
        default=10,
        help="The number of instructions to use in the prompt."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.batch_dir = args.batch_dir.replace("?", args.type)
    args.seed_domains_path = args.seed_domains_path.replace("?", args.type)

    # load the seed domains
    seed_domains = json.load(open(args.seed_domains_path, "r"))["entity_words"]
    print(f"Loaded {len(seed_domains)} human-written seed domains.")

    os.makedirs(args.batch_dir, exist_ok=True)

    # load the LM-generated domains
    lm_domains = []
    request_idx = 0
    if os.path.exists(os.path.join(args.batch_dir, "lm_generated_seed_domains.json")):
        with open(os.path.join(args.batch_dir, "lm_generated_seed_domains.json"), "r") as fin:
            for line in fin:
                data_point = json.loads(line)
                lm_domains.extend(data_point["entity_words"])
                request_idx = max(request_idx, data_point["request_idx"])
        print(f"Loaded {len(lm_domains)} LM-generated seed domains.")

    # now generate new domains
    progress_bar = tqdm.tqdm(total=args.num_domains_to_generate)
    if lm_domains:
        progress_bar.update(len(lm_domains))

    with open(os.path.join(args.batch_dir, "lm_generated_seed_domains.json"), "a") as fout:
        # create gpt4 context messages
        context_msgs = []
        # loop until we have expected number of domains
        while len(lm_domains) < args.num_domains_to_generate:
            # sample LM domains
            prompt_domains = sample_lm_domains(lm_domains_list=lm_domains, n=8)
            # sample seed domains
            prompt_domains += random.sample(seed_domains, args.num_prompt_instructions - len(prompt_domains))
            # shuffle the prompt
            random.shuffle(prompt_domains)
            # encode the prompt
            prompt = encode_prompt(prompt_domains=prompt_domains)

            context_msgs.append({"role": "user", "content": prompt})
            text, _ = gpt4.send_chat_request_azure(context_msgs, temp=1.5, sample_n=1)
            context_msgs.append({"role": "assistant", "content": text + "\n"})
            # split text by ','
            lm_generated_domains = text.split(',')
            lm_generated_domains = [domain.strip() for domain in lm_generated_domains]

            # use ROUGE to filter out bad or duplicate domains
            good_results = filter.rouge_filter(lm_generated_domains, prompt_domains)
            progress_bar.update(len(good_results))

            fout.write(json.dumps({
                "entity_words": good_results,
                "request_idx": request_idx + 1
            }) + "\n")

            lm_domains.extend(good_results)
            request_idx += 1

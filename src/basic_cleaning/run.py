#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info(f'Downloading input artifact {args.input_artifact}')
    local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)
    
    logger.info(f'Removing price ouliers. min_price :{args.min_price}, max_price: {args.max_price}')
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    
    logger.info(f'Converting type of last_review')
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    logger.info(f'Saving cleaning df and sendng to W&B')
    # Saving the dataframe in a file
    df.to_csv("clean_sample.csv", index=False)
    
    # Sending the data to W&B
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic cleaning")


    parser.add_argument(
        "--input_artifact", 
        type= str,
        help= "Name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help= "Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help= "type of the output",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help= "min valid price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="max valid price",
        required=True
    )


    args = parser.parse_args()

    go(args)
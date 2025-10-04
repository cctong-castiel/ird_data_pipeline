import argparse
import yaml
from prefect import serve
from core.orchestrator import ird_scrape_data_dag, ird_preprocess_data_dag, ird_rag_dag
# from core.pipeline import run_pipeline

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a YAML file.')
    parser.add_argument('yaml_file', type=str, help='Name of the YAML file')
    args = parser.parse_args()
    print(f'YAML file provided: {args.yaml_file}')

    # load config
    with open(f'src/config/files/{args.yaml_file}.yaml', 'r') as file:
        config = yaml.safe_load(file)
    print(f'Config loaded: {config}')

    # running the default pipeline
    # run_pipeline(config=config)

    # running the Prefect orchestrator DAGs
    ird_scrape_data_dag()
    ird_preprocess_data_dag(config=config)
    ird_rag_dag(config=config)

    # ird_scrape_data_dag.to_deployment(name="ird_scrape_data_deployment")
    # ird_preprocess_data_dag(config=config).to_deployment(name="ird_preprocess_data_deployment")
    # rag_deploy = ird_rag_dag(config=config).to_deployment(name="ird_rag_deployment")
    # serve.deploy([scrape_deploy, preprocess_deploy, rag_deploy])
    # ird_scrape_data_dag()
from core.orchestrator import ird_scrape_data_dag, ird_preprocess_data_dag


if __name__ == "__main__":
    # deploy ird_scrape_data_dag
    ird_scrape_data_dag.deploy(
        name="ird-data-pipeline-deployment",
        work_pool_name="ird-data-pool",
        image="cctongcastiel/ird_data_pipeline_scrape:0.0.1"
    )

    # deploy ird_preprocess_data_dag
    ird_preprocess_data_dag.deploy(
        name="ird-preprocess-pipeline-deployment",
        work_pool_name="ird-data-pool",
        image="cctongcastiel/ird_data_pipeline_preprocess:0.0.1"
    )

    # deploy ird_rag_dag
    # ird_rag_dag.deploy(
    #     name="ird-rag-pipeline-deployment",
    #     work_pool_name="ird-data-pool",
    #     image="cctongcastiel/ird_data_pipeline_rag:0.0.1"
    # )
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
)
from llama_index.core import Settings
import time
from tqdm.notebook import tqdm


def evaluate_llm_performance(questions, query_engine):
    """
    Evaluate the average response time, faithfulness, and relevancy of
    responses generated by GPT-3.5-turbo for a given chunk size.
    """
    # Define Faithfulness and Relevancy Evaluators
    faithfulness_gpt4 = FaithfulnessEvaluator(llm=Settings.llm)
    relevancy_gpt4 = RelevancyEvaluator(llm=Settings.llm)

    total_response_time = 0
    total_faithfulness = 0
    total_relevancy = 0

    num_questions = len(questions)

    # Iterate over each question in eval_questions to compute metrics.
    # While BatchEvalRunner can be used for faster evaluations
    # (see: https://docs.llamaindex.ai/en/latest/examples/evaluation/batch_eval.html),
    # we're using a loop here to specifically measure response time .
    for question in tqdm(questions):
        start_time = time.time()
        response_vector = query_engine.query(question)
        elapsed_time = time.time() - start_time

        faithfulness_result = faithfulness_gpt4.evaluate_response(
            response=response_vector
        ).passing

        relevancy_result = relevancy_gpt4.evaluate_response(
            query=question, response=response_vector
        ).passing

        total_response_time += elapsed_time
        total_faithfulness += faithfulness_result
        total_relevancy += relevancy_result

    average_response_time = total_response_time / num_questions
    average_faithfulness = total_faithfulness / num_questions
    average_relevancy = total_relevancy / num_questions

    return {
        "response_time": average_response_time,
        "faithfulness": average_faithfulness,
        "relevancy": average_relevancy,
    }

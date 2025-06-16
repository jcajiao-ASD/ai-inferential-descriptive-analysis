def create_summary_prompt(json_data: str) -> str:
    """
    Creates a detailed, instruction-tuned prompt for summarizing Copilot metrics.
    """
    # The Qwen2 chat template uses <|im_start|> and <|im_end|> tokens.
    system_prompt = (
        "You are an expert data analyst and technical lead for a software development team. "
        "Your task is to review daily developer productivity metrics from GitHub Copilot and "
        "provide a concise summary for management. The summary must be both descriptive (stating the facts) "
        "and inferential (providing actionable insights and identifying trends)."
    )

    user_prompt = (
        "Please analyze the following GitHub Copilot usage data, which is provided as a JSON object. "
        "Generate a response in Markdown format with two distinct sections: 'Descriptive Summary' and 'Inferential Insights'.\n\n"
        "In the 'Descriptive Summary', state the key absolute metrics, such as total suggestions, total acceptances, "
        "overall acceptance rate, and total lines of code accepted.\n\n"
        "In the 'Inferential Insights', analyze the data to identify notable trends, potential issues, or positive outcomes. "
        "Consider the following questions: Is the acceptance rate healthy? Which programming languages or IDEs show the highest engagement? "
        "Is there a significant discrepancy between chat usage and code completion usage that might suggest a need for more team training? "
        "Highlight any data points that are particularly high, low, or anomalous.\n\n"
        "Here is the data:\n"
        f"```json\n{json_data}\n```"
    )

    # Construct the final prompt using the Qwen2-Instruct chat format.
    full_prompt = (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    return full_prompt

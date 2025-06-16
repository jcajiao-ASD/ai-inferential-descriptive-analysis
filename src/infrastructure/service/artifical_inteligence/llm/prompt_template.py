def create_summary_prompt(json_data: str) -> str:
    """
    Creates a detailed, instruction-tuned prompt for summarizing Copilot metrics.
    """
    # The Qwen2 chat template uses <|im_start|> and <|im_end|> tokens.
    system_prompt = (
        "You are an expert data analyst and technical lead for a software development team. "
        "Your task is to review daily developer productivity metrics from GitHub Copilot and "
        "provide a concise summary for management. The summary must be both descriptive (stating the facts) "
        "and inferential (providing actionable insights and identifying trends). "
        "Please provide all your responses in Spanish."
    )

    user_prompt = (
        "Por favor analiza los siguientes datos de uso de GitHub Copilot, proporcionados como objeto JSON. "
        "Genera una respuesta en formato Markdown con dos secciones distintas: 'Resumen Descriptivo' y 'Insights Inferenciales'.\n\n"
        "En el 'Resumen Descriptivo', indica las métricas clave absolutas, como total de sugerencias, total de aceptaciones, "
        "tasa general de aceptación y total de líneas de código aceptadas.\n\n"
        "En los 'Insights Inferenciales', analiza los datos para identificar tendencias notables, posibles problemas o resultados positivos. "
        "Considera las siguientes preguntas: ¿Es saludable la tasa de aceptación? ¿Qué lenguajes de programación o IDEs muestran mayor engagement? "
        "¿Existe una discrepancia significativa entre el uso del chat y la completación de código que pueda sugerir la necesidad de más capacitación al equipo? "
        "Destaca cualquier dato que sea particularmente alto, bajo o anómalo.\n\n"
        "Aquí están los datos:\n"
        f"```json\n{json_data}\n```\n\n"
        "Asegúrate de responder completamente en español."
    )

    # Construct the final prompt using the Qwen2-Instruct chat format.
    full_prompt = (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    return full_prompt

"""
LLM Service module for handling large language model operations.

This module provides:
- LLMService: A class for loading, unloading, and using LLMs for text generation
"""

from llama_cpp import Llama


class LLMService:
    """
    A service for handling large language model operations.

    Attributes
    ----------
    model_path : str
        Path to the GGUF model file.
    llm : Llama
        The loaded language model instance.

    Methods
    -------
    load_model() -> None
        Loads the GGUF model into memory.
    unload_model() -> None
        Unloads the model and releases resources.
    generate_summary(prompt: str) -> str
        Generates a summary using the loaded model.

    """

    def __init__(self, model_path: str):
        """
        Initialize the LLM service with a model path.

        Parameters
        ----------
        model_path : str
            Path to the GGUF model file to be loaded.

        """
        self.model_path = model_path
        self.llm = None

    def load_model(self):
        """
        Load the GGUF model into memory.

        This method initializes the Llama model with specific parameters
        for context window size, GPU layers, and threading.

        Raises
        ------
        RuntimeError
            If the model file cannot be found or loaded.

        """
        print(f"Loading model from: {self.model_path}")
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=4096,  # Context window size
            n_gpu_layers=0,  # Explicitly set to 0 for CPU-only inference
            n_threads=8,  # Adjust based on available CPU cores
            verbose=True,
        )
        print("Model loaded successfully.")

    def unload_model(self):
        """Unloads the model and releases resources."""
        if self.llm:
            # The Llama object from llama-cpp-python handles resource cleanup
            # upon garbage collection. Setting it to None suffices.
            self.llm = None
            print("Model unloaded.")

    def generate_summary(self, prompt: str) -> str:
        """Generate a summary using the loaded model."""
        if not self.llm:
            raise RuntimeError("Model is not loaded. Cannot generate summary.")

        output = self.llm(
            prompt,
            max_tokens=512,  # Max length of the summary
            stop=["<|im_end|>", "##"],  # Stop tokens for Qwen2
            echo=False,
        )
        if output["choices"] and len(output["choices"]) > 0:
            return output["choices"][0]["text"].strip()
        else:
            return "No se pudo generar una respuesta"


# Instantiate the service
llm_service = LLMService(
    model_path="src/infrastructure/service/artifical_inteligence/models/qwen2-1_5b-instruct-q5_k_m.gguf"
)

from llama_index.embeddings.adapter.utils import BaseAdapter
import torch.nn.functional as F
from torch import nn, Tensor
import torch
from typing import Dict, List


class CustomNN(BaseAdapter):
    """Custom NN transformation.

    Args:
        hidden_layers (List[int]): Dimensions of all layers.
        bias (bool): Whether to use bias. Defaults to False.
        activation_fn_str (str): Name of activation function. Defaults to "relu".

    """

    def __init__(
        self,
        hidden_layers: List[int],
        bias: bool = False,
        add_residual: bool = False,
    ) -> None:
        super(CustomNN, self).__init__()

        self.bias = bias
        self.hidden_layers = hidden_layers
        list_linear_layers = []
        for h, _ in enumerate(hidden_layers[:-1]):
            list_linear_layers.append(
                nn.Linear(hidden_layers[h], hidden_layers[h + 1], bias=bias)
            )
        self.linear_layers = nn.ModuleList(list_linear_layers)
        self._add_residual = add_residual
        # if add_residual, then add residual_weight (init to 0)
        self.residual_weight = nn.Parameter(torch.zeros(1))

    def forward(self, embed: Tensor) -> Tensor:
        """Forward pass (Wv).

        Args:
            embed (Tensor): Input tensor.

        """
        output = embed.detach().clone()
        for layer in self.linear_layers:
            output = layer(output)
            output = F.relu(output)

        if self._add_residual:
            output = self.residual_weight * output + embed

        return output

    def get_config_dict(self) -> Dict:
        """Get config dict."""
        return {
            "hidden_layers": self.hidden_layers,
            "bias": self.bias,
            "add_residual": self._add_residual,
        }

"""
Custom CNN Feature Extractor for Dr. Mario

Handles 12-channel observations (16, 8, 12) for Stable-Baselines3.
"""

import torch
import torch.nn as nn
from gymnasium import spaces
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class DrMarioCNN(BaseFeaturesExtractor):
    """
    Custom CNN for Dr. Mario observations (16, 8, 12).

    Architecture:
    - Conv2D(12, 32, kernel_size=3) - Extract spatial features
    - Conv2D(32, 64, kernel_size=3) - Deepen features
    - Flatten
    - Linear(features_dim)
    """

    def __init__(self, observation_space: spaces.Box, features_dim: int = 256):
        """
        Args:
            observation_space: Observation space (16, 8, 12)
            features_dim: Output feature dimension
        """
        super().__init__(observation_space, features_dim)

        # Get input shape
        n_input_height, n_input_width, n_input_channels = observation_space.shape

        # CNN layers (channels-last input → channels-first for PyTorch)
        self.cnn = nn.Sequential(
            # Input: (batch, 12, 16, 8) after transpose
            nn.Conv2d(n_input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),  # → (batch, 64, 8, 4)
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing a forward pass
        with torch.no_grad():
            sample = torch.zeros(1, n_input_height, n_input_width, n_input_channels)
            # Transpose to channels-first for PyTorch: (B, H, W, C) → (B, C, H, W)
            sample = sample.permute(0, 3, 1, 2)
            n_flatten = self.cnn(sample).shape[1]

        # Linear layer to get features_dim output
        self.linear = nn.Sequential(
            nn.Linear(n_flatten, features_dim),
            nn.ReLU(),
        )

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Args:
            observations: (batch, height, width, channels) - channels-last from SB3

        Returns:
            Features: (batch, features_dim)
        """
        # SB3 gives us (B, H, W, C), PyTorch Conv2d expects (B, C, H, W)
        # Permute: (B, H, W, C) → (B, C, H, W)
        x = observations.permute(0, 3, 1, 2)

        # Pass through CNN
        x = self.cnn(x)

        # Pass through linear layer
        x = self.linear(x)

        return x


if __name__ == "__main__":
    # Test the custom CNN
    import gymnasium as gym

    obs_space = gym.spaces.Box(
        low=0.0,
        high=1.0,
        shape=(16, 8, 12),
        dtype="float32"
    )

    print("Testing DrMarioCNN...")
    print(f"Observation space: {obs_space.shape}")

    cnn = DrMarioCNN(obs_space, features_dim=256)

    # Create dummy observation
    dummy_obs = torch.zeros(4, 16, 8, 12)  # Batch of 4

    # Forward pass
    features = cnn(dummy_obs)

    print(f"Input shape: {dummy_obs.shape}")
    print(f"Output shape: {features.shape}")
    print(f"Expected: (4, 256)")

    assert features.shape == (4, 256), f"Expected (4, 256), got {features.shape}"

    print("✓ DrMarioCNN test passed!")

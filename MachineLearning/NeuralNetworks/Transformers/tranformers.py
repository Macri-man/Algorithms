import numpy as np
import matplotlib.pyplot as plt
def get_positional_encoding(max_len, d_model):
    pos = np.arange(max_len)[:, np.newaxis]  # Shape (max_len, 1)
    i = np.arange(d_model)[np.newaxis, :]  # Shape (1, d_model)
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / d_model)  # Shape (1, d_model)

    pos_encoding = pos * angle_rates  # Shape (max_len, d_model)
    pos_encoding[:, 0::2] = np.sin(pos_encoding[:, 0::2])  # Apply sine to even indices
    pos_encoding[:, 1::2] = np.cos(pos_encoding[:, 1::2])  # Apply cosine to odd indices
    return pos_encoding
class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.num_heads = num_heads
        self.d_model = d_model
        self.depth = d_model // num_heads

        # Weights for the query, key, and value
        self.Wq = np.random.randn(d_model, d_model) * 0.01
        self.Wk = np.random.randn(d_model, d_model) * 0.01
        self.Wv = np.random.randn(d_model, d_model) * 0.01
        self.Wo = np.random.randn(d_model, d_model) * 0.01

    def split_heads(self, x):
        batch_size = x.shape[0]
        x = x.reshape(batch_size, -1, self.num_heads, self.depth)  # Shape (batch_size, seq_len, num_heads, depth)
        return np.transpose(x, (0, 2, 1, 3))  # Shape (batch_size, num_heads, seq_len, depth)

    def attention(self, q, k, v, mask=None):
        matmul_qk = np.dot(q, k.T)  # Shape (batch_size, num_heads, seq_len, seq_len)
        scaled_attention_logits = matmul_qk / np.sqrt(self.depth)

        if mask is not None:
            scaled_attention_logits += (mask * -1e9)  # Masking

        attention_weights = self.softmax(scaled_attention_logits)
        output = np.dot(attention_weights, v)  # Shape (batch_size, num_heads, seq_len, depth)

        return output, attention_weights

    def forward(self, x):
        q = np.dot(x, self.Wq)
        k = np.dot(x, self.Wk)
        v = np.dot(x, self.Wv)

        q = self.split_heads(q)  # Shape (batch_size, num_heads, seq_len, depth)
        k = self.split_heads(k)
        v = self.split_heads(v)

        attention, _ = self.attention(q, k, v)

        attention = np.transpose(attention, (0, 2, 1, 3))  # Shape (batch_size, seq_len, num_heads, depth)
        concat_attention = attention.reshape(attention.shape[0], -1, self.d_model)  # Shape (batch_size, seq_len, d_model)

        output = np.dot(concat_attention, self.Wo)  # Shape (batch_size, seq_len, d_model)
        return output

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
class FeedForwardNetwork:
    def __init__(self, d_model, d_ff):
        self.W1 = np.random.randn(d_model, d_ff) * 0.01  # Weights for the first layer
        self.b1 = np.zeros((d_ff, 1))  # Bias for the first layer
        self.W2 = np.random.randn(d_ff, d_model) * 0.01  # Weights for the second layer
        self.b2 = np.zeros((d_model, 1))  # Bias for the second layer

    def forward(self, x):
        x = self.relu(np.dot(x, self.W1) + self.b1)  # Apply first layer
        return np.dot(x, self.W2) + self.b2  # Apply second layer

    def relu(self, x):
        return np.maximum(0, x)
class EncoderLayer:
    def __init__(self, d_model, num_heads, d_ff):
        self.mha = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForwardNetwork(d_model, d_ff)
        self.layernorm1 = np.zeros((d_model, 1))  # Layer normalization parameters
        self.layernorm2 = np.zeros((d_model, 1))

    def forward(self, x):
        attn_output = self.mha.forward(x)
        x = x + attn_output  # Residual connection
        x = self.layernorm1 + x  # Layer normalization

        ffn_output = self.ffn.forward(x)
        x = x + ffn_output  # Residual connection
        x = self.layernorm2 + x  # Layer normalization

        return x
class Transformer:
    def __init__(self, input_size, d_model, num_heads, num_layers, d_ff):
        self.d_model = d_model
        self.encoder_layers = [EncoderLayer(d_model, num_heads, d_ff) for _ in range(num_layers)]
        self.positional_encoding = get_positional_encoding(max_len=50, d_model=d_model)  # Example length

    def forward(self, x):
        seq_len = x.shape[1]
        x += self.positional_encoding[:seq_len, :]

        for layer in self.encoder_layers:
            x = layer.forward(x)

        return x
input_size = 20  # Input dimension
d_model = 64  # Embedding size
num_heads = 4  # Number of attention heads
num_layers = 2  # Number of encoder layers
d_ff = 128  # Feed-forward network size

# Create a sample input
sample_input = np.random.rand(32, 50, input_size)  # (batch_size, seq_len, input_size)

# Create the Transformer model
transformer = Transformer(input_size=input_size, d_model=d_model, num_heads=num_heads, num_layers=num_layers, d_ff=d_ff)

# Forward pass
output = transformer.forward(sample_input)
print("Output shape:", output.shape)

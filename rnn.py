import torch 
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import sys
import pyprof
import torch.cuda.profiler as profiler



# Device configuration

gpu_id = sys.argv[1]
device = f"cuda:{gpu_id}"

# Hyper-parameters
sequence_length = 28
input_size = 28
hidden_size = 128
num_layers = 2
num_classes = 10
batch_size = int(sys.argv[2])
num_epochs = 2
learning_rate = 0.01


# Recurrent neural network (many-to-one)
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        # Set initial hidden and cell states 
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device) 
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))  # out: tensor of shape (batch_size, seq_length, hidden_size)
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

model = RNN(input_size, hidden_size, num_layers, num_classes).to(device)

# Test the model
model.eval()
with torch.no_grad():
    inputs = torch.randn(batch_size, 28, 28).to(device)
    pyprof.init()
    outputs = model(inputs)

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')

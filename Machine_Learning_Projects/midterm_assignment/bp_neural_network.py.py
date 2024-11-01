import numpy as np

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.learning_rate = learning_rate
        
        # 初始化权重和偏置
        self.weights_input_to_hidden = np.random.normal(0.0, self.hidden_nodes**-0.5, 
                                                       (self.input_nodes, self.hidden_nodes))
        self.weights_hidden_to_output = np.random.normal(0.0, self.output_nodes**-0.5, 
                                                        (self.hidden_nodes, self.output_nodes))
        self.biases_hidden = np.zeros(self.hidden_nodes)
        self.biases_output = np.zeros(self.output_nodes)
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward_pass(self, inputs):
        self.hidden_inputs = np.dot(inputs, self.weights_input_to_hidden) + self.biases_hidden
        self.hidden_outputs = self.sigmoid(self.hidden_inputs)
        
        self.final_inputs = np.dot(self.hidden_outputs, self.weights_hidden_to_output) + self.biases_output
        self.final_outputs = self.sigmoid(self.final_inputs)
        
        return self.final_outputs
    
    def backward_pass(self, inputs, targets):
        # 计算输出层误差
        output_errors = targets - self.final_outputs
        output_gradients = output_errors * self.sigmoid_derivative(self.final_outputs)
        
        # 计算隐藏层误差
        hidden_errors = np.dot(output_gradients, self.weights_hidden_to_output.T)
        hidden_gradients = hidden_errors * self.sigmoid_derivative(self.hidden_outputs)
        
        # 更新权重和偏置
        self.weights_hidden_to_output += self.learning_rate * np.dot(self.hidden_outputs.T, output_gradients)
        self.biases_output += self.learning_rate * np.sum(output_gradients, axis=0)
        
        self.weights_input_to_hidden += self.learning_rate * np.dot(inputs.T, hidden_gradients)
        self.biases_hidden += self.learning_rate * np.sum(hidden_gradients, axis=0)
        
    def train(self, inputs_list, targets_list, epochs):
        for epoch in range(epochs):
            for inputs, targets in zip(inputs_list, targets_list):
                inputs = np.array([inputs])  # 确保输入是二维数组
                targets = np.array([targets])  # 确保目标是二维数组
                self.forward_pass(inputs)
                self.backward_pass(inputs, targets)
                
            if epoch % 100 == 0:
                loss = np.mean((targets_list - self.forward_pass(inputs_list))**2)
                print(f'Epoch {epoch}, Loss: {loss}')

# 示例数据
inputs_list = np.array([[0.1, 0.2], [0.3, 0.4]])
targets_list = np.array([[0.9, 0.1], [0.8, 0.2]])

# 创建神经网络实例
nn = NeuralNetwork(input_nodes=2, hidden_nodes=3, output_nodes=2, learning_rate=0.1)

# 训练神经网络
nn.train(inputs_list, targets_list, epochs=1000)
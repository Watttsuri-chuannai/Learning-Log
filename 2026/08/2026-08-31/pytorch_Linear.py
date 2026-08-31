import torch
#print("PyTorch 版本：", torch.__version__)
#print("是否能使用 GPU：", torch.cuda.is_available())

x = torch.tensor([
    [1.0],
    [3.0],
    [5.0],
    [10.0]
])

y = torch.tensor([
    [1.5],
    [4.5],
    [7.5],
    [15.0]
])

"""
w = torch.tensor([[1.0]], requires_grad=True)
b = torch.tensor([5.0], requires_grad=True)

learning_rate = 0.01

for epoch in range(10000):
    y_hat = x @ w + b
    loss = ((y_hat - y)**2).mean()
    loss.backward()


    with torch.no_grad():
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad

    w.grad.zero_()
    b.grad.zero_()

    if epoch % 100 == 0:
        print(f"第 {epoch} 轮，loss = {loss.item():.6f}")

print("最终的w:", w)
print("最终的b:", b)
"""

model = torch.nn.Linear(1, 1)
loss_function = torch.nn.MSELoss()
optimizer = torch.optim.SGD(
    model.parameters(),
    lr = 0.01
)

for epoch in range(1000):
    y_hat = model(x)
    loss = loss_function(y_hat, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 100 == 0:
        print(f"第 {epoch} 轮，loss = {loss.item():.6f}")

print("最终 w：", model.weight.item())
print("最终 b：", model.bias.item())
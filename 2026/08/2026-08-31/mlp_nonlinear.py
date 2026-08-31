import torch

x = torch.linspace(-2, 2, 100).reshape(-1, 1)
y = x ** 2

model = torch.nn.Sequential(
    torch.nn.Linear(1, 16),
    torch.nn.ReLU(),
    torch.nn.Linear(16, 1)
)
loss_function = torch.nn.MSELoss()
optimizer = torch.optim.SGD(
    model.parameters(),
    lr = 0.05
)

for epoch in range(5000):
    y_hat = model(x)
    loss = loss_function(y_hat, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 500 == 0:
        print(f"第 {epoch} 轮，loss = {loss.item():.6f}")

with torch.no_grad():
    test_x = torch.tensor([[-2.0], [-1.0], [0.0], [1.0], [2.0]])
    prediction = model(test_x)

print(prediction)
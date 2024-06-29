import numpy as np
from sklearn.linear_model import LinearRegression


def linear_regression(data):
    X = np.array(data)[:, 0].reshape(-1, 1)
    y = np.array(data)[:, 1]

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)

    result = np.column_stack((X.flatten(), y_pred))
    return result.tolist()


# Example usage
# data = [[1, 2], [2, 3], [3, 5], [4, 7]]
# result = linear_regression(data)
# print(f"result: {result}")

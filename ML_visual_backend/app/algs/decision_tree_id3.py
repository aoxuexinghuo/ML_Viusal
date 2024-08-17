import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree


def decision_tree_id3(data):
    # 生成示例数据
    df = pd.DataFrame(data)

    # 将分类变量转换为数值
    df = pd.get_dummies(df, columns=['天气', '温度', '湿度', '风速'])

    # 准备数据
    X = df.drop(columns=['打羽毛球'])
    y = df['打羽毛球']

    # 分割数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    # 使用ID3算法创建决策树
    clf = DecisionTreeClassifier(criterion='entropy', random_state=1)
    clf = clf.fit(X_train, y_train)

    return clf, X.columns.tolist()


def generate_tree_mermaid_code(data):
    decision_tree, feature_names = decision_tree_id3(data)

    def recurse_tree(node):
        if decision_tree.tree_.feature[node] != _tree.TREE_UNDEFINED:  # not a leaf
            name = feature_names[decision_tree.tree_.feature[node]]
            left_child = decision_tree.tree_.children_left[node]
            right_child = decision_tree.tree_.children_right[node]
            node_id = f"node{node}"
            left_id = f"node{left_child}"
            right_id = f"node{right_child}"
            if decision_tree.tree_.threshold[node] != -2:  # check if it is a split node
                decision_text = f"{name}"
            else:
                decision_text = f"{name}"

            return (
                    f"{node_id}([{decision_text}])\n" +
                    recurse_tree(left_child) +
                    recurse_tree(right_child) +
                    f"{node_id} -->|是| {left_id}\n" +
                    f"{node_id} -->|否| {right_id}\n"
            )
        else:  # leaf node
            value = decision_tree.tree_.value[node]
            class_id = value.argmax()
            class_name = decision_tree.classes_[class_id]
            return f"node{node}[\"{class_name}\"]\n"

    # Start recursion from the root
    mermaid_code = "graph TD\n"
    mermaid_code += "Root([Root]) --> node0\n"
    mermaid_code += recurse_tree(0)
    # print(mermaid_code)
    return mermaid_code

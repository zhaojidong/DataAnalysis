
import pandas as pd


if __name__ == '__main__':
    df = pd.DataFrame(columns=list("ABC"))
    # df.loc[len(df)] = [1, 2, 3]
    print(df)
    # dict_1 = {'Name': ['Zara', 'TT'], 'Age': 7, 'Class': 'First', 'Address': 'Beijing'}
    # for key, value in dict_1.items():
    #     print(key)
    #     if type(value) is []:
    #         for v in value:
    #             print(v)
    #     else:
    #         print(value)

    # inp = [{'c1': 10, 'c2': 100}, {'c1': 11, 'c2': 110}, {'c1': 12, 'c2': 123}]
    # df = pd.DataFrame(inp)
    # print(df)
    # print(df.at[1, 'c1'])
    # for index, row in df.iterrows():
    #     print(index)  # 输出每行的索引值
    #     print(row[index-1])





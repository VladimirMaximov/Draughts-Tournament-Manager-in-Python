import pandas as pd

dataframe = pd.DataFrame({"Название турнира:": ["Турнир посвященный Новому году"],
                          "ФИО судьи:": ["Vadsfkjlasd;f"],
                          "ФИО помощника судьи:": ["asdfasdfs"],
                          "Система проведения соревнований:": ["fadsaf"],
                          "Количество туров:": ["fdsaafsd"],
                          "Номер текущего тура:": ["afdsfsda"],
                          "Дата начала соревнований:": ["fadssfda"],
                          "Дата окончания соревнований:": ["fdsasfda"],
                          "Приоритет 1 при равенстве очков:": ["fdasdfs"],
                          "Приоритет 2 при равенстве очков:": ["fdasasd"],
                          "Приоритет 3 при равенстве очков:": ["asfd"],
                          "Приоритет 4 при равенстве очков:": ["asfddf"]}).set_index("Название турнира:").T

dataframe = pd.read_excel("C:/Users/user/Desktop/12345 2024-01-15.xlsx", sheet_name="Турнирные данные")
referee_name, assistant_referee_name, system, count_of_tours, \
                current_tour, start, end, pr1, pr2, pr3, pr4 = tuple(dataframe[dataframe.columns[1]].tolist())
print(dataframe[dataframe.columns[1]].tolist())


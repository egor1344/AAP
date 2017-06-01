from main.models import Apartment
from django.db.models import Max, Avg, Min, StdDev, Sum, Variance
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

class Command(BaseCommand):
    help = 'Analitic price aprtment'

    # def add_arguments(self, parser):
    #     parser.add_argument('pages', default=1, type=int)

    def handle(self, *args, **options):
        exel = pd.read_excel('test.xlsx', 'Все обьявления по Уфе', index_col=None, na_values=['NA'])
        # corr = exel.corr()
        main_data = exel.drop(['f1','f2','f3','f4','f5','f6','city','site',
            'adress',"district","type_house", 'floor', 'name'], axis=1)
        trg = main_data[['price', 'price_for_metr']]
        trn = main_data.drop(['price', 'price_for_metr'], axis=1)
        print(main_data.corr())
        # corr = main_data.corr()
        # print(corr)
        # print(main_data.shape)
        # Xtrn, Xtest, Ytrn, Ytest = train_test_split(trn, trg, test_size=0.4)
        # models = [LinearRegression(), # метод наименьших квадратов
        #       RandomForestRegressor(n_estimators=100, max_features ='sqrt'), # случайный лес
        #       KNeighborsRegressor(n_neighbors=6), # метод ближайших соседей
        #       SVR(kernel='linear'), # метод опорных векторов с линейным ядром
        #       LogisticRegression() # логистическая регрессия
        #       ]
        # TestModels = pd.DataFrame()
        # tmp = {}
        # #для каждой модели из списка
        # for model in models:
        #     #получаем имя модели
        #     m = str(model)
        #     tmp['Model'] = m[:m.index('(')]    
        #     #для каждого столбцам результирующWWего набора
        #     for i in range(Ytrn.shape[1]):
        #         #обучаем модель
        #         model.fit(Xtrn, Ytrn[0]) 
        #         #вычисляем коэффициент детерминации
        #         tmp['R2_Y%s'%str(i+1)] = r2_score(Ytest[0], model.predict(Xtest))
        #     #записываем данные и итоговый DataFrame
        #     TestModels = TestModels.append([tmp])
        # #делаем индекс по названию модели
        # TestModels.set_index('Model', inplace=True)
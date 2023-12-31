
import csv,os,re,sys,codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib,  statistics
from sklearn.model_selection import GridSearchCV 
from sklearn.pipeline import Pipeline
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm 
from sklearn.linear_model import LogisticRegression 
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectKBest,chi2,mutual_info_classif,f_classif
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import classification_report
from collections import Counter
from sklearn.neighbors import KNeighborsClassifier



### converting age in days ########

def convert_string_to_float(input_string):
    if input_string.strip() == '--':
        return input_string  # return the unchanged value '--'
    
    parts = input_string.split()
    years = 0
    days = 0

    for i in range(0, len(parts), 2):
        value = int(parts[i])
        unit = parts[i + 1]

        if unit == 'years':
            years = value
        elif unit == 'days':
            days = value

    total_days = years * 365 + days
    return float(total_days)

input_file = 'training_data.csv'
output_file = 'trainnnnn.csv'

with open(input_file, 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        row[1] = convert_string_to_float(row[1])
        writer.writerow(row)



input_file = 'test_data.csv'
output_file = 'tsttt.csv'

with open(input_file, 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        row[1] = convert_string_to_float(row[1])
        writer.writerow(row)


 ########## imputation of missing values #################




df = pd.read_csv('trainnnnn.csv')
df3 = pd.read_csv('tsttt.csv')

search_string1 = '--'
search_string2 = 'not reported'


for column in df.columns:
    if df[column].dtype == 'object':  
        column_counts = df[column].value_counts()
        
        
        most_common_value = column_counts.idxmax()
        
        
        df[column] = df[column].replace([search_string1, search_string2], most_common_value)


df.to_csv('trainn2.csv', index=False)



for column in df3.columns:
    if df3[column].dtype == 'object':  
        column_counts = df3[column].value_counts()
        
        
        most_common_value = column_counts.idxmax()
        
        
        df3[column] = df3[column].replace([search_string1, search_string2], most_common_value)


df3.to_csv('tsttt2.csv', index=False)





file_path = 'trainn2.csv'
df = pd.read_csv(file_path)

column_name = 'Age_at_diagnosis'
string_to_replace = '--'

df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
mean_value = df[column_name].mean()
mean_value = int(mean_value)
df[column_name].replace(string_to_replace, mean_value, inplace=True)

output_file_path = 'output_file.csv'
df.to_csv(output_file_path, index=False)


file_path = 'output_file.csv'
df = pd.read_csv(file_path)

column_name = 'Age_at_diagnosis'

variable_value = mean_value

df[column_name].fillna(variable_value, inplace=True)

output_file_path = 'imputed_data.csv'
df.to_csv(output_file_path, index=False)





############## one hot encoding ##############



df = pd.read_csv('imputed_data.csv')
df2 = pd.read_csv('tsttt2.csv')
categorical_columns = ['Gender','Primary_Diagnosis','Race','IDH1','TP53','ATRX','PTEN','EGFR','CIC','MUC16','PIK3CA','NF1','PIK3R1','FUBP1','RB1','NOTCH1','BCOR','CSMD3','SMARCA4','GRIN2A','IDH2','FAT4','PDGFRA']



df_encoded = pd.get_dummies(df, columns=categorical_columns)
df_encoded = df_encoded.astype(int)
df_encoded.to_csv('encoded_file.csv', index=False)



df2_encoded = pd.get_dummies(df2, columns=categorical_columns)
df2_encoded = df2_encoded.astype(int)
df2_encoded.to_csv('encoded_test.csv', index=False)


csv_file_path = 'encoded_test.csv'
df = pd.read_csv(csv_file_path)
df['Race_american indian or alaska native'] = 0
df['Race_asian'] = 0
df['BCOR_MUTATED'] = 0
df['CSMD3_MUTATED'] = 0
df.to_csv(csv_file_path, index=False)





###############   adding column name to target csv file   ##########


csv_file = 'training_data_targets.csv'
target_file = 'targets.csv'

new_column_names = ['target']

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    rows = [row for row in reader]

rows.insert(0, new_column_names)

with open(target_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)




# creating a new csv file with data and target values



source_file = 'targets.csv'
destination_file = 'encoded_file.csv'
final_file = 'now_train.csv'

column_name = 'target'


with open(source_file, 'r') as source:
    source_reader = csv.DictReader(source)
    
   
    column_data = [row[column_name] for row in source_reader]


with open(destination_file, 'r') as destination:
    destination_reader = csv.DictReader(destination)
    
   
    destination_header = destination_reader.fieldnames
    
    
    destination_data = [row for row in destination_reader]


destination_header.append(column_name)


for dest_row, source_value in zip(destination_data, column_data):
    dest_row[column_name] = source_value


with open(final_file, 'w', newline='') as destination:
    destination_writer = csv.DictWriter(destination, fieldnames=destination_header)
    destination_writer.writeheader()
    destination_writer.writerows(destination_data)



















data= pd.read_csv('now_train.csv')
data=np.asarray(data)






class classification():
     def __init__(self,path='now_train.csv',clf_opt='lr',no_of_selected_features=None):
        self.path = path
        self.clf_opt=clf_opt
        self.no_of_selected_features=no_of_selected_features
        if self.no_of_selected_features!=None:
            self.no_of_selected_features=int(self.no_of_selected_features) 

# Selection of classifiers  
     def classification_pipeline(self):    
   
   # AdaBoost 
        if self.clf_opt=='ab':
            print('\n\t### Training AdaBoost Classifier ### \n')
            #be1 = svm.SVC(kernel='linear', class_weight='balanced',probability=True)              
            be2 = LogisticRegression(solver='liblinear',class_weight='balanced') 
            be3 = DecisionTreeClassifier(max_depth=20)
#            clf = AdaBoostClassifier(algorithm='SAMME',n_estimators=100)            
            clf = AdaBoostClassifier(algorithm='SAMME.R',n_estimators=100)
            clf_parameters = {
            'clf__base_estimator':(be2,be3),
            'clf__random_state':(0,10),
            }      
    # Decision Tree
        elif self.clf_opt=='dt':
            print('\n\t### Training Decision Tree Classifier ### \n')
            clf = DecisionTreeClassifier(random_state=40) 
            clf_parameters = {
            'clf__criterion':('gini', 'entropy'), 
            'clf__max_features':('auto', 'sqrt', 'log2'),
            'clf__max_depth':(10,40,45,60),
            'clf__ccp_alpha':(0.009,0.01,0.05,0.1),
            } 
    # Logistic Regression 
        elif self.clf_opt=='lr':
            print('\n\t### Training Logistic Regression Classifier ### \n')
            clf = LogisticRegression(class_weight='balanced') 
            clf_parameters = {
            'clf__solver':('lbfgs','liblinear'),
            'clf__random_state':(0,10),
            } 
    # Multinomial Naive Bayes
        elif self.clf_opt=='nb':
            print('\n\t### Training Multinomial Naive Bayes Classifier ### \n')
            clf = MultinomialNB(fit_prior=True, class_prior=None)  
            clf_parameters = {
            'clf__alpha':(0,1),
            }            
    # Random Forest 
        elif self.clf_opt=='rf':
            print('\n\t ### Training Random Forest Classifier ### \n')
            clf = RandomForestClassifier(max_features=None,class_weight='balanced')
            clf_parameters = {
            'clf__criterion':('entropy','gini'),       
            'clf__n_estimators':(30,50),
            'clf__max_depth':(10,20,30,50),
            }          
    # Support Vector Machine  
        elif self.clf_opt=='svm': 
            print('\n\t### Training SVM Classifier ### \n')
            clf = svm.SVC(class_weight='balanced',probability=True)  
            clf_parameters = {
            'clf__C':(0.1,0.2),
            'clf__kernel':('linear','rbf'), 
            }
            
            
        elif self.clf_opt == 'knn':
            print('\n\t### Training K-Nearest Neighbors Classifier ### \n')
            clf = KNeighborsClassifier()
            clf_parameters = {
                'clf__n_neighbors': (3, 5, 10),
                'clf__weights': ('uniform', 'distance'),
                'clf__p': (1, 2),  # 1 for Manhattan distance, 2 for Euclidean distance
            }
            
            
                    
        else:
            print('Select a valid classifier \n')
            sys.exit(0)        
        return clf,clf_parameters    
 
 
 
# Statistics of individual classes
     def get_class_statistics(self,labels):
        class_statistics=Counter(labels)
        print('\n Class \t\t Number of Instances \n')
        for item in list(class_statistics.keys()):
            print('\t'+str(item)+'\t\t\t'+str(class_statistics[item]))
       
# Load the data 
     def get_data(self,filename):
      
        reader=pd.read_csv(self.path+filename)  
        
   
        
        data=reader.iloc[:, :-1]
        labels=reader['target']

        self.get_class_statistics(labels)          

        return data, labels
    
    
    
    
    
    
    
    
    
    
 
        
        
        
        
        
        
        
        
   
     def classification(self):  
   # Get the data
        data,labels=self.get_data('now_train.csv')
        data=np.asarray(data)

# Experiments using training data only during training phase (dividing it into training and validation set)
        skf = StratifiedKFold(n_splits=4)
        predicted_class_labels=[]; actual_class_labels=[]; 
        count=0; probs=[];
        for train_index, test_index in skf.split(data,labels):
            X_train=[]; y_train=[]; X_test=[]; y_test=[]
            for item in train_index:
                X_train.append(data[item])
                y_train.append(labels[item])
            for item in test_index:
                X_test.append(data[item])
                y_test.append(labels[item])
            count+=1                
            print('Training Phase '+str(count))
            
            
            
            #print ('\n\n\n')
            #print('training data',train_index)
            #print ('\n\n\n')
            #print('test data',test_index)
            #print ('\n\n\n')
            
            
            
            
            clf,clf_parameters=self.classification_pipeline()
            pipeline = Pipeline([
                    #   ('feature_selection', SelectKBest(f_classif, k=self.no_of_selected_features)),    
                  #      ('feature_selection', SelectKBest(chi2, k=self.no_of_selected_features)),                                      
                      ('feature_selection', SelectKBest(mutual_info_classif, k=self.no_of_selected_features)),        
                        ('clf', clf),])
            grid = GridSearchCV(pipeline,clf_parameters,scoring='f1_macro',cv=10)          
            grid.fit(X_train,y_train)     
            clf= grid.best_estimator_  
                 
                 
                 
                 
           





            predicted = clf.predict(X_test)                 
            predicted=clf.predict(X_test)  
            #print(predicted)
            predicted_probability = clf.predict_proba(X_test) 
            
            for item in predicted_probability:
                probs.append(float(max(item)))
            for item in y_test:
                actual_class_labels.append(item)
            for item in predicted:
                predicted_class_labels.append(item)           
        confidence_score=statistics.mean(probs)-statistics.variance(probs)
        confidence_score=round(confidence_score, 3)
        print ('\n The Probablity of Confidence of the Classifier: \t'+str(confidence_score)+'\n') 
       
    # Evaluation
        class_names=list(Counter(labels).keys())
        class_names = [str(x) for x in class_names] 
        #print('\n\n The classes are: ')
        #print(class_names)      
       
        print('\n ##### Classification Report on Training Data ##### \n')
        print(classification_report(actual_class_labels, predicted_class_labels, target_names=class_names))        
                
        pr=precision_score(actual_class_labels, predicted_class_labels, average='macro') 
        print ('\n Precision:\t'+str(pr)) 
        
        rl=recall_score(actual_class_labels, predicted_class_labels, average='macro') 
        print ('\n Recall:\t'+str(rl))
        
        fm=f1_score(actual_class_labels, predicted_class_labels, average='macro') 
        print ('\n F1-Score:\t'+str(fm))
        
        # Experiments on Given Test Data during Test Phase
        if confidence_score>0.80:
            print('\n ***** Classifying Test Data ***** \n')   
            predicted_cat=[];
  
            data1=pd.read_csv('encoded_test.csv') 
            tst_data=np.asarray(data1)
            predicted=clf.predict(tst_data)
            print('\n ##### Classification Report on test data ##### \n')
            #print(data1) 
            
            
            
            
            csv_file_path = 'test_result_lr.csv'
            with open(csv_file_path, 'w', newline='') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 csv_writer.writerow(['prdctd_lbls'])  
                 for value in predicted:
                     csv_writer.writerow([value])

            
            lowercase_predicted = np.char.lower(predicted)
            string_to_count_1 = "LGG"
            string_to_count_2 = "GBM"
            count_1 = np.count_nonzero(lowercase_predicted == string_to_count_1.lower())
            count_2 = np.count_nonzero(lowercase_predicted == string_to_count_2.lower())
            print(f"no. of instances for '{string_to_count_1}': {count_1}")
            print(f"no. of instances for '{string_to_count_2}': {count_2}")

            
            
            
            
        else:   
            '''print("\n\n ******* The classifier's condidence score ("+ str(confidence_score)+") is poor ******* \n")'''
            
            
            
            
            
                      
    
import warnings
warnings.filterwarnings("ignore")


clf=classification('/home/ttarun/Downloads/mlp5/', clf_opt='lr',
                        no_of_selected_features=10)

clf.classification()            
            






































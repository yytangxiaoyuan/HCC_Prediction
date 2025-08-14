library(readxl)
library(glmnet)
library(survival)
library(survcomp)
library(timeROC)
library(survex)
library(openxlsx)

set.seed(6699)

train_feature <- read_excel(
  sprintf("./UniCOXRegressFeatureSelect/train_feature.xlsx", as.character(i)), 
  sheet="Sheet1")

features <- as.matrix(train_feature[, 4:ncol(train_feature)])
targets <- Surv(train_feature$Time, train_feature$Event)

params <- cv.glmnet(features, targets, family='cox', nfold=10, alpha=1, intercept=FALSE)
best_lambda <- params$lambda.min

lasso_model <- glmnet(features, targets, family='cox', alpha=1, lambda=best_lambda, intercept=FALSE)

coef_matrix <- coef(lasso_model)
selected_features <- which(coef_matrix != 0)
coefficients <- coef_matrix[selected_features]
selected_feature_names <- names(train_feature[, 4:ncol(train_feature)])[selected_features]

train_selected_feature_values <- features[,selected_features]
train_lasso_cox_scores <- train_selected_feature_values %*% coefficients
train_C_index <- concordance.index(x=train_lasso_cox_scores, 
                                   surv.time = train_feature$Time, 
                                   surv.event = train_feature$Event, 
                                   method = "noether")


valid_feature <- read_excel(
  sprintf("./UniCOXRegressFeatureSelect/valid_feature_%s.xlsx", as.character(i)), 
  sheet="Sheet1")
features <- as.matrix(valid_feature[, 4:ncol(valid_feature)])
targets <- Surv(valid_feature$Time, valid_feature$Event)

valid_selected_feature_values <- features[,selected_features]
valid_lasso_cox_scores <- valid_selected_feature_values %*% coefficients
valid_C_index <- concordance.index(x=valid_lasso_cox_scores, 
                                   surv.time = valid_feature$Time,
                                   surv.event = valid_feature$Event, 
                                   method = "noether")

C2_feature <- read_excel(
  sprintf("./UniCOXRegressFeatureSelect/C2_feature_%s.xlsx", as.character(i)), 
  sheet="Sheet1")
features <- as.matrix(C2_feature[, 4:ncol(C2_feature)])
targets <- Surv(C2_feature$Time, C2_feature$Event)

C2_selected_feature_values <- features[,selected_features]
C2_lasso_cox_scores <- C2_selected_feature_values %*% coefficients
C2_C_index <- concordance.index(x=C2_lasso_cox_scores, surv.time = C2_feature$Time, 
                             surv.event = C2_feature$Event, method = "noether")

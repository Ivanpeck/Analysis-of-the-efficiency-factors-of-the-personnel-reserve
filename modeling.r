library(glmnet)
library(writexl)
library(readxl)
library(dplyr)     # включает %>%
library(tibble)  # или library(dplyr)


rating_binar <- -1 # тут меняем: один раз прогоняем 1, один раз -1
# 1) Загрузка данных
if (rating_binar == 1) {data <- read_excel("X_y для R_plus1.xlsx", sheet = "Sheet1")}
if (rating_binar == -1) {data <- read_excel("X_y для R_minus1.xlsx", sheet = "Sheet1")}
# 2) Подготовка матрицы X и вектора y
x <- as.matrix(data[, setdiff(names(data), "y")])
y <- data[["y"]]

# ===== 3)

p <- ncol(x)
lower <- rep(-Inf, p)
upper <- rep( Inf, p)

# Индексы, где beta[0] — интерсепт, поэтому дальше сдвигаем на -1
pos_idx_py <- c(1,3,4,5,7,9,10,13,14,16,17,19)
neg_idx_py <- c(2,6,8,11,12,15,18,20)

# В glmnet индексы для признаков: 1..p, соответствуют beta[1]..beta[p].
# Значит r-индексы = k-1. Отфильтруем индексы, которые выходят за p (на всякий случай).
r_pos <- c(1,3,4,5,7,9,10,13,14,16,17,19)  # beta[k] >= 0
r_neg <- c(2,6,8,11,12,15,18,20)

if (rating_binar == 1) {
  # beta[k] >= 0
  if (length(r_pos)) lower[r_pos] <- pmax(lower[r_pos], 0)
  # beta[k] <= 0
  if (length(r_neg)) upper[r_neg] <- pmin(upper[r_neg], 0)
}
if (rating_binar == -1) {
  # beta[k] >= 0
  if (length(r_neg)) lower[r_neg] <- pmax(lower[r_neg], 0)
  # beta[k] <= 0
  if (length(r_pos)) upper[r_pos] <- pmin(upper[r_pos], 0)
}


fit <- cv.glmnet(
  x, y,
  family = "binomial",
  alpha = 0.5,                 # чистый Ridge (без L1), при λ → 0 штраф исчезающе мал
  standardize = FALSE,       # чтобы цель совпадала с вашей без стандартизации
  intercept = TRUE,
  lower.limits = lower,
  upper.limits = upper
)
coefs <- coef(fit, s = "lambda.min")
print(fit$lambda.min)
model_glmnet_coef <- coef(
  fit,
  s = "lambda.min"
) %>% 
  as.matrix() %>% 
  as.data.frame() %>% 
  rename("value"=1) %>% 
  rownames_to_column("var")


# Преобразуем в data.frame для записи
coefs_df <- data.frame(
  Feature = rownames(as.matrix(coefs)),
  Coefficient = as.numeric(coefs)
)

# 2) Сохраняем в Excel
if (rating_binar == 1) {write_xlsx(coefs_df, "coefs_plus1.xlsx")}
if (rating_binar == -1) {write_xlsx(coefs_df, "coefs_minus1.xlsx")}
/library(tidyverse)
library(ggplot2)
library(reshape2)
library(readxl)

data_m <- read.csv2("C:/Users/vajma/Desktop/Prezentacije genos/Tecan paper/Data_manual.csv")
data_a <- read.csv2("C:/Users/vajma/Desktop/Prezentacije genos/Tecan paper/Data_auto.csv")
data_avg <- read.csv2("C:/Users/vajma/Desktop/Prezentacije genos/Tecan paper/Data_avg.csv")
data_graph <- read.csv2("C:/Users/vajma/Desktop/Prezentacije genos/Tecan paper/Data_graph.csv")

# Calculate coefficients of variation for each column in sample sets
for (i in 1:24) {
  # Convert column to numerical data
  data_m[paste0("GP", 1:24)] <- lapply(data_m[paste0("GP", 1:24)], as.numeric)
}

for (i in 1:24) {
  # Convert column to numerical data
  data_a[paste0("GP", 1:24)] <- lapply(data_a[paste0("GP", 1:24)], as.numeric)
}

cv_m <- numeric(24)

# Iterate through the manual variables
for (i in 1:24) {
  # Calculate standard deviation
  sd_value <- sd(data_m[,paste0("GP", i)])
  # Calculate mean
  mean_value <- mean(data_m[,paste0("GP", i)])
  # Calculate coefficient of variation
  cv_m[i] <- (sd_value / mean_value) * 100
}

# Iterate through the manual variables remove outliers
for (i in 1:24) {
  # Remove outliers
  data_m_filtered <- data_m[,paste0("GP", i)][abs(data_m[,paste0("GP", i)] - mean(data_m[,paste0("GP", i)])) <= 3*sd(data_m[,paste0("GP", i)])]
  # Calculate standard deviation
  sd_value <- sd(data_m_filtered)
  # Calculate mean
  mean_value <- mean(data_m_filtered)
  # Calculate coefficient of variation
  cv_m[i] <- (sd_value / mean_value) * 100
}

cv_a <- numeric(24)


# Iterate through the automated variables
for (i in 1:24) {
  # Calculate standard deviation
  sd_value <- sd(data_a[,paste0("GP", i)])
  # Calculate mean
  mean_value <- mean(data_a[,paste0("GP", i)])
  # Calculate coefficient of variation
  cv_a[i] <- (sd_value / mean_value) * 100
}

# Iterate through the automated variables remove outliers
for (i in 1:24) {
  # Remove outliers
  data_a_filtered <- data_a[,paste0("GP", i)][abs(data_a[,paste0("GP", i)] - mean(data_a[,paste0("GP", i)])) <= 3*sd(data_a[,paste0("GP", i)])]
  # Calculate standard deviation
  sd_value <- sd(data_a_filtered)
  # Calculate mean
  mean_value <- mean(data_a_filtered)
  # Calculate coefficient of variation
  cv_a[i] <- (sd_value / mean_value) * 100
}

# Create data frame of coefficients of variation for each sample set
cv_df <- data.frame(sample1 = cv_m, sample2 = cv_a)

# Create a data frame containing the two variables
data_frame <- data.frame(GP = paste0("GP", 1:24), cv_m = cv_m, cv_a = cv_a)

data_frame$GP <- factor(data_frame$GP, levels = paste0("GP", 1:24))


data_frame_new_long <- data_frame %>% gather(Method, Value, -GP)
data_frame_new_long$GP <- factor(data_frame_new_long$GP, levels = paste0("GP", 1:24))

ggplot(data_frame_new_long, aes(x = reorder(GP, GP), y = Value, fill = Method)) +
  geom_col(position = "dodge") +
  xlab("GP") +
  ylab("Coefficient of Variation (%)") +
  ggtitle("Comparison of CV between Manual and Automated Methods") + 
  scale_fill_manual(values = c("cv_m" = "#f9756c", "cv_a" = "#00c0c4"), labels = c("Automated", "Manual"))+
  scale_color_manual(values = c("cv_m" = "#f9756c", "cv_a" = "#00c0c4"), labels = c("Automated", "Manual")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))+
  theme(plot.title = element_text(size=19,hjust = 0.5))


data_avg$Avg <- as.numeric(data_avg$Avg)
data_avg$GP <- factor(data_avg$GP, levels = paste("GP", 1:24, sep = ""))

ggplot(data_avg, aes(x = GP, y = Avg)) +
  geom_bar(stat = "identity", position = "dodge", width = 0.7) +
  ggtitle("Average relative glycan abundance for plasma standards") + 
  xlab("Glycan Peak") +
  ylab("Relative glycan abundance(%)")+
  theme(plot.title = element_text(size=19,hjust = 0.5))

# melted data_a to long format
data_a_long <- data_a %>% 
  gather(GP, cv, GP1:GP24) %>% 
  mutate(method = "cv_a")

# melted data_m to long format
data_m_long <- data_m %>% 
  gather(GP, cv, GP1:GP24) %>% 
  mutate(method = "cv_m")

# combined data_a_long and data_m_long
data_frame_new_long <- rbind(data_a_long, data_m_long)
data_frame_new_long$GP <- factor(data_frame_new_long$GP, levels = unique(data_avg$GP))

# plot
ggplot(data_frame_new_long, aes(x = GP, y = cv)) +
  geom_bar(stat = "identity", position = "dodge", width = 0.7) +
  geom_errorbar(aes(x = GP, ymin=cv, ymax=cv, color = method),
                position = position_dodge(width = 0.7),
               width = 0.2) +
  xlab("Glycan Peak") +
  ylab("Relative abundance(%)") +
  scale_color_manual(values = c("#00c0c4", "#f9756c"), 
                     labels = c("Automated", "Manual")) +
  theme(legend.position = "right", 
        legend.title = element_blank(), 
        legend.text = element_text(face = "bold")) +
  guides(fill = "none", color = guide_legend(override.aes = list(fill = "grey")))


data_graph[paste0("Avg")] <- lapply(data_graph[paste0("Avg")], as.numeric)
data_graph[paste0("cv")] <- lapply(data_graph[paste0("cv")], as.numeric)
data_graph[paste0("sd")] <- lapply(data_graph[paste0("sd")], as.numeric)



#Order plot
data_graph$GP <- factor(data_graph$GP, levels = paste("GP", 1:24, sep = ""))

#plot
ggplot(data_graph, aes(x = GP , y = Avg, fill = method)) +
  geom_col(position = "dodge") +
  geom_errorbar(aes(x = GP, ymin=Avg+sd, ymax=Avg-sd),
                position = position_dodge(width = 0.95),
                size=1,
                width = 0.2) +
  xlab("Glycan peak") +
  ylab("Relative abundance (%)") +
  scale_fill_manual(name = "Method", values = c("cv_m" = "#f9756c", "cv_a" = "#00c0c4"), labels = c("Automated", "Manual")) +
  scale_color_manual(name = "Method", values = c("cv_m" = "#f9756c", "cv_a" = "#00c0c4"), labels = c("Automated", "Manual")) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, size = 12, face = "bold"),
        axis.text.y = element_text(size = 12, face = "bold"),
        axis.title.x = element_text(size = 18, face = "bold"),
        axis.title.y = element_text(size = 18, face = "bold"),
        legend.title = element_text(size = 18, face = "bold"),
        legend.text = element_text(size = 16, face = "bold"))#+
  # facet_wrap(~GP, scales = "free")

#boxplots of standards
boxplot_data <- rbind(mutate(data_a, st_name = paste0("ST", formatC(1:24, width = 2, flag = '0')), method = "a"),
                             mutate(data_m, st_name = paste0("ST", formatC(1:24, width = 2, flag = '0')), method = "m"))
boxplot_data <- pivot_longer(boxplot_data, cols = GP1:GP24, names_to = "glycan", values_to = "narea")
boxplot_data$glycan <- factor(boxplot_data$glycan, levels = paste("GP", 1:24, sep = ""))

ggplot(boxplot_data, aes(x = method, y = narea))+
  geom_boxplot(aes(fill = method))+
  facet_wrap(~glycan, scales = "free")+
  guides(fill = "none")

######################################

# This script:
# - imports measures data
# - plot deciles charts

######################################


# Preliminaries ----

## Import libraries
library('tidyverse')
library('lubridate')
library('reshape2')
library('here')
library('patchwork')

## Create output directory
dir.create(here::here("output", "figures"), showWarnings = FALSE, recursive=TRUE)

## Decile plot function
plot_decile <- function(data = data, ylab = "ylab") {

ggplot(data, aes(x = date, y = value)) +
  geom_line(aes(group = quantile, linetype = label, size = label), colour = "blue") +
  theme_bw() +
  theme(legend.title = element_blank(), legend.box.background = element_rect(colour = "black")) +
  scale_linetype_manual("Variabler",values=c("median" = 1 ,"decile" = 2)) +
  scale_size_manual(breaks=c("median","decile"), values=c(1,0.5)) +
  guides(size = "none") +
  scale_x_date(date_breaks = "3 month", date_labels =  "%b %Y") +
  theme(axis.text.x=element_text(angle=60, hjust=1)) +
  ylab(ylab) +
  xlab("")
  
}

## Import data
measures_broad_spectrum <- read_csv(
  here::here("output", "measures", "measure_broad_spectrum_proportion.csv"),
  col_types = cols_only(
    
    # Identifier
    practice = col_integer(),
    
    # Outcomes
    broad_spectrum_antibiotics_prescriptions = col_double(),
    antibacterial_prescriptions = col_double(),
    value = col_double(),
    
    # Date
    date = col_date(format="%Y-%m-%d")
    
  ),
  na = character()
  )

measures_trimethoprim <- read_csv(
  here::here("output", "measures", "measure_trimethoprim_prescriptions.csv"),
  col_types = cols_only(
    
    # Identifier
    practice = col_integer(),
    
    # Outcomes
    trimethoprim_prescriptions = col_double(),
    nitrofurantoin_and_trimethoprim_prescriptions = col_double(),
    value = col_double(),
    
    # Date
    date = col_date(format="%Y-%m-%d")
    
  ),
  na = character()
)


# Calculate deciles ----
data_plot_brad_spectrum <- measures_broad_spectrum %>%
  group_by(date) %>%  
  summarise(quantile = scales::percent(c(seq(0, 1, by = 0.1))),
            value = quantile(value, c(seq(0, 1, by = 0.1)), na.rm = T)) %>%
  mutate(label = ifelse(quantile == "50.0%", "median", "decile")) %>%
  mutate(date = as.Date(date, format = "%Y-%m-%d"))

data_plot_trimethoprim <- measures_broad_spectrum %>%
  group_by(date) %>%  
  summarise(quantile = scales::percent(c(seq(0, 1, by = 0.1))),
            value = quantile(value, c(seq(0, 1, by = 0.1)), na.rm = T)) %>%
  mutate(label = ifelse(quantile == "50.0%", "median", "decile")) %>%
  mutate(date = as.Date(date, format = "%Y-%m-%d"))

# Figures ----

## Broad spectrum antibiotics
decile_plot_measures_broad_spectrum <- plot_decile(data = data_plot_brad_spectrum, 
                                                   ylab = "Proportion of broad spectrum antibiotic prescriptions (out of all antibiotic prescriptions)")

### Trimethoprim
decile_plot_measures_trimethoprim <- plot_decile(data = data_plot_trimethoprim, 
                                                   ylab = "Measure of trimethoprim as a proportion of prescribing of nitrofurantoin and trimethoprim")






prochlorperazine <-  ggplot(data_incident_groups, aes(x = date, y = prochlorperazine, colour = group, linetype = `Number of patients with first prescriptions`)) +
  geom_line() +
  facet_wrap(~group, scales = "free") +
  theme_bw() +
  theme(legend.position = "bottom") +
  guides(colour=FALSE, linetype = guide_legend(nrow = 2)) +
  ylab("Total number of patients issued first prescription of \n prochlorperazine antipsychotics, per month") +
  xlab("") +
  scale_x_date(date_breaks = "3 month", date_labels =  "%b %Y") +
  theme(axis.text.x = element_text(angle = 60, hjust = 1))

ggsave(filename=here::here("output", "figures", "plot_first_prochlorperazine.svg"),
       prochlorperazine,
       units = "cm", width = 40, height = 20
)

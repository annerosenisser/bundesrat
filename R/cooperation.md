<!-- see 
http://stackoverflow.com/questions/31914161/how-to-convert-rmd-into-md-in-r-studio
for how to render .Rmd to .md (to push to github). -->
This file analyses the data collected on sessions of the German
Bundesrat (Federal Council). I use data that I collected with a
Python-based webscraper (combining
[Selenium](http://selenium-python.readthedocs.io) and
[scrapy](https://scrapy.org)). You find my code
[here](https://github.com/annerosenisser/bundesrat/tree/master/bundesrat).

More specifically, it asks two questions:

1.  Which are the committees involved in the decision-making process?
    Which are the most important committees?

2.  Which committees tend to cooperate most?

### Data preparation

I'm reading in the data that I collected with the scraper:

    getwd()

    ## [1] "/Users/Annerose/Documents/15-16/Code/bundesrat/R"

    # yourpath <- "/Users/Annerose/Documents/15-16/Code/bundesrat"
    # setwd(yourpath)
    bundesrat <- read.csv("bundesrat_2014-16.csv")

I then make sure that the data is read in correctly:

    names(bundesrat)
    head(bundesrat)

### Which are the important committees?

In the dataset, each decision of the German Bundesrat is saved in one
row. The committees involved in a given decision are coded as dummy
variables. This signifies that I can easily table in how many decisions
each committee was involved during the time period of observation
(2014-2016):

    for (i in names(bundesrat)[1:15]) {bundesrat[, i] <- as.integer(bundesrat[, i])}
    t <- apply(bundesrat[, c(1:15)], 2, sum, na.rm = T)
    t <- sort(t, decreasing = T)
    barplot(t, xlab = "Committees", ylab = "# Decisions involved", 
            main = "Number of Decisions per Committee in the German Bundesrat")
    labels <- c("Wi: Economy", "Fz: Finances", "In: Internal", "R: Law", "EU: EU affairs", 
                "U: Environment", "AV: Agriculture, Consumer", "Vk: Transport", "G: Health", "K: Culture",
                "AIS: Work, Integration, Social", "FJ: Family, Youth",
                "Wo: Housing", "V: Defense", "AA: Foreign")
    legend("topright", labels, cex = 0.6)

![](cooperation_files/figure-markdown_strict/unnamed-chunk-3-1.png)

It seems that the economic ("Wi"), financial ("Fz") and domestic polity
("In") committees are clearly the most important ones, i.e. those
involved in the largest number of decisions.

But has there been a temporal trend in the importance of committees? To
examine this, I run the analysis separately per year.

First, I create a function that will transform and then plot the
relevant data (I call this function `bplotfun`):

    bplotfun <- function(df, ... ) {
      df <- df[, c(1:15)]
      t <- apply(df, 2, sum, na.rm = T)
      t <- sort(t, decreasing = T)
      barplot(t, xlab = "Committees", ylab = "# Decisions involved", 
            # cex.axis = 0.5, 
            las = 2, # turn the axis labels
            ...)
    }

Then I "feed" the function with the relevant data:

    # Make three panes to plot the barplots: 
    par(mfrow=c(1,3))

    for (i in seq(2014, 2016)) {
      bplotfun(df = bundesrat[bundesrat$year==i, ], main = as.character(i))
    }

![](cooperation_files/figure-markdown_strict/unnamed-chunk-5-1.png)

As the three figures indicate, the economics committee has been the most
important one throughout all three years. However, it is interesting to
note that the EU committee was more important than the finance committee
in 2016 -- this might be explained by the Brexit referendum in June 2016
(?).

### Which committees cooperate most?

To examine which committees cooperate most, I first rely on a simple
covariation matrix:

    m <- round(cor(bundesrat[, c(1:15)], use = "pairwise.complete.obs", 
        method = "pearson"), 3)
    head(m, 5)

    ##         AA    AIS     AV     EU     FJ     Fz      G     In      K      R
    ## AA   1.000 -0.030 -0.017  0.004 -0.023  0.005 -0.021  0.058 -0.029 -0.006
    ## AIS -0.030  1.000  0.246  0.089  0.143  0.085  0.136 -0.062 -0.031 -0.023
    ## AV  -0.017  0.246  1.000  0.001  0.086  0.146  0.191  0.126 -0.080  0.005
    ## EU   0.004  0.089  0.001  1.000 -0.028 -0.040 -0.049 -0.141 -0.101 -0.026
    ## FJ  -0.023  0.143  0.086 -0.028  1.000 -0.005 -0.020 -0.094  0.052 -0.032
    ##          U      V     Vk     Wi     Wo
    ## AA   0.006 -0.023 -0.012 -0.071  0.017
    ## AIS -0.018  0.173  0.053 -0.332  0.068
    ## AV  -0.092  0.005 -0.012 -0.099  0.007
    ## EU  -0.061  0.095  0.024 -0.090  0.074
    ## FJ  -0.045  0.029  0.005 -0.064 -0.045

It's difficult to see any pattern from this large table (of which only
parts are displayed above). Therefore, I opt instead for a correlation
plot. You need to have `corrplot` installed to run this. If not, run
`install.packages("corrplot")` to get the package. For more information
on the package, see
[here](http://www.sthda.com/english/wiki/visualize-correlation-matrix-using-correlogram).

    require(corrplot)

    ## Loading required package: corrplot

    corrplot(m, method = "color")

![](fig-unnamed-chunk-7-1.png)

It's still pretty hard to see any pattern in this plot. I see two issues
with this plot:

1.  Correlations are on average very low, so it's hard to see any
    nuances.

2.  The data isn't ordered in increasing or decreasing order of
    correlation strength.

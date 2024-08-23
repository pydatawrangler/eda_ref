library(ggplot2)

mpg

ggplot(mpg, aes(x = displ, y = hwy)) +
    geom_point()

ggplot(mpg, aes(displ, hwy, color = class)) +
    geom_point()

ggplot(mpg, aes(displ, hwy)) +
    geom_point() +
    facet_wrap(~class)

ggplot(mpg, aes(displ, hwy)) +
    geom_point() +
    geom_smooth()

ggplot(mpg, aes(drv, hwy)) + geom_boxplot()

ggplot(mpg, aes(hwy)) + geom_histogram()

economics

ggplot(economics, aes(date, uempmed)) +
    geom_line()

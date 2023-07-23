# Chapter 10

library(tidyverse)

mpg

ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point()

ggplot(mpg, aes(x = displ, y = hwy, shape = class)) +
  geom_point()

ggplot(mpg, aes(x = displ, y = hwy, size = class)) +
  geom_point()

ggplot(mpg, aes(x = displ, y = hwy, alpha = class)) +
  geom_point()

# 10.2.1 Exercises

# 1
ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(shape = 17, color= "pink")

# 2
ggplot(mpg, color = 'blue') +
  geom_point(aes(x = displ, y = hwy)) # , fill = "blue"))

# 3
?geom_point

# 4
ggplot(mpg, aes(x = displ, y = hwy, color = displ < 5)) +
  geom_point()

# 10.3 Geometric objects

ggplot(mpg, aes(x = displ, y = hwy, linetype = drv)) +
  geom_smooth()

ggplot(mpg, aes(x = displ, y = hwy, color = drv)) +
  geom_point() +
  geom_smooth(aes(linetype = drv))

ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(aes(color = class)) +
  geom_smooth()

ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point() +
  geom_point(
    data = mpg |> filter(class == "2seater"),
    color = "red"
  ) +
  geom_point(
    data = mpg |> filter(class == "2seater"),
    shape = "circle open", size = 3, color = "red"
  )

ggplot(mpg, aes(x = hwy)) +
  geom_histogram(binwidth = 2)

ggplot(mpg, aes(x = hwy)) +
  geom_density()

ggplot(mpg, aes(x = hwy)) +
  geom_boxplot()

library(ggridges)

ggplot(mpg, aes(x = hwy, y = drv, fill = drv, color = drv)) +
  geom_density_ridges(alpha = 0.5, show.legend = FALSE)

ggplot(mpg, aes(x = hwy, y = displ, color = drv)) +
  geom_line()

ggplot(mpg, aes(x = displ, y = hwy, stroke = 1, fill = drv)) +
  geom_point(shape = 21, color = "white")

# 10.4 Facets

ggplot(mpg |> mutate(year = factor(year)), aes(x = displ, y = hwy, color = year)) +
  geom_point() +
  facet_wrap(~cyl)

ggplot(mpg |> mutate(year = factor(year)), aes(x = displ, y = hwy, color = year)) +
  geom_point() +
  facet_grid(drv ~ cyl, scales = "free_y")

# 10.4.1 Exercises

ggplot(mpg, aes(x = displ, y = hwy, color = year)) +
  geom_point() +
  facet_wrap(~drv)

ggplot(mpg) +
  geom_point(aes(x = drv, y = cyl))

ggplot(mpg) +
  geom_point(aes(x = displ, y = hwy)) +
  facet_grid(drv ~ .)

ggplot(mpg) +
  geom_point(aes(x = displ, y = hwy)) +
  facet_grid(. ~ cyl)

ggplot(mpg) + 
  geom_point(aes(x = displ, y = hwy)) + 
  facet_wrap(~ class, nrow = 2)

ggplot(mpg, aes(x = displ)) + 
  geom_histogram() + 
  facet_grid(drv ~ .)

ggplot(mpg, aes(x = displ)) + 
  geom_histogram() +
  facet_grid(. ~ drv)

# 10.5 Statistical transformations

ggplot(diamonds, aes(x = cut)) +
  geom_bar()

?geom_point

diamonds |>
  count(cut)

?after_stat

ggplot(diamonds, aes(x = cut, y = after_stat(prop), group = 5)) +
  geom_bar()

ggplot(diamonds, aes(x = cut, y = after_stat(prop), fill = color, group = 1)) + 
  geom_bar()
ggplot(diamonds, aes(x = cut, fill = color)) + 
  geom_bar()

ggplot(diamonds) +
  stat_summary(
    aes(x = cut, y = depth),
    fun.min = min,
    fun.max = max,
    fun = median
  )

?stat_summary

ggplot(diamonds, aes(x = cut, y = depth)) +
  geom_pointrange(aes(ymin = depth, ymax = depth))

?geom_pointrange

# 10.6 Position adjustments

ggplot(mpg, aes(x = drv, fill = class)) +
  geom_bar(position = "dodge")

ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(position = "jitter")

# 10.6.1 Exercises

ggplot(mpg, aes(x = cty, y = hwy, color = class)) + 
  geom_point() +
  facet_wrap(~class)

# 10.7 Coordinate Systems

nz <- map_data("nz")

ggplot(nz, aes(x = long, y = lat, group = group)) +
  geom_polygon(fill = "white", color = "black") +
  coord_quickmap()

bar <- ggplot(data = diamonds) +
  geom_bar(
    mapping = aes(x = clarity, fill = clarity),
    show.legend = FALSE,
    width = 1
  ) +
  theme(aspect.ratio = 1)

bar + coord_polar()

ggplot(data = mpg, mapping = aes(x = cty, y = hwy)) +
  geom_point() + 
  geom_abline() +
  coord_fixed()

library(tidyverse)

library(palmerpenguins)
library(ggthemes)

penguins
df <- penguins

glimpse(penguins)
View(penguins)

ggplot(
  data = penguins,
  mapping = aes(x = flipper_length_mm, y = body_mass_g)
  ) +
  geom_point(mapping = aes(color = species, shape = species)) +
  geom_smooth() +
  labs(
    title = "Body mass and flipper length",
    subtitle = "Dimensions for Adelie, Chinstrap, and Gentoo Penguins",
    x = "Flipper length (mm)", y = "Body mass (g)",
    color = "Species", shape = "Species",
    caption = "Data come from the palmerpenguins package."
  ) +
  scale_color_colorblind()

ggplot(
  data=penguins,
  mapping=aes(x=bill_length_mm, y=bill_depth_mm)
) +
  geom_point()

ggplot(
  data=penguins,
  mapping=aes(x=flipper_length_mm, y=body_mass_g)
) +
  geom_point(mapping=aes(color=bill_depth_mm)) +
  geom_smooth()

ggplot() +
  geom_point(
    data=penguins,
    mapping=aes(x=flipper_length_mm, y=body_mass_g)
  ) +
  geom_smooth(
    data=penguins,
    mapping=aes(x=flipper_length_mm, y=body_mass_g),
    se=FALSE
  )

# thru Section 2.2
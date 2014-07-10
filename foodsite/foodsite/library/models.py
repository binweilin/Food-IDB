from django.db import models

class Region(models.Model):
    """
    A class to represent regions of the word
    Has a one-to-many relationship with Recipe and with Chef
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    google_map = models.TextField()
    # how to represent recipes for region, also chefs?

    def __str__(self):
        return self.name


class Chef(models.Model):
    """
    A class to represent famous chefs hailing from various regions of the world
    Has a many-to-one relationship with Region
    Has a one-to-many relationship with Recipe
    """
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region)
    birth_place = models.CharField(max_length=50)
    birth_date = models.DateField()
    #recipes?
    youtube = models.TextField()
    twitter = models.TextField()
    bio = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    A class to represent recipes for regional foods
    Has a many-to-one relationship with Region and with Chef
    """
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region)
    chef = models.ForeignKey(Chef)
    ingredients = models.TextField()
    instructions = models.TextField()
    time_needed = models.CharField(max_length=10)
    DIFFICULTY_LEVELS = (
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    )
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_LEVELS)
    dish_type = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.


class Autor(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to="autores", null=True, blank=True)
    origen = models.CharField(max_length=30)
    nacimiento = models.DateField()

    class Meta:
        verbose_name = 'autor'
        verbose_name_plural = 'autores'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'genero'
        verbose_name_plural = 'generos'

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    nombre = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    precio = models.FloatField()
    editorial = models.CharField(max_length=50)
    fecha = models.IntegerField()
    imagen = models.ImageField(upload_to="libros", null=True, blank=True)

    class Meta:
        verbose_name = 'libro'
        verbose_name_plural = 'libros'

    def __str__(self):
        return self.nombre









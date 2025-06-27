from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    class Meta:
        db_table = 'categoria'
        managed = False

    def __str__(self):
        return self.nombre

class Tiempo(models.Model):
    tiempo = models.IntegerField()

    class Meta:
        db_table = 'tiempo'
        managed = False

    def __str__(self):
        return f"{self.tiempo} segundos"


class Bancopregunta(models.Model):
    idcategoria = models.ForeignKey(
        Categoria,
        models.DO_NOTHING,
        db_column='IdCategoria',
        blank=True,
        null=True
    )
    tiempo = models.ForeignKey(
        Tiempo,
        models.DO_NOTHING,
        db_column='tiempo_id',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'bancopregunta'
        managed = False

    def __str__(self):
        return f"BancoPregunta {self.pk}"


class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=200)
    cedula = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'estudiante'
        managed = False

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Prueba(models.Model):
    fechainicio = models.DateField(db_column='FechaInicio')
    fechafin = models.DateField(db_column='FechaFin')
    estado = models.BooleanField(db_column='Estado')

    class Meta:
        db_table = 'prueba'
        managed = False

    def __str__(self):
        return f"Prueba desde {self.fechainicio} hasta {self.fechafin}"


class Examen(models.Model):
    titulo = models.CharField(max_length=255)
    estado = models.BooleanField()
    descripcion = models.TextField()
    idprueba = models.ForeignKey(
        Prueba,
        models.DO_NOTHING,
        db_column='IdPrueba',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'examen'
        managed = False

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    url_imagen = models.CharField(max_length=255)
    cuerpo = models.TextField()
    idbancopregunta = models.ForeignKey(
        Bancopregunta,
        models.DO_NOTHING,
        db_column='IdBancoPregunta',
        blank=True,
        null=True
    )
    idprueba = models.ForeignKey(
        Prueba,
        models.DO_NOTHING,
        db_column='IdPrueba',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'pregunta'
        managed = False

    def __str__(self):
        return f"Pregunta {self.pk}: {self.cuerpo[:30]}..."


class Respuesta(models.Model):
    descripcion = models.TextField()
    estado = models.BooleanField()
    idpregunta = models.ForeignKey(
        Pregunta,
        models.DO_NOTHING,
        db_column='idPregunta',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'respuesta'
        managed = False

    def __str__(self):
        return f"Respuesta {self.pk}: {self.descripcion[:30]}..."


class Resultado(models.Model):
    puntaje = models.IntegerField()
    idestudiante = models.ForeignKey(
        Estudiante,
        models.DO_NOTHING,
        db_column='IdEstudiante',
        blank=True,
        null=True
    )
    idexamen = models.ForeignKey(
        Examen,
        models.DO_NOTHING,
        db_column='IdExamen',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'resultado'
        managed = False

    def __str__(self):
        return f"Resultado de {self.idestudiante} - {self.puntaje} pts"


class RespuestaEstudiante(models.Model):
    idresultado = models.ForeignKey(
        Resultado,
        models.DO_NOTHING,
        db_column='IdResultado',
        blank=True,
        null=True
    )
    idpregunta = models.ForeignKey(
        Pregunta,
        models.DO_NOTHING,
        db_column='IdPregunta',
        blank=True,
        null=True
    )
    idrespuesta = models.ForeignKey(
        Respuesta,
        models.DO_NOTHING,
        db_column='IdRespuesta',
        blank=True,
        null=True
    )
    es_correcta = models.BooleanField(db_column='Es_Correcta')

    class Meta:
        db_table = 'respuesta_estudiante'
        managed = False

    def __str__(self):
        estado = "Correcta" if self.es_correcta else "Incorrecta"
        return f"Resp. estudiante {self.pk} - {estado}"


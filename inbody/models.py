from django.db import models

class Student(models.Model):
    uid = models.CharField(primary_key=True, max_length=255, db_column='uid')
    name = models.CharField(db_column='name')
    school = models.CharField(max_length=255, db_column='school')
    grade = models.IntegerField(db_column='grade')
    class_num = models.IntegerField(db_column='class_num')
    number = models.IntegerField(db_column='number')
    gender = models.BooleanField(db_column='gender')

    class Meta:
        managed = False
        db_table = 'students'

    def __str__(self):
        return f"{self.name} - {self.school} - {self.grade}/{self.class_num}/{self.number}"

class GameRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=255)
    game_type = models.CharField(max_length=255)
    start_ts = models.IntegerField()
    finish_ts = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'game_records'

class InBodyRecord(models.Model):
    record_id = models.CharField(primary_key=True, max_length=64)
    uid = models.CharField(max_length=30)
    timestamp = models.BigIntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    fat = models.FloatField()
    fat_ratio = models.FloatField()
    muscle = models.FloatField()
    skeletal_muscle = models.FloatField()
    water_content = models.FloatField()
    bmi = models.FloatField()

    class Meta:
        managed = False
        db_table = 'inbody_records'

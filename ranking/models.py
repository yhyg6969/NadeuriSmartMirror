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
        managed = False  # Set this to False to indicate that Django should not manage the table
        db_table = 'students'  # Set this to the actual table name in your PostgreSQL database

    def __str__(self):
        return f"{self.name} - {self.school} - {self.grade}/{self.class_num}/{self.number}"
    


class GameRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=255)
    game_type = models.CharField(max_length=255)
    start_ts = models.IntegerField()  # Change to IntegerField if timestamps fit within its range
    finish_ts = models.IntegerField()  # Change to IntegerField if timestamps fit within its range

    class Meta:
        managed = False
        db_table = 'game_records'

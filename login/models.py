# login/models.py

from django.db import models

class Student(models.Model):
    uid = models.CharField(primary_key=True, db_column='uid')
    name = models.CharField(db_column='name')
    school = models.CharField(max_length=255, db_column='school')
    grade = models.IntegerField(db_column='grade')
    class_num = models.IntegerField(db_column='class_num')
    number = models.IntegerField(db_column='number')
    gender = models.BooleanField(db_column='gender')

    def generate_password(self):
        # Ensure class_num and number are formatted as two-digit numbers
        class_num_str = str(self.class_num).zfill(2)
        number_str = str(self.number).zfill(2)
        
        # Concatenate grade, class_num, and number to form a 5-digit password
        password = f"{self.grade}{class_num_str}{number_str}"
        return password

    def __str__(self):
        return f"{self.school} - {self.grade} - {self.class_num} - {self.number}"

    class Meta:
        managed = False  # Set this to False to indicate that Django should not manage the table
        db_table = 'students'  # Set this to the actual table name in your PostgreSQL database

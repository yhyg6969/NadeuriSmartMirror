from django.db import models


class user_table(models.Model):
    uid = models.CharField(primary_key=True, max_length=255, db_column='uid')
    user_name = models.CharField(max_length=255, db_column='user_name')
    center_name = models.CharField(max_length=255, db_column='center_name')
    birth = models.IntegerField(db_column='birth')
    gender = models.BooleanField(db_column='gender')

    class Meta:
        managed = False
        db_table = 'user_table'


class game_table(models.Model):
    record_id = models.AutoField(primary_key=True, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    game_name = models.CharField(max_length=255, db_column='game_name')
    game_type = models.CharField(max_length=255, db_column='game_type')
    play_time = models.IntegerField(db_column='play_time')
    correct_score = models.IntegerField(db_column='correct_score')
    fail_score = models.IntegerField(db_column='fail_score')
    start_ts = models.IntegerField(db_column='start_ts')
    finish_ts = models.IntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'game_table'


class walk_table(models.Model):
    record_id = models.AutoField(primary_key=True, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    walk_name = models.CharField(max_length=255, db_column='walk_name')
    walk_time = models.IntegerField(db_column='walk_time')
    walk_count = models.IntegerField(db_column='walk_count')
    velocity = models.IntegerField(db_column='velocity')
    start_ts = models.IntegerField(db_column='start_ts')
    finish_ts = models.IntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'walk_table'



class stretch_table(models.Model):
    record_id = models.AutoField(primary_key=True, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    stretch_name = models.CharField(max_length=255, db_column='stretch_name')
    stretch_type = models.CharField(max_length=255, db_column='stretch_type')
    stretch_time = models.IntegerField(db_column='stretch_time')
    acc_average = models.IntegerField(db_column='acc_average')
    start_ts = models.IntegerField(db_column='start_ts')
    finish_ts = models.IntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'stretch_table'


class center_table(models.Model):
    center_id = models.AutoField(primary_key=True, db_column='center_uid')
    center_name = models.CharField(max_length=255, db_column='center_name')
    center_password = models.CharField(max_length=255, db_column='center_password')

    class Meta:
        managed = False
        db_table = 'center_table'


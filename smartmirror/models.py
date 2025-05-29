from django.db import models


class user_table(models.Model):
    uid = models.CharField(primary_key=True, max_length=255, db_column='uid')
    user_name = models.CharField(max_length=255, db_column='user_name')
    center_name = models.CharField(max_length=255, db_column='center_name')
    birth = models.CharField(max_length=8, db_column='birth')  # CHAR(8) → CharField
    gender = models.BooleanField(db_column='gender')

    class Meta:
        managed = False
        db_table = 'user_table'


class center_table(models.Model):
    center_id = models.AutoField(primary_key=True, db_column='center_uid')
    center_name = models.CharField(max_length=255, db_column='center_name')
    center_password = models.CharField(max_length=255, db_column='center_password')
    center_salt = models.CharField(max_length=255, db_column='center_salt')

    class Meta:
        managed = False
        db_table = 'center_table'


class smartmirror_table(models.Model):
    record_id = models.CharField(primary_key=True, max_length=64, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    game_name = models.CharField(max_length=255, db_column='game_name')
    game_type = models.IntegerField(db_column='game_type')
    play_time = models.BigIntegerField(db_column='play_time')
    correct_score = models.IntegerField(db_column='correct_score')
    fail_score = models.IntegerField(db_column='fail_score')
    start_ts = models.BigIntegerField(db_column='start_ts')
    finish_ts = models.BigIntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'smartmirror_table'


class sprocket_table(models.Model):
    record_id = models.CharField(primary_key=True, max_length=64, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    sprocket_name = models.CharField(max_length=255, db_column='sprocket_name')
    sprocket_type = models.IntegerField(db_column='sprocket_type')
    sprocket_time = models.BigIntegerField(db_column='sprocket_time')
    sprocket_score = models.IntegerField(db_column='sprocket_score')
    start_ts = models.BigIntegerField(db_column='start_ts')
    finish_ts = models.BigIntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'sprocket_table'


class teblow_table(models.Model):
    record_id = models.CharField(primary_key=True, max_length=64, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    teblow_name = models.CharField(max_length=255, db_column='teblow_name')
    teblow_type = models.IntegerField(db_column='teblow_type')
    teblow_time = models.BigIntegerField(db_column='teblow_time')
    teblow_score = models.IntegerField(db_column='teblow_score')
    start_ts = models.BigIntegerField(db_column='start_ts')
    finish_ts = models.BigIntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'teblow_table'


class paps_table(models.Model):
    record_id = models.CharField(primary_key=True, max_length=64, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    paps_name = models.CharField(max_length=255, db_column='paps_name')
    paps_type = models.IntegerField(db_column='paps_type')
    paps_time = models.IntegerField(db_column='paps_time')
    paps_repeat = models.IntegerField(db_column='paps_repeat')
    paps_difficulty = models.IntegerField(db_column='paps_difficulty')
    paps_score = models.IntegerField(db_column='paps_score')
    paps_percents = models.CharField(max_length=64, db_column='paps_percents')
    start_ts = models.BigIntegerField(db_column='start_ts')
    finish_ts = models.BigIntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'paps_table'


class dtx_table(models.Model):
    record_id = models.CharField(primary_key=True, max_length=64, db_column='record_id')
    uid = models.CharField(max_length=255, db_column='uid')
    dtx_name = models.CharField(max_length=255, db_column='dtx_name')
    dtx_type = models.IntegerField(db_column='dtx_type')
    dtx_time = models.BigIntegerField(db_column='dtx_time')
    dtx_score = models.IntegerField(db_column='dtx_score')
    start_ts = models.BigIntegerField(db_column='start_ts')
    finish_ts = models.BigIntegerField(db_column='finish_ts')

    class Meta:
        managed = False
        db_table = 'dtx_table'

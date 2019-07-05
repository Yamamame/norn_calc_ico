from django.db import models

class payment_history(models.Model):
    # execute date
    exec_date = models.DateTimeField()
    # operation id part 1
    operation_id_1 = models.CharField(max_length=15)
    # operation id part 2
    operation_id_2 = models.CharField(max_length=15)
    # operation id part 3
    operation_id_3 = models.CharField(max_length=15)
    # operation id part 4
    operation_id_4 = models.CharField(max_length=15)
    # operation id part 5
    operation_id_5 = models.CharField(max_length=15)
    # type
    payment_type = models.CharField(max_length=64)
    # amount
    amount = models.FloatField()
    # t_hash
    t_hash = models.CharField(max_length=256)
    # main_balance
    main_balance = models.FloatField()
    # currency
    currency = models.CharField(max_length=8)
    # udate_at
    update_at =  models.DateTimeField()

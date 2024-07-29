# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ComplainDetails(models.Model):
    complain_id = models.IntegerField(db_column='complain_id', db_comment='foreign key')  # Field name made lowercase.
    product_id = models.IntegerField(db_comment='product yg dicomplain')
    process_name = models.CharField(max_length=25)
    complaincategory_id = models.SmallIntegerField(db_comment='another table')
    complain_description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'complain_details'



class Complain(models.Model):
    complain_type = models.SmallIntegerField()
    customer_id = models.IntegerField(db_comment='customer who complains')
    nomor_document = models.CharField(max_length=200, db_comment='nomor IC')
    document_date = models.DateField(db_comment='tanggal IC')
    created_by = models.CharField(max_length=30)
    created_date = models.DateField(blank=True, null=True)
    updated_by = models.CharField(max_length=30, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'complain'

class ComplainCategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'complain_category'

class Companies(models.Model):
    name = models.CharField(max_length=100)
    npwp = models.CharField(max_length=20)
    contact = models.CharField(max_length=100)
    top_id = models.PositiveSmallIntegerField()
    type = models.PositiveIntegerField()
    status = models.PositiveIntegerField(db_comment='9-> di hold pengiriman')
    efakturaddress_type = models.PositiveIntegerField(db_comment='1-> Alamat mengacu ke NPWP pusat, 2->Alamat mengacu ke alamat kirim')
    rating = models.PositiveIntegerField()
    keterangan = models.CharField(max_length=250, blank=True, null=True)
    balance_ar = models.DecimalField(max_digits=15, decimal_places=2)
    balance_ap = models.DecimalField(max_digits=15, decimal_places=2)
    created_by = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'companies'

class Employees(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'employees'

class Products(models.Model):
    name = models.CharField(max_length=250)
    name2 = models.CharField(max_length=250, blank=True, null=True, db_comment='Untuk Item Code')
    customer = models.ForeignKey(Companies, models.DO_NOTHING)
    marketing = models.ForeignKey(Employees, models.DO_NOTHING)
    category_id = models.PositiveIntegerField()
    type_id = models.PositiveIntegerField()
    unit_fg = models.CharField(max_length=5, db_comment='PCS, ROLL, KG')
    unit_po = models.CharField(max_length=5, db_comment='PCS, ROLL, KG')
    quantity_per_ufg = models.DecimalField(max_digits=10, decimal_places=2, db_comment='How many Unit_PO in one unit of FG. Example: 12500 PCS PER ROLL')
    buffered_quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_comment='How many we already have buffer stock (in unit_fg)')
    number_color = models.PositiveIntegerField(db_comment='Berapa warna')
    number_material = models.PositiveIntegerField(db_comment='Berapa material')
    width_fg = models.DecimalField(max_digits=10, decimal_places=2, db_comment='Lebar Produk Jadi')
    width_design = models.DecimalField(max_digits=10, decimal_places=2)
    height_fg = models.DecimalField(max_digits=10, decimal_places=2, db_comment='TInggi Produk jadi')
    height_design = models.DecimalField(max_digits=10, decimal_places=2)
    length_fg = models.PositiveSmallIntegerField(db_comment='Bila unit_fg dalam bentuk Roll, 1 roll ada berapa meter')
    bagmaking_up = models.PositiveIntegerField()
    sideseal_width = models.DecimalField(max_digits=10, decimal_places=2, db_comment='For 3-side seal, std pouch, diapers')
    bottomseal_height = models.DecimalField(max_digits=10, decimal_places=2)
    sidegusset_size = models.DecimalField(max_digits=10, decimal_places=2)
    bottomgusset_size = models.DecimalField(max_digits=10, decimal_places=2)
    revisi = models.PositiveIntegerField(db_comment='Revisi keberapa. Contoh: revisi Nomor MD')
    notes = models.CharField(max_length=250, blank=True, null=True)
    revisi_notes = models.TextField(blank=True, null=True, db_comment='Keterangan Revisi')
    status = models.PositiveIntegerField(db_comment='0-> obsolete, 1->active, 2->inactive')
    created_by = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'products'
        
class IcCapa(models.Model):
    id = models.BigAutoField(primary_key=True)
    complain_id = models.PositiveIntegerField()
    complaindetail_id = models.PositiveBigIntegerField()
    corrective_action = models.TextField(blank=True, null=True)
    perventive_action = models.TextField(blank=True, null=True)
    pic = models.CharField(db_column='PIC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateField(blank=True, null=True)
    verifikasi = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ic_capa'


class IcProblemanalysis(models.Model):
    id = models.BigAutoField(primary_key=True)
    complain_id = models.PositiveIntegerField()
    complaindetail_id = models.PositiveBigIntegerField()
    analysis_category = models.CharField(max_length=25, db_comment='MAN, MACHINE, METHOD, MATERIAL, ENVIRONMENT')
    analysis_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'ic_problemanalysis'

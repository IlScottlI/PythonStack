from django.db import models

# Create your models here.


class Dojo(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    desc = models.TextField(null=True)

    def __str__(self):
        return f"<Dojo object: {self.name} ({self.id})>"


class Ninja(models.Model):
    dojo_id = models.ForeignKey(
        Dojo, related_name="Dojo", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Sector(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SubSector(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductFamily(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OtherIndividuals(models.Model):
    user = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class ProductType(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AdditionalDetail(models.Model):
    ulid = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.UUID} - {self.details}"


class Action(models.Model):
    title = models.TextField()
    due_date = models.DateTimeField(blank=True)
    complete_date = models.DateTimeField(blank=True)
    owner = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class QADB(models.Model):
    sector_id = models.ForeignKey(
        Sector,
        related_name="sector_qadb",
        on_delete=models.CASCADE
    )
    sector_sub_id = models.ForeignKey(
        SubSector,
        related_name="sub_sector_qadb",
        on_delete=models.CASCADE
    )
    prod_fam_id = models.ForeignKey(
        ProductFamily,
        related_name="prod_fam_qadb",
        on_delete=models.CASCADE
    )
    category_id = models.ForeignKey(
        Category,
        related_name="category_qadb",
        on_delete=models.CASCADE
    )
    originator = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    short_desc = models.TextField()
    Standard = models.TextField(blank=True)
    desc_by = models.CharField(max_length=255)
    other_ind_id = models.ForeignKey(
        OtherIndividuals,
        related_name="other_ind_qadb",
        on_delete=models.CASCADE
    )
    when_desc = models.DateTimeField()
    process_order = models.CharField(max_length=255)
    defect_start = models.DateTimeField()
    defect_end = models.DateTimeField()
    product_type_id = models.ForeignKey(
        ProductType,
        related_name="product_type_qadb",
        on_delete=models.CASCADE
    )
    product_desc = models.TextField()
    brand_code = models.CharField(max_length=255)
    day_code = models.CharField(max_length=255)
    quanity = models.IntegerField()
    unit_of_measure = models.CharField(max_length=100)
    YE = 'Yes'
    NO = 'No'
    UK = 'Unknown'
    CHOICES = [
        (YE, 'Yes'),
        (NO, 'No'),
        (UK, 'Unknown'),
    ]
    scrapped = models.CharField(
        max_length=8,
        choices=CHOICES,
        default=None,
    )
    steam_number = models.CharField(max_length=100)
    failure_memo = models.CharField(
        max_length=8,
        choices=CHOICES,
        default=None,
    )
    need_to_hold = models.CharField(
        max_length=8,
        choices=CHOICES,
        default=None,
    )
    need_rework = models.CharField(
        max_length=8,
        choices=CHOICES,
        default=None,
    )
    root_cause = models.TextField(null=True)
    additional_info = models.TextField(null=True)
    actions = models.ForeignKey(
        Action,
        related_name="actions_qadb",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

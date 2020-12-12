from dojo_ninjas_app.models import Dojo, Ninja 

Dojo.objects.create(name="Coding Dojo Arlington", city="Arlington",state="VA")
Dojo.objects.create(name="Coding Dojo Bellevue", city="Bellevue", state="WA")
Dojo.objects.create(name="Coding Dojo Dallas", city="Dallas", state="TX")

Dojo.objects.get(id=1).delete()
Dojo.objects.get(id=2).delete()
Dojo.objects.get(id=3).delete()

Dojo.objects.create(name="Coding Dojo Arlington", city="Arlington",state="VA")
Dojo.objects.create(name="Coding Dojo Bellevue", city="Bellevue", state="WA")
Dojo.objects.create(name="Coding Dojo Dallas", city="Dallas", state="TX")

Ninja.objects.create(dojo_id=Dojo.objects.get(id=4),first_name='Scott',last_name='Johnson')
Ninja.objects.create(dojo_id=Dojo.objects.get(id=4),first_name='Mr',last_name='Man')
Ninja.objects.create(dojo_id=Dojo.objects.get(id=4),first_name='Jane',last_name='Doe')

Ninja.objects.create(dojo_id=Dojo.objects.get(id=5),first_name='Scott',last_name='Johnson')
Ninja.objects.create(dojo_id=Dojo.objects.get(id=5),first_name='Mr',last_name='Man')
Ninja.objects.create(dojo_id=Dojo.objects.get(id=5),first_name='Jane',last_name='Doe')

Ninja.objects.create(dojo_id=Dojo.objects.get(id=6),first_name='Scott',last_name='Johnson')
Ninja.objects.create(dojo_id=Dojo.objects.get(id=6),first_name='Mr',last_name='Man')
Ninja.objects.create(dojo_id=Dojo.objects.get(id=6),first_name='Jane',last_name='Doe')

Ninja.objects.first()
Ninja.objects.last()

Ninja.objects.last().dojo_id.id

desc = models.TextField(null=True)


Dojo.objects.create(name="Coding Dojo Dallas", city="Dallas", state="TX", desc="Desc")
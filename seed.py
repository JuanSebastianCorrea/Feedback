from models import User, Feedback, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

User.query.delete()
Feedback.query.delete()

f1 = Feedback(title='fin', content='Finance', username='Muffingirl')
f2 = Feedback(title='legal', content='Legal', username='Muffingirl')
f3 = Feedback(title='mktg', content='Marketing', username='Bluethecat')
f4 = Feedback(title='mktg', content='Marketing', username='Bluethecat')

leonard = Employee(name='Leonard', dept=dl)
liz = Employee(name='Liz', dept=dl)
maggie = Employee(name='Maggie', state='DC', dept=dm)
nadine = Employee(name='Nadine')

db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
db.session.commit()

pc = Project(proj_code='car', proj_name='Design Car',
             assignments=[EmployeeProject(emp_id=liz.id, role='Chair'),
                          EmployeeProject(emp_id=maggie.id)])
ps = Project(proj_code='server', proj_name='Deploy Server',
             assignments=[EmployeeProject(emp_id=liz.id),
                          EmployeeProject(emp_id=leonard.id, role='Auditor')])

db.session.add_all([ps, pc])
db.session.commit()
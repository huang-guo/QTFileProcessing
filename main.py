import database
from component.myForm import MyForm

if __name__ == '__main__':
    database.create_all()
    root = MyForm()
    root.mainloop()

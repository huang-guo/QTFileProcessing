from database import create_all
from component.myForm import MyForm

if __name__ == '__main__':
    create_all()
    root = MyForm()
    root.mainloop()

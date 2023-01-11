class mixin_DS:
    def department_ds(self):
        return 'Open DS department'

class mixin_DEV:
    def department_dev(self):
        return 'Open development department'

class mixin_Test:
    def department_test(self):
        return 'Open testing department'

class Base_company:
    pass

class Company_dev(Base_company, mixin_DEV, mixin_Test)
    pass

class Company_ds(Base_company, mixin_DS, mixin_Test)
    pass

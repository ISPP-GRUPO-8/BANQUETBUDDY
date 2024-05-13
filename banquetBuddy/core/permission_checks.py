
#####Check kind of user#####
def is_user_employee(user):
    return hasattr(user, 'EmployeeUsername')

def is_user_catering_company(user):
    return hasattr(user, 'CateringCompanyusername')

def is_user_particular(user):
    return hasattr(user, 'ParticularUsername')

#####Check if user can modify entity#####


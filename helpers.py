from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    uppercase = 1,    # need min. 1 uppercase letters
    numbers = 1,      # need min. 1 digits
    special = 1,      # need min. 1 special characters
)

specialities_possible = ["endocrinologist",
                         'gynecologist',
                         'surgeon',
                         'cardiologist',
                         'neurologist',
                         'allegologist',
                         ]

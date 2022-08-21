def approved_appointment(first_name, date_of_appointment):
    """
    Creates email body template for approved appointments

    Args:
        first_name: name of recipient
        date_of_appointment: date of appointment

    Return: html string holding the email body
    """
    template = f"""
        <html>
            <head></head>
            <h1 style='text-align:center'>Approved appointment!</h1>
            <p><br>Hello {first_name},</br> 
                    <br>Your appointment for {date_of_appointment} is approved!</br>
               <br>Kind Regards,</br>
               Online Doctor appointments' Team</p>
            </body>
        </html>
    """
    return template


def rejected_appointment(first_name, date_of_appointment):
    """
    Creates email body template for rejected appointments

    Args:
        first_name: name of recipient
        date_of_appointment: date of appointment

    Return: html string holding the email body
    """
    template = f"""
            <html>
                <head></head>
                <h1 style='text-align:center'>Rejected appointment!</h1>
                <p><br>Hello {first_name},</br>
                        <br>Unfortunately, Your appointment for {date_of_appointment} has been rejected!
                        Please try again or contact us at 00000000000.</br>
                   <br>Kind Regards,</br>
                   Online Doctor appointments' Team</p>
                </body>
            </html>
        """
    return template

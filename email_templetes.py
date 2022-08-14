def approved_appointment(date_of_appointment):
    templete = f"""
        <html>
            <head></head>
            <h1 style='text-align:center'>Approved appointment!</h1>
            <p>Hello, 
                    Your appointment for {date_of_appointment} is approved!
               Kind Regards,
               Online Doctor appointments' Team</p>
            </body>
        </html>
    """
    return templete

def rejected_appointment(date_of_appointment):
    templete = f"""
            <html>
                <head></head>
                <h1 style='text-align:center'>Approved appointment!</h1>
                <p>Hello, 
                        Unfortunately, Your appointment for {date_of_appointment} has been rejected!
                        Please try again or contact us at 00000000000.
                   Kind Regards,
                   Online Doctor appointments' Team</p>
                </body>
            </html>
        """
    return templete
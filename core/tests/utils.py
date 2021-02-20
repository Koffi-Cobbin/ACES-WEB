from .. import models


def createConfiguration(
    location: str = "KNUST",
    main_phone_number: str = "0200000000",
    office_phone_number: str = "0200000000",
    email_address: str = "aces_knust@acesknust.org",
    about: str = "The about of aces",
    history: str = "The history of aces",
    whatsapp_link: str = "https://wa.me/",
    facebook_link: str = "https://facebook.com",
    twitter_link: str = "https://twitter.com",
    youtube_link: str = "http://youtube.com"
    
):
    """
    Create a basic configuration for the site
    """

    return models.Configuration.objects.create(
        location=location,
        main_phone_number = main_phone_number,
        office_phone_number = office_phone_number,
        email_address = email_address,
        about = about,
        history = history,
        whatsapp_link = whatsapp_link,
        facebook_link = facebook_link,
        twitter_link = twitter_link,
        youtube_link = youtube_link
    )

def createExecutiveRole(name: str="President", core=True, duty: str="The duty of the office"):
    """
    Create an executive role.
    """
    return models.ExecutiveRole.objects.create(name=name, core=core, duty=duty)
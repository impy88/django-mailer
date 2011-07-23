from distutils.core import setup


setup(
    name="django-scheduled-mailer",
    version=__import__("scheduled_mailer").__version__,
    description="A reusable Django app for queuing the sending of email",
    long_description=open("docs/usage.txt").read(),
    author="Eugene Glybin",
    author_email="aeron@aeron.cc",
    url="https://github.com/Aeron/django-mailer",
    packages=[
        "scheduled_mailer",
        "scheduled_mailer.management",
        "scheduled_mailer.management.commands",
    ],
    package_dir={"scheduled_mailer": "scheduled_mailer"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)

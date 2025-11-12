import calendar
from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from data.abstractions import DatabaseQueryHandler
from data.models import BirthdayReminder, Contact, Tag


class ContactQueries(DatabaseQueryHandler):
    def get_contacts(self) -> list[Contact]:
        with Session(self.engine) as session:
            query = select(Contact)
            contacts = session.scalars(query)
            return list(contacts)

    def get_contacts_by_tag(self, tag: str) -> list[Contact]:
        with Session(self.engine) as session:
            query = select(Contact).join(Contact.tags).where(Tag.label == tag)
            contacts = session.scalars(query)
            return list(contacts)

    def get_contact_by_id(self, contact_id: int) -> Contact | None:
        with Session(self.engine) as session:
            query = select(Contact).where(Contact.contact_id == contact_id)
            contact = session.scalar(query)
            return contact

    def get_contact_by_name(self, contact_name: str) -> Contact | None:
        with Session(self.engine) as session:
            query = select(Contact).where(Contact.name == contact_name)
            contact = session.scalar(query)
            return contact

    def get_contacts_with_birthdays_in_days(self, days_before_reminder: int) -> list[BirthdayReminder]:
        """
        Get contacts with birthdays in the next N days.
        """

        def get_workday_celebration_day_for(birthday: date) -> date:
            """
            Returns celebration day from birthday by shifting it away from weekend:
            Saturday to Monday,
            Sunday to Monday
            """
            weekday = birthday.isoweekday()
            shift = 0 if weekday not in [6, 7] else (8 - weekday)
            return birthday + timedelta(days=shift)

        def get_this_date_at_year(dob: date, year: int) -> date:
            if dob.month == 2 and dob.day == 29 and not calendar.isleap(year):
                return date(year, 3, 1)
            return date(year, dob.month, dob.day)

        def get_next_celebration_day(dob: date) -> date:
            """
            Returns celebration day on current year or next.
            """
            today = date.today()
            birthday = get_this_date_at_year(dob, today.year)
            # Get celebration date before comparison with today:
            # If birthday is on Saturday, and today is Sunday - we still can congratulate on Monday
            celebration = get_workday_celebration_day_for(birthday)
            if celebration >= today:
                return celebration
            else:
                # If celebration date passed - congratulation comes next year
                birthday = get_this_date_at_year(dob, today.year + 1)
                celebration = get_workday_celebration_day_for(birthday)
                return celebration

        with Session(self.engine) as session:
            query = select(Contact).where(Contact.date_of_birth.is_not(None))
            contacts = session.scalars(query)
            today = date.today()
            reminders: list[BirthdayReminder] = []
            for contact in contacts:
                if contact.date_of_birth is None:
                    continue

                celebration_day = get_next_celebration_day(contact.date_of_birth)
                days_to_celebration = (celebration_day - today).days
                if days_to_celebration > days_before_reminder:
                    continue

                reminder = BirthdayReminder(
                    contact=contact,
                    bidthday=celebration_day
                )
                reminders.append(reminder)

            return reminders

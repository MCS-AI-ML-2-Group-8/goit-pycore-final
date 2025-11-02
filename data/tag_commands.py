from data.abstractions import DomainCommand

class AddTag(DomainCommand):
    label: str

class RemoveTag(DomainCommand):
    label: str
